from lib.entity.game_object import GameObject
from lib.entity.map import map_factory

class Layer:
    def __init__(self):
        self.children = []  # GameObject列表

    def handle_event(self, event):
        if hasattr(self, "on_" + event.name):  # 如果self有该事件的处理方法
            getattr(self, "on_" + event.name)(event)  # 则处理
        if not event.handled:  # 如果该事件没有被handle & obj对象有Children属性
            for child in self.children:  # 则循环遍历每个layer
                child.handle_event(event)  # 调用其handle_event方法
                if event.handled:  # 如果被handle则退出
                    break

    def update(self, dt):
        for child in self.children:
            child.update(dt)

    def draw(self, screen):
        pass

    def add_game_object(self, game_object):
        if isinstance(game_object, GameObject):
            self.children.append(game_object)

class MapLayer(Layer):
    def draw(self, screen):
        self.children.sort(key=lambda obj: obj.z, reverse=True)  # 按GameObject的Z坐标从大到小，也即从远即近的渲染
        for child in self.children:
            child.draw(screen)

def map_layer_factory(map_id, map_client, network_client):
    map_layer = MapLayer()
    _map = map_factory(map_id, map_client, network_client)
    map_layer.add_game_object(_map)
    return map_layer

class ShapeLayer(Layer):
    def draw(self, screen):
        self.children.sort(key=lambda obj: obj.y)  # 按GameObject的Y坐标从小到大，也即从游戏中由远即近的渲染
        for child in self.children:
            child.draw(screen)
        for child in self.children:
            child.late_draw(screen)

def shape_layer_factory(network_client):
    shape_layer = ShapeLayer()
    return shape_layer

class UILayer(Layer):
    def draw(self, screen):
        self.children.sort(key=lambda obj: obj.z, reverse=True)  # 按GameObject的Z坐标从大到小，也即从远即近的渲染
        for child in self.children:
            child.draw(screen)

def ui_layer_factory(network_client):
    ui_layer = UILayer()
    return ui_layer