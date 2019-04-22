from time import sleep, time
from weakref import WeakKeyDictionary
from queue import Queue

from core.network.channel import Channel
from core.network.server import Server

from utils.map_x import MapX
from settings import ResourcePort

queue = Queue()


class MapUnitReadTask:
    """
    地图读取任务包装
    """
    def __init__(self, channel, map_x, data):
        self.channel = channel
        self.data = data
        self.map_x = map_x

    def run(self):
        unit_num = self.data["unit_num"]
        jpeg, masks = self.map_x.read_unit(unit_num)
        send_data = {
            'action': "receive_map_unit",
            'map_id': self.map_x.map_id,
            'unit_num': unit_num,
            'jpeg': jpeg,
            'masks': masks
        }
        self.channel.transmit(send_data)


class MapServerChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.map_x_pool = {}

    def network(self, data):
        print(data)

    def network_request_map_info(self, data):
        """
        地图信息获取，直接返回
        :param data:
        :return:
        """
        map_x = self._get_map_x(data)
        send_data = {
            'action': "receive_map_info",
            'map_id': map_x.map_id,
            'map_type': map_x.map_type,
            'map_width': map_x.map_width,
            'map_height': map_x.map_height,
            'unit_width': 320,
            'unit_height': 240,
            'col': map_x.col,
            'row': map_x.row,
            'n': map_x.n,
            'coordinate': map_x.coordinate
        }
        self.transmit(send_data)

    def network_request_map_unit(self, data):
        """
        地图单元读取，放入队列，轮询读取
        :param data:
        :return:
        """
        map_x = self._get_map_x(data)
        jpeg, masks = map_x.read_unit(data["unit_num"])
        send_data = {
            'action': "receive_map_unit",
            'map_id': map_x.map_id,
            'unit_num': data["unit_num"],
            'jpeg': jpeg,
            'masks': masks
        }
        self.transmit(send_data)

    def network_request_find_path(self, data):
        """
        获取行走路径，直接返回
        :param data:
        :return:
        """
        map_x = self._get_map_x(data)
        path_list = map_x.find_path(data["current"], data["target"])
        send_data = {
            'action': "receive_path_list",
            'path_list': path_list,
            'is_running': data["is_running"]
        }
        self.transmit(send_data)

    def _get_map_x(self, data):
        map_path = data["map_file"]
        if map_path not in self.map_x_pool:
            self.map_x_pool[map_path] = MapX(map_path)
        return self.map_x_pool[map_path]


class MapServer(Server):
    channel_class = MapServerChannel

    def __init__(self, *args, **kwargs):
        self.id = 0
        Server.__init__(self, *args, **kwargs)
        self.clients = WeakKeyDictionary()
        print('Server launched')

    def on_connected(self, channel, address):
        print("New Map Client" + str(address))
        self.add_client(channel)

    def add_client(self, client):
        self.clients[client] = True


map_server = MapServer(local_address=("localhost", int(ResourcePort)))
while True:
    map_server.pump()
    if not queue.empty():  # 检测有没有地图单元读取任务
        task = queue.get(block=False)
        task.run()
    sleep(0.001)
