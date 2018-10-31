import asyncio

from utils.map_x import MapX
from settings import ResourcePort


class MapServer:
    def __init__(self):
        self.server = None
        self.reader = None
        self.writer = None

        self.map_x_pool = {}

    async def map_quest_handler(self, reader, writer):
        self.reader = reader
        self.writer = writer

        data = await self.reader.read(100)
        request_data = eval(data.decode())

        print(request_data)

        if request_data["request"] == "map_info":
            await self.get_map_info(request_data["map_id"])
        elif request_data["request"] == "map_unit":
            await self.get_map_unit(request_data["map_id"], request_data["unit_num"])
        elif request_data["request"] == "find_path":
            await self.get_path(request_data["map_id"], request_data["current"],
                          request_data["target"], request_data["is_running"])
        writer.close()

    async def get_map_info(self, map_id):
        map_x = self._get_map_x(map_id)
        send_data = {
            'event': "receive_map_info",
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
        self.writer.write(str(send_data).encode("utf-8"))
        await self.writer.drain()

    async def get_map_unit(self, map_id, unit_num):
        map_x = self._get_map_x(map_id)
        await asyncio.sleep(0.1)
        jpeg, masks = map_x.read_unit(unit_num)
        send_data = {
            'event': "receive_map_info",
            'map_id': map_x.map_id,
            'jpeg': jpeg,
            'masks': masks
        }
        self.writer.write(str(send_data).encode("utf-8"))
        await self.writer.drain()

    async def get_path(self, map_id, current, target, is_running):
        map_x = self._get_map_x(map_id)
        path_list = map_x.find_path(current, target)
        send_data = {
            'action': "receive_path_list",
            'path_list': path_list,
            'is_running': is_running
        }
        self.writer.write(str(send_data).encode("utf-8"))
        await self.writer.drain()

    def _get_map_x(self, map_id):
        if map_id not in self.map_x_pool:
            self.map_x_pool[map_id] = MapX(map_id)
        return self.map_x_pool[map_id]

    async def loop(self, host, port):
        self.server = await asyncio.start_server(self.map_quest_handler, host, port)

        client_address = self.server.sockets[0].getsockname()
        print(f'Serving on {client_address}')

        async with self.server:
            await self.server.serve_forever()

map_server = MapServer()
asyncio.run(map_server.loop("localhost", int(ResourcePort)))
