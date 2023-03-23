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
        self.session = None

    def create_session(self):
        login_url: str = self.name + "goform/login"
        data = {
            "username": self.username,
            "password": self.password,
            "random": random.random()
        }
        resp = requests.post(login_url, data=data)
        print(resp.text)
