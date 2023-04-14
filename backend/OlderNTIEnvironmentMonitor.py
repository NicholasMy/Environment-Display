from typing import Tuple, Dict, Any

import requests

from backend.EnvironmentalMonitor import EnvironmentalMonitor


class OlderNTIEnvironmentMonitor(EnvironmentalMonitor):

    def __init__(self, name: str, friendly_name: str, url: str):
        # The URL should look like "http://enviromux-davis-339e.cse.buffalo.edu/"
        super().__init__()
        self.name = name
        self.friendly_name = friendly_name
        self.url = url
        self.session_cookie = None

    def create_session(self):
        # print("Creating session " + self.url)

        pass
        # We're using guest access, no need to log in
        # They only support HTTP anyway, so it's more secure than sending a password to a privileged account


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

        # Find the line we care about
        for line in lines:
            if line.startswith("var haParams ="):
                data_line = line
                break

        if not data_line:
            raise Exception("Could not find data line")

        # Extract all the data from that one important line in a super ugly format
        data_arrays = data_line.split("new Array")
        for pair in [(d_temperature, 3), (d_humidity, 5)]:
            d, index = pair
            raw_values = data_arrays[index].split(",")
            for i, value in enumerate(raw_values):
                if value.startswith("\"") and value.endswith("\""):
                    raw_values[i] = value[1:-1]
                    try:
                        # Try to convert to floats
                        raw_values[i] = float(raw_values[i])
                    except ValueError:
                        pass
            d["current"] = raw_values[1]
            d["units"] = raw_values[2]
            d["maxThresh"] = raw_values[11]
            d["maxWThresh"] = raw_values[11]  # These older monitors don't have a separate warning/critical threshold

        return d_temperature, d_humidity

    def fetch_data(self):
        # print("Fetching data " + self.url)

        d = {
            "name": self.name,
            "friendly_name": self.friendly_name,
        }

        data_url = self.url + "Updater.html"

        try:
            data = requests.get(data_url, timeout=10)
            assert data.status_code == 200
            text = data.text
            parsed_temperature, parsed_humidity = self.parse_ugly_data(text)
            d["temperature"] = parsed_temperature
            d["humidity"] = parsed_humidity
        except Exception as e:
            # Ignore errors
            print(e)

        d["url"] = self.url

        return d
