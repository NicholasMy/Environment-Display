import time

from EnvironmentalMonitor import EnvironmentalMonitor


class MockEnvironmentMonitor(EnvironmentalMonitor):
    def create_session(self):
        pass

    def fetch_data(self):
        time.sleep(self.wait_time)
        raise Exception("Fake exception")

    def __init__(self, name: str, friendly_name: str, url: str, wait_time: float):
        super().__init__()
        self.name = name
        self.friendly_name = friendly_name
        self.url = url
        self.wait_time = wait_time
