from core.entity.game_object import GameObject
from game.map_ip.map import Map


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
        self.children = []


class MapLayer(Layer):
    this_frame_children = []

    def early_update(self, context):
        self.this_frame_children = []
        for child in self.children:
            if context["collision_window"].collidepoint(child.x, child.y)\
                    or isinstance(child, Map):
                self.this_frame_children.append(child)
                child.early_update(context)

    def update(self, context):
        for child in self.this_frame_children:
            child.update(context)

    def late_update(self, context):
        for child in self.this_frame_children:
            child.late_update(context)

    def draw(self, screen):
        self.this_frame_children.sort(key=lambda obj: obj.z, reverse=True)  # 按GameObject的Y坐标从小到大，也即从游戏中由远即近的渲染
        for child in self.this_frame_children:
            child.draw(screen)
        for child in self.this_frame_children:
            child.late_draw(screen)


class ShapeLayer(Layer):
    this_frame_children = []

    def early_update(self, context):
        self.this_frame_children = []
        for child in self.children:
            if context["collision_window"].collidepoint(child.x, child.y):
                self.this_frame_children.append(child)
                child.early_update(context)

    def update(self, context):
        for child in self.this_frame_children:
            child.update(context)

    def late_update(self, context):
        for child in self.this_frame_children:
            child.late_update(context)

    def draw(self, screen):
        self.this_frame_children.sort(key=lambda obj: obj.y)  # 按GameObject的Y坐标从小到大，也即从游戏中由远即近的渲染
        for child in self.this_frame_children:
            child.draw(screen)
        for child in self.this_frame_children:
            child.late_draw(screen)


class UILayer(Layer):
    def __init__(self):
        super().__init__()
        self.z_index = 0

    def draw(self, screen):
        self.children.sort(key=lambda obj: obj.z)  # 按GameObject的Z坐标从大到小，也即从远即近的渲染
        for child in self.children:
            child.draw(screen)

    def lose_focus(self):
        for child in self.children:
            child.lose_focus()

    def handle_event(self, event):
        if hasattr(self, "on_" + event.name):  # 如果self有该事件的处理方法
            getattr(self, "on_" + event.name)(event)  # 则处理
        if not event.handled:  # 如果该事件没有被handle & obj对象有Children属性
            temp_children = sorted(self.children, key=lambda obj: obj.z, reverse=True)
            for child in temp_children:  # 则循环遍历每个layer
                child.handle_event(event)  # 调用其handle_event方法
                if event.handled:  # 如果被handle则退出
                    break

    def add_game_object(self, game_object):
        if isinstance(game_object, GameObject):
            game_object.z = self.z_index
            self.z_index += 1
            self.children.append(game_object)
