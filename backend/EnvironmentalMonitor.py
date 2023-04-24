class EnvironmentalMonitor:
    def create_session(self):
        raise NotImplementedError

    def is_rebooting(self) -> bool:
        return False

    def reboot_necessary(self) -> bool:
        return False

    def reboot_if_needed(self):
        pass

    def fetch_data(self) -> dict:
        raise NotImplementedError

    def __init__(self):
        self.name = None
        self.friendly_name = None
        self.url = None
