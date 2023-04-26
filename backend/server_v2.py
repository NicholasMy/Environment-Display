import asyncio
import json
from datetime import datetime
from time import sleep
import socketio
from tornado import ioloop
import login_secrets as secrets
from typing import List, Optional, Awaitable
from threading import Lock, Thread
import tornado.web

from backend import database
from backend.EnvironmentalMonitor import EnvironmentalMonitor
from backend.MockEnvironmentMonitor import MockEnvironmentMonitor
from backend.NTIEnvironmentMonitor import NTIEnvironmentMonitor
from backend.OlderNTIEnvironmentMonitor import OlderNTIEnvironmentMonitor
from backend.database import Record

CACHE = {}
CACHE_UPDATED = False
CACHE_LOCK = Lock()
sio = socketio.AsyncServer(async_mode='tornado', cors_allowed_origins="*")  # Not secure, but Nginx will change this


def __get_failure_dictionary():
    return {
        "success": False
    }


monitors: List[EnvironmentalMonitor] = [
    NTIEnvironmentMonitor("davis339a", "Davis 339A", "https://temp-davis-339a.cse.buffalo.edu/",
                          secrets.NTI_USERNAME, secrets.NTI_PASSWORD, 23.0),
    # MockEnvironmentMonitor("mockdavis339a", "Mock Davis 339A", "https://temp-davis-339a.cse.buffalo.edu/", 3.0),
    NTIEnvironmentMonitor("davis339c", "Davis 339C", "https://temp-davis-339c.cse.buffalo.edu/",
                          secrets.NTI_USERNAME, secrets.NTI_PASSWORD, 22.0),
    NTIEnvironmentMonitor("davis339e", "Davis 339E North", "https://temp-davis-339e.cse.buffalo.edu/",
                          secrets.NTI_USERNAME, secrets.NTI_PASSWORD, 21.0),
    OlderNTIEnvironmentMonitor("davis339a_old", "Davis 339A Hot Aisle", "http://enviromux-davis-339a.cse.buffalo.edu/"),
    OlderNTIEnvironmentMonitor("davis339c_old", "Davis 339C Hot Aisle", "http://enviromux-davis-339c.cse.buffalo.edu/"),
    OlderNTIEnvironmentMonitor("davis339e_old", "Davis 339E South", "http://enviromux-davis-339e.cse.buffalo.edu/"),
]


# for i in range(5):
#     monitors.append(MockEnvironmentMonitor(f"mock{i}", f"Mock {i}", "https://temp-davis-339a.cse.buffalo.edu/", random() * 1))


class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def set_default_headers(self):
        # Allow * origins to all API endpoints in development
        self.set_header("Access-Control-Allow-Origin", "*")  # Not secure, but Nginx will change this


class MainHandler(BaseHandler):
    def get(self):
        self.write("Whoops, you probably meant to load the frontend or make a specific API call.")


class RoomsHandler(BaseHandler):
    def get(self):
        rooms_list = []
        for monitor in monitors:
            rooms_list.append({
                "name": monitor.name,
                "friendly_name": monitor.friendly_name
            })

        d = {
            "rooms": rooms_list
        }
        self.write(json.dumps(d))


class DataHandler(BaseHandler):
    def get(self):
        self.write(json.dumps(get_data()))


class HistoryHandler(BaseHandler):
    def get(self, monitor, days):
        self.write(Record.get_json_for_monitor(monitor, int(days)))


@sio.on('connect')
async def connect(sid, environ, auth):
    # Send the initial state when connecting
    await sio.emit("data", get_data(), room=sid)


@sio.on('disconnect')
async def disconnect(sid):
    pass


def get_data():
    global CACHE
    # Add the time the data was fetched
    data = CACHE.copy()
    data["time"] = datetime.now().isoformat()
    ret = {
        "data": data
    }
    return ret


def background_updater():
    print("Starting background updater")
    global CACHE
    global CACHE_LOCK
    global CACHE_UPDATED
    while True:
        for monitor in monitors:
            try:
                with CACHE_LOCK:
                    CACHE[monitor.name]["updating"] = True
                    CACHE_UPDATED = True
                data = monitor.fetch_data()
                with CACHE_LOCK:
                    CACHE[monitor.name] = data  # This removes the "updating" key
                    CACHE[monitor.name]["success"] = True
                    CACHE[monitor.name].pop("rebooting", None)
                    CACHE_UPDATED = True
                Record.create(monitor.name, data["temperature"]["current"], data["humidity"]["current"])
            except Exception as e:
                print("Error getting data for sensor ", monitor.url, str(e))
                with CACHE_LOCK:
                    CACHE[monitor.name] = __get_failure_dictionary()
                    if monitor.is_rebooting():
                        CACHE[monitor.name]["rebooting"] = True
                    CACHE_UPDATED = True
            reboot = monitor.reboot_necessary()
            if reboot:
                with CACHE_LOCK:
                    CACHE[monitor.name] = __get_failure_dictionary()
                    CACHE[monitor.name]["rebooting"] = True
                    CACHE_UPDATED = True
                monitor.reboot_if_needed()
        sleep(1)


async def background_sender():
    global CACHE_LOCK
    global CACHE_UPDATED
    CACHE_LOCK.acquire()
    if CACHE_UPDATED:
        CACHE_UPDATED = False
        CACHE_LOCK.release()
        await sio.emit("data", get_data())
    else:
        CACHE_LOCK.release()


async def initialize():
    global CACHE
    global CACHE_LOCK
    with CACHE_LOCK:
        for monitor in monitors:
            CACHE[monitor.name] = __get_failure_dictionary()


async def main():
    await initialize()
    global sio

    background_updater_thread = Thread(target=background_updater)
    background_updater_thread.daemon = True  # This thread will die when the main thread dies
    background_updater_thread.start()

    ioloop.PeriodicCallback(background_sender, 500).start()

    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/data", DataHandler),
        (r"/rooms", RoomsHandler),
        (r"/history/([a-zA-Z0-9_]+)/([0-9]+)", HistoryHandler),
        (r"/socket.io/", socketio.get_tornado_handler(sio)),
    ])

    app.listen(8085)
    print("Web server started on port 8085")

    await asyncio.Event().wait()


if __name__ == '__main__':
    database.initialize_database()
    asyncio.run(main())
