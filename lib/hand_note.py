#
# class T:
#     def __init__(self, a):
#         self.__setattr__("on_a", a)
#
#     def handle_event(self, name):
#         return hasattr(self, "on_"+name)
#
#     def on_q(self):
#         return "123"
#
# t = T(1)
# print()
# print(t.handle_event("a"))
#
# l = []
# l.insert(0,9)
# l.insert(0,8)
# print(l)
import asyncio
from utils.map_client_asyncio import MapClient

mc = MapClient("localhost", 8001)

loop = asyncio.get_event_loop()

loop.create_task(mc.connect(loop))

mc.send({"request": "deluxe"})
mc.send({"request": "dawn"})
mc.send({"request": "?"})


loop.run_forever()

loop.close()
