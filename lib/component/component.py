class Component:
    def __init__(self):
        self.game_object = None

    def start(self, obj):
        self.game_object = obj

    def handle_event(self, event):
        if hasattr(self, "on_" + event.name):  # 如果self有该事件的处理方法
            getattr(self, "on_" + event.name)(event)  # 则处理

    def early_update(self):
        pass

    def update(self, dt):
        pass

    def late_update(self):
        pass

    def draw(self, screen):
        pass

    def handle_message(self, name, value):
        # if hasattr(self, name):
        #     self.__setattr__(name, value)
        # # 如果截断信息则返回True
        pass
