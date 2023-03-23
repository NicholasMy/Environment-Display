import random
import requests


class NTIEnvironmentMonitor:

    def __init__(self, name: str, friendly_name: str, url: str, username: str, password: str):
        # The URL should look like "https://temp-davis-339e.cse.buffalo.edu/"
        self.name = name
        self.friendly_name = friendly_name
        self.url = url
        self.username = username
        self.password = password
        self.session_cookie = None

    def create_session(self):
        login_url: str = self.url + "goform/login"
        data = {
            "username": self.username,
            "password": self.password,
            "random": random.random()
        }
        resp = requests.post(login_url, data=data, verify=False)
        # These monitors seem to use a really weak HTTPS certificate, so we need to disable verification
        resp = resp.json()
        success = resp["success"]
        if success == "true":
            cookie = resp["cookie"]
            self.session_cookie = cookie
        else:
            raise Exception(f"Login failed to: {self.url}")

    def fetch_data(self):
        d = {
            "name": self.name,
            "friendly_name": self.friendly_name,
        }

        if not self.session_cookie:
            self.create_session()

        temperature_url = self.url + "goform/sensorStatus?id=0"
        humidity_url = self.url + "goform/sensorStatus?id=1"

        try:
            temperature_data = requests.get(temperature_url, cookies={"session": self.session_cookie},
                                            verify=False).json()
            humidity_data = requests.get(humidity_url, cookies={"session": self.session_cookie}, verify=False).json()
        except Exception as e:
            # If that failed, we probably need a new session
            self.create_session()
            return self.fetch_data()

        d["temperature"] = temperature_data
        d["humidity"] = humidity_data

        return d
