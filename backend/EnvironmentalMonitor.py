class EnvironmentalMonitor:
    def create_session(self):
        raise NotImplementedError

    def fetch_data(self):
        raise NotImplementedError

    def __init__(self):
        self.name = None
        self.friendly_name = None
        self.url = None
