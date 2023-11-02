import logging
import requests
import base64
import ssl
import asyncio
import websockets
logging.getLogger().setLevel(logging.INFO)


class METHOD():
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"
    SUBSCRIBE = "SUBSCRIBE"


class WS_OPCODE:
    WELCOME = "0"
    PREFIX = "1"
    CALL = "2"
    CALLRESULT = "3"
    CALLERROR = "4"
    SUBSCRIBE = "5"
    UNSUBSCRIBE = "6"
    PUBLISH = "7"
    EVENT = "8"


class LCU_Client(requests.Session):
    BASE_URL = "https://127.0.0.1"
    WSS_URL = "wss://127.0.0.1"
    LOCKFILE_PATH = "C:\Riot Games\League of Legends\lockfile"

    def __init__(self):
        with open(self.LOCKFILE_PATH, "r") as f:
            lcu_auth_info = f.read().split(":")
            self.pname = lcu_auth_info[0]
            self.pid = lcu_auth_info[1]
            self.port = lcu_auth_info[2]
            self.password = lcu_auth_info[3]
            self.protocol = lcu_auth_info[4]
        super().__init__()
        self.ssl_cert = ssl.create_default_context(
            purpose=ssl.Purpose.SERVER_AUTH, capath="./", cafile="./riotgames.pem")
        self.basic_auth = base64.b64encode(
            bytes(f"riot:{self.password}", "utf-8")).decode("utf-8")
        if not self.initialize_lcu_session():
            logging.log(logging.ERROR, "Failed to initialize LCU session")
            exit(1)
        self.socket_status = False
        self.mq = asyncio.Queue()

    def initialize_lcu_session(self) -> bool:
        self.auth = ("riot", self.password)
        self.verify = "./riotgames.pem"
        lcu_status = self.get(
            f"{self.BASE_URL}:{self.port}/lol-service-status/v1/lcu-status")

        # display request results in formattd json
        logging.log(logging.INFO, "LCU Status: %s" % lcu_status.status_code)
        return lcu_status.status_code == 200

    def __call__(self, method: str, endpoint: str, data=None):
        if method != "SUBSCRIBE":
            logging.log(logging.INFO, f" {method} {endpoint}")
        match method:
            case METHOD.POST:
                return self.post(f"{self.BASE_URL}:{self.port}{endpoint}")
            case METHOD.GET:
                return self.get(f"{self.BASE_URL}:{self.port}{endpoint}")
            case METHOD.PUT:
                if data is None:
                    logging.log(logging.ERROR, "PUT request requires data")
                return self.put(f"{self.BASE_URL}:{self.port}{endpoint}", data=data)
            case METHOD.DELETE:
                return self.delete(f"{self.BASE_URL}:{self.port}{endpoint}")
            case METHOD.SUBSCRIBE:
                if self.socket_status == False:
                    self.socket_status = True
                    self.__start_ws(endpoint)
            case _:
                logging.log(logging.ERROR, "Invalid HTTP method")
                return requests.Response()

    def __start_ws(self, endpoint):
        asyncio.create_task(self.__wss_handler(endpoint))

    async def __wss_handler(self, endpoint):
        async with websockets.connect(f"wss://riot:{self.password}@127.0.0.1:{self.port}", ssl=self.ssl_cert) as websocket:
            await websocket.send(f"[{WS_OPCODE.SUBSCRIBE}, \"{endpoint}\"]")
            try:
                while True:
                    message = await websocket.recv()
                    await self.mq.put(message)
            except websockets.ConnectionClosed:
                print("Connection was closed")
            except Exception as e:
                print(f"An error occurred: {e}")
