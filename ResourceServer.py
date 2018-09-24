from time import sleep
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from utils.MAPX import MapX
from Settings import Resource_Port


class ResourceChannel(Channel):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.MapX_Pool = {}

    def Network(self, data):
        pass

    def Network_get_map_info(self, data):
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
        self.Send(send_data)

    def Network_get_map_unit(self, data):
        map_x = self._get_map_x(data)
        unit_num = data["unit_num"]
        jpeg, masks = map_x.read_unit(unit_num)
        send_data = {
            'action': "receive_map_unit",
            'map_id': map_x.map_id,
            'unit_num': unit_num,
            'jpg': jpeg,
            'masks': masks
        }
        self.Send(send_data)

    def Network_find_path(self, data):
        map_x = self._get_map_x(data)
        path_list = map_x.find_path(data["current"], data["target"])
        send_data = {
            'action': "receive_path_list",
            'map_id': map_x.map_id,
            'path_list': path_list,
            'is_running': data["is_running"]
        }
        self.Send(send_data)

    def _get_map_x(self, data):
        map_path = data["map_file"]
        if map_path not in self.MapX_Pool:
            self.MapX_Pool[map_path] = MapX(map_path)
        return self.MapX_Pool[map_path]


class ResourceServer(Server):
    channelClass  = ResourceChannel

    def __init__(self, *args, **kwargs):
        self.id = 0
        Server.__init__(self, *args, **kwargs)
        print('Server launched')

    def Connected(self, channel, addr):
        print('new connection:', channel)

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)


host, port = "localhost", Resource_Port
resource_server = ResourceServer(localaddr=(host, int(port)))
while True:
    resource_server.Launch()