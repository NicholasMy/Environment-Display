from NTIEnvironmentMonitor import NTIEnvironmentMonitor
from backend import login_secrets
from backend.OlderNTIEnvironmentMonitor import OlderNTIEnvironmentMonitor
import requests


def main():
    monitor = NTIEnvironmentMonitor("test", "test", "https://temp-davis-339e.cse.buffalo.edu/",
                                    login_secrets.NTI_USERNAME, login_secrets.NTI_PASSWORD)
    # monitor = OlderNTIEnvironmentMonitor("davis339cold", "Davis 339c Old", "http://enviromux-davis-339c.cse.buffalo.edu/")
    monitor.create_session()
    print(monitor.fetch_data())
    monitor.reboot()

    # url = "https://temp-davis-339e.cse.buffalo.edu/goform/reboot"
    #
    # payload = {'magic': '936438'}
    # files = [
    #
    # ]
    # # headers = {
    # #     # 'Cookie': monitor.session_cookie
    # #     'Cookie': "sessionId=cmVhZG9ubHk6Vnp5JnBwdF44cTV1UkxpVDUqJlV3eXZUYlUjQXI6Mg="
    # # }
    #
    # cookies = {
    #     'sessionId': "cmVhZG9ubHk6Vnp5JnBwdF44cTV1UkxpVDUqJlV3eXZUYlUjQXI6Mg=="
    # }
    #
    # print(monitor.session_cookie)
    #
    # req = requests.Request("POST", url, cookies=cookies, data=payload, files=files)
    # prepared = req.prepare()
    # print(prepared)
    #
    # response = requests.Session().send(prepared)
    #
    # print(response.text)


if __name__ == '__main__':
    main()
