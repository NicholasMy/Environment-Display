import random
import requests

from backend.EnvironmentalMonitor import EnvironmentalMonitor


class NTIEnvironmentMonitor(EnvironmentalMonitor):

    def __init__(self, name: str, friendly_name: str, url: str, username: str, password: str):
        # The URL should look like "https://temp-davis-339e.cse.buffalo.edu/"
        super().__init__()
        self.name = name
        self.friendly_name = friendly_name
        self.url = url
        self.username = username
        self.password = password
        self.session_cookie = None

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

    def fetch_data(self):
        # print("Fetching data " + self.url)
        d = {
            "name": self.name,
            "friendly_name": self.friendly_name,
        }

        if not self.session_cookie:
            self.create_session()

        temperature_url = self.url + "goform/sensorStatus?id=0"
        humidity_url = self.url + "goform/sensorStatus?id=1"

        try:
            temperature_data = requests.get(temperature_url, cookies={"session": self.session_cookie}, timeout=10).json()
            humidity_data = requests.get(humidity_url, cookies={"session": self.session_cookie}, timeout=10).json()
        except Exception as e:
            # If that failed, we probably need a new session
            self.create_session()
            return self.fetch_data()

        d["temperature"] = temperature_data
        d["humidity"] = humidity_data
        d["url"] = self.url

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

        return d
