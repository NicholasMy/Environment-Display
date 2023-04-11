import random
from typing import Tuple, Dict, Any

import requests

from backend.EnvironmentalMonitor import EnvironmentalMonitor


class OlderNTIEnvironmentMonitor(EnvironmentalMonitor):

    def __init__(self, name: str, friendly_name: str, url: str, username: str, password: str):
        # The URL should look like "http://enviromux-davis-339e.cse.buffalo.edu/"
        super().__init__()
        self.name = name
        self.friendly_name = friendly_name
        self.url = url
        self.username = username
        self.password = password
        self.session_cookie = None

    def create_session(self):
        login_url: str = self.url + "index.html"
        data = {
            "a": self.username,
            "b": self.password,
        }
        resp = requests.post(login_url, data=data, timeout=10)
        success = resp.status_code == 200
        if success:
            # For some reason, the cookie name is empty. What a great idea /s. We gotta read it this weird way.
            cookie = resp.raw.headers.get("Set-Cookie")
            print(cookie)
            if not cookie:
                print(resp.headers)
                raise Exception("Could not find cookie")
            self.session_cookie = cookie
        else:
            raise Exception(f"Login failed to: {self.url}")


    @staticmethod
    def parse_ugly_data(text: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        # These old environmental monitors embed the data in a JavaScript script in an HTML file.
        # It's super ugly to parse, so we'll do that here.
        # Return two dicts, one for temperature and one for humidity.

        # I started doing this with regex, but this is probably easier to read and understand.
        # ^var haParams = new Array.*?Temperature #2",".*?(?<current>.*?)","(?<units>.*?)",(.*?,){2}"(?<maxThresh>.*?)"

        d_temperature = {}
        d_humidity = {}

        # Get the line starting with var haParams =
        # This is the line that contains the data we want
        lines = text.splitlines()
        data_line = None
        for line in lines:
            if line.startswith("var haParams ="):
                data_line = line
                break

        if not data_line:
            raise Exception("Could not find data line")

        data_arrays = data_line.split("new Array")
        print()





    def fetch_data(self):
        d = {
            "name": self.name,
            "friendly_name": self.friendly_name,
        }

        if not self.session_cookie:
            self.create_session()

        data_url = self.url + "Updater.html"

        try:
            data = requests.get(data_url, headers={"Cookie": self.session_cookie}, timeout=10)
            assert data.status_code == 200
            text = data.text
            parsed_temperature, parsed_humidity = self.parse_ugly_data(text)

        except Exception as e:
            # If that failed, we probably need a new session
            self.create_session()
            return self.fetch_data()

        d["temperature"] = parsed_temperature
        d["humidity"] = parsed_humidity
        d["url"] = self.url

        return d
