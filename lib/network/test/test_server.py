from weakref import WeakKeyDictionary
from queue import Queue
from time import sleep

from lib.network.server import Server
from lib.network.channel import Channel

queue = Queue()  # 地图单元读取队列

class TChannel(Channel):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    @staticmethod
    def network(data):
        print(data)

class TServer(Server):
    channel_class = TChannel
    def __init__(self, *args, **kwargs):
        self.id = 0
        super().__init__(self, *args, **kwargs)
        self.clients = WeakKeyDictionary()
        print('Server launched')

    def on_connected(self, channel, address):
        self.add_client(channel)
        print(address)

    def add_client(self, client):
        print("New Player" + str(client.addr))
        self.clients[client] = True

host, port = "localhost", 9999
resource_server = TServer(local_address=(host, int(port)))

while True:
    resource_server.pump()
    if not queue.empty():  # 检测有没有地图单元读取任务
        task = queue.get(block=False)
        task.run()
    sleep(0.0001)