import random
from datetime import datetime

import requests
from requests import ReadTimeout

from backend.EnvironmentalMonitor import EnvironmentalMonitor


class NTIEnvironmentMonitor(EnvironmentalMonitor):

    def __init__(self, name: str, friendly_name: str, url: str, username: str, password: str,
                 reboot_hours: float = 24.0, sensor_id: int = 0):
        # The URL should look like "https://temp-davis-339e.cse.buffalo.edu/"
        super().__init__()
        self.name = name
        self.friendly_name = friendly_name
        self.url = url
        self.username = username
        self.password = password
        self.reboot_hours = reboot_hours
        self.session_cookie = None
        self.last_reboot = datetime.now()
        self.rebooting = False
        self.sensor_id = sensor_id

    def get_seconds_since_last_reboot(self):
        return (datetime.now() - self.last_reboot).seconds

    def is_rebooting(self):
        return self.rebooting and self.get_seconds_since_last_reboot() < 120
        # If it's still offline 2 minutes after the reboot, it's probably not actually rebooting

    def reboot(self):
        if self.is_rebooting():
            print("Attempted to reboot while already rebooting. Ignoring. ", self.url)
            return
        print("Rebooting " + self.friendly_name)
        self.rebooting = True
        url = self.url + "goform/reboot"
        data = {
            "magic": 936438  # I don't know how this was chosen, but it's the same for all of them
        }
        try:
            self.create_session()
            res = requests.post(url, data=data, cookies={"session": self.session_cookie}, timeout=5)
            # print(res.text)
        except ReadTimeout:
            self.rebooting = False
            print("Reboot request timed out for " + self.url)
        except ConnectionError:
            self.rebooting = False
            print("Device is still rebooting " + self.url)
        except Exception:
            self.rebooting = False
            print("Reboot failed for " + self.url)
        self.last_reboot = datetime.now()

    def reboot_necessary(self) -> bool:
        if self.reboot_hours <= 0.0:
            return False
        return (datetime.now() - self.last_reboot).seconds / 60 / 60 > self.reboot_hours

    def reboot_if_needed(self):
        if self.reboot_necessary():
            self.reboot()

    def get_seconds_to_next_reboot(self):
        if self.reboot_hours <= 0.0:
            return -1.0
        return self.reboot_hours * 60 * 60 - (datetime.now() - self.last_reboot).seconds

    def create_session(self):
        # print("Creating session " + self.url)
        login_url: str = self.url + "goform/login"
        data = {
            "username": self.username,
            "password": self.password,
            "random": random.random()
        }
        resp = requests.post(login_url, data=data, timeout=10)
        resp = resp.json()
        success = resp["success"]
        if success == "true":
            cookie = resp["cookie"]
            self.session_cookie = cookie
        else:
            raise Exception(f"Login failed to: {self.url}")

    def fetch_data(self, retry=False):
        # retry will prevent infinite recursion. Set to true if this is the second attempt at fetching data.

        # print("Fetching data " + self.url)
        d = {
            "name": self.name,
            "friendly_name": self.friendly_name,
        }

        if not self.session_cookie:
            self.create_session()

        temperature_url = self.url + "goform/sensorStatus?id=" + str(self.sensor_id)
        humidity_url = self.url + "goform/sensorStatus?id=" + str(self.sensor_id + 1)

        try:
            temperature_data = requests.get(temperature_url,
                                            cookies={"session": self.session_cookie},
                                            timeout=5).json()
            humidity_data = requests.get(humidity_url,
                                         cookies={"session": self.session_cookie},
                                         timeout=5).json()
        except Exception as e:
            if retry:
                raise e  # Don't try again if this is the second attempt, just bubble up the exception

            # If that failed, we probably need a new session
            self.create_session()
            return self.fetch_data(retry=True)

        d["temperature"] = temperature_data
        d["humidity"] = humidity_data
        d["url"] = self.url
        d["next_reboot_seconds"] = self.get_seconds_to_next_reboot()

        # Convert strings to ints/floats if possible
        for measurement in ["temperature", "humidity"]:
            for key in d[measurement]:
                try:
                    d[measurement][key] = int(d[measurement][key])
                except ValueError:
                    try:
                        d[measurement][key] = float(d[measurement][key])
                    except ValueError:
                        pass

        self.rebooting = False
        return d
