from NTIEnvironmentMonitor import NTIEnvironmentMonitor
from backend import login_secrets
from backend.OlderNTIEnvironmentMonitor import OlderNTIEnvironmentMonitor


def main():
    # monitor = NTIEnvironmentMonitor("davis339e", "Davis 339e", "https://temp-davis-339e.cse.buffalo.edu/",
    #                                 login_secrets.NTI_USERNAME, login_secrets.NTI_PASSWORD)
    monitor = OlderNTIEnvironmentMonitor("davis339cold", "Davis 339c Old", "http://enviromux-davis-339c.cse.buffalo.edu/")
    monitor.create_session()
    print(monitor.fetch_data())


if __name__ == '__main__':
    main()
