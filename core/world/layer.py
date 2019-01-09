from core.entity.game_object import GameObject
from game.map.map import map_factory
from game.character.character import character_factory


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

    def early_update(self, context):
        for child in self.children:
            child.early_update(context)

    def update(self, context):
        for child in self.children:
            child.update(context)

    def late_update(self, context):
        for child in self.children:
            child.late_update(context)

    def draw(self, screen):
        pass

    def add_game_object(self, game_object):
        if isinstance(game_object, GameObject):
            self.children.append(game_object)

    def destroy(self):
        for child in self.children:
            child.destroy()
        del self


class MapLayer(Layer):
    def draw(self, screen):
        self.children.sort(key=lambda obj: obj.z, reverse=True)  # 按GameObject的Z坐标从大到小，也即从远即近的渲染
        for child in self.children:
            child.draw(screen)


class ShapeLayer(Layer):
    def draw(self, screen):
        self.children.sort(key=lambda obj: obj.y)  # 按GameObject的Y坐标从小到大，也即从游戏中由远即近的渲染
        for child in self.children:
            child.draw(screen)
        for child in self.children:
            child.late_draw(screen)


class UILayer(Layer):
    def draw(self, screen):
        self.children.sort(key=lambda obj: obj.z, reverse=True)  # 按GameObject的Z坐标从大到小，也即从远即近的渲染
        for child in self.children:
            child.draw(screen)

    def lose_focus(self):
        for child in self.children:
            child.lose_focus()