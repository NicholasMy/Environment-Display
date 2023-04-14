import asyncio
import json
from datetime import datetime
from time import sleep

import socketio

import login_secrets as secrets
from typing import List
from threading import Lock, Thread

import tornado.web

from backend.EnvironmentalMonitor import EnvironmentalMonitor
from backend.NTIEnvironmentMonitor import NTIEnvironmentMonitor
from backend.OlderNTIEnvironmentMonitor import OlderNTIEnvironmentMonitor

CACHE = {}
CACHE_UPDATED = False
CACHE_LOCK = Lock()
sio = socketio.AsyncServer(async_mode='tornado', cors_allowed_origins="*")

__failure_dictionary = {
    "success": False
}

monitors: List[EnvironmentalMonitor] = [
    NTIEnvironmentMonitor("davis339a", "Davis 339A", "https://temp-davis-339a.cse.buffalo.edu/",
                          secrets.NTI_USERNAME, secrets.NTI_PASSWORD),
    NTIEnvironmentMonitor("davis339c", "Davis 339C", "https://temp-davis-339c.cse.buffalo.edu/",
                          secrets.NTI_USERNAME, secrets.NTI_PASSWORD),
    NTIEnvironmentMonitor("davis339e", "Davis 339E", "https://temp-davis-339e.cse.buffalo.edu/",
                          secrets.NTI_USERNAME, secrets.NTI_PASSWORD),
    OlderNTIEnvironmentMonitor("davis339a_old", "Davis 339A Old", "http://enviromux-davis-339a.cse.buffalo.edu/"),
    OlderNTIEnvironmentMonitor("davis339c_old", "Davis 339C Old", "http://enviromux-davis-339c.cse.buffalo.edu/"),
    OlderNTIEnvironmentMonitor("davis339e_old", "Davis 339E Old", "http://enviromux-davis-339e.cse.buffalo.edu/"),
]


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Whoops, you probably meant to load the frontend or make a specific API call.")


class RoomsHandler(tornado.web.RequestHandler):
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


class DataHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(get_data()))


@sio.on('connect')
async def connect(sid, b, c):
    print("Socket connected")
    print(sid, b, c)
    # TODO track set of connections, send data on first connection, send updates in background


@sio.on('disconnect')
async def disconnect(sid):
    print("Socket disconnected")
    print(sid)


def get_data():
    global CACHE
    # Add the time the data was fetched
    ret = CACHE.copy()
    ret["time"] = datetime.now().isoformat()
    return ret


def background_updater():
    global CACHE
    global CACHE_LOCK
    global CACHE_UPDATED
    while True:
        for monitor in monitors:
            try:
                data = monitor.fetch_data()
                with CACHE_LOCK:
                    CACHE[monitor.name] = data
                    CACHE[monitor.name]["success"] = True
                    CACHE_UPDATED = True
            except Exception as e:
                print(e)
                with CACHE_LOCK:
                    CACHE[monitor.name] = __failure_dictionary
                    CACHE_UPDATED = True

        sleep(1)


async def initialize():
    global CACHE
    global CACHE_LOCK
    with CACHE_LOCK:
        for monitor in monitors:
            CACHE[monitor.name] = __failure_dictionary


async def main():
    await initialize()
    global sio

    background_thread = Thread(target=background_updater)
    background_thread.start()

    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/data", DataHandler),
        (r"/rooms", RoomsHandler),
        (r"/socket.io/", socketio.get_tornado_handler(sio)),
    ])

    app.listen(8085)

    await asyncio.Event().wait()


if __name__ == '__main__':
    asyncio.run(main())
