from NTIEnvironmentMonitor import NTIEnvironmentMonitor
from backend import secrets

def main():
    monitor = NTIEnvironmentMonitor("davis339e", "Davis 339e", "https://temp-davis-339e.cse.buffalo.edu/",
                                    secrets.NTI_USERNAME, secrets.NTI_PASSWORD)
    monitor.create_session()
    print(monitor.fetch_data())


if __name__ == '__main__':
    main()
