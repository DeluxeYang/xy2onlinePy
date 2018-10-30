import asyncio


from settings import ResourcePort


async def map_quest_handler(reader, writer):
    data = await reader.read(100)
    request = data.decode()

    print(f"Received {request!r}")

    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()


async def map_server(host, port):
    server = await asyncio.start_server(map_quest_handler, host, port)

    client_address = server.sockets[0].getsockname()
    print(f'Serving on {client_address}')

    async with server:
        await server.serve_forever()

#
#
# class ResourceChannel(Channel):
#
#     def __init__(self, *args, **kwargs):
#         Channel.__init__(self, *args, **kwargs)
#         self.MapX_Pool = {}
#
#     def Network(self, data):
#         pass
#
#     def Network_get_map_info(self, data):
#         """
#         地图信息获取，直接返回
#         :param data:
#         :return:
#         """
#         map_x = self._get_map_x(data)
#         send_data = {
#             'action': "receive_map_info",
#             'map_id': map_x.map_id,
#             'map_type': map_x.map_type,
#             'map_width': map_x.map_width,
#             'map_height': map_x.map_height,
#             'unit_width': 320,
#             'unit_height': 240,
#             'col': map_x.col,
#             'row': map_x.row,
#             'n': map_x.n,
#             'coordinate': map_x.coordinate
#         }
#         self.Send(send_data)
#
#     def Network_get_map_unit(self, data):
#         """
#         地图单元读取，放入队列，轮询读取
#         :param data:
#         :return:
#         """
#         map_x = self._get_map_x(data)
#         task = Task(self, map_x, data)
#         queue.put(task)
#
#     def Network_find_path(self, data):
#         """
#         获取行走路径，直接返回
#         :param data:
#         :return:
#         """
#         map_x = self._get_map_x(data)
#         path_list = map_x.find_path(data["current"], data["target"])
#         send_data = {
#             'action': "receive_path_list",
#             'path_list': path_list,
#             'is_running': data["is_running"]
#         }
#         self.Send(send_data)
#
#     def _get_map_x(self, data):
#         map_path = data["map_file"]
#         if map_path not in self.MapX_Pool:
#             self.MapX_Pool[map_path] = MapX(map_path)
#         return self.MapX_Pool[map_path]
#
#
# class ResourceServer(Server):
#     channelClass  = ResourceChannel
#
#     def __init__(self, *args, **kwargs):
#         self.id = 0
#         Server.__init__(self, *args, **kwargs)
#         self.clients = WeakKeyDictionary()
#         print('Server launched')
#
#     def Connected(self, channel, addr):
#         self.add_client(channel)
#
#     def add_client(self, client):
#         print("New Player" + str(client.addr))
#         self.clients[client] = True


asyncio.run(map_server("localhost", int(ResourcePort)))