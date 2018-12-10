from core.world.director import director


class Scene:
    def __init__(self):
        self.director = director
        self.layers = []  # layer层，其z序固定，由近及远，z越大则越远

        self.title = ""
        self.resolution = (800, 600)

    def handle_event(self, event):
        if hasattr(self, "on_" + event.name):  # 如果self有该事件的处理方法
            getattr(self, "on_" + event.name)(event)  # 则处理
        if not event.handled:  # 如果该事件没有被handle & obj对象有Children属性
            for layer in self.layers:  # 则循环遍历每个layer
                layer.handle_event(event)  # 调用其handle_event方法
                if event.handled:  # 如果被handle则退出
                    break
    """
    layer 更新流
        event   early   update  late    draw
        
    ui    \      \         /     \        /
    shape  \      \       /       \      /
    map     \      \     /         \    / 
    """
    def update(self, data):
        for layer in self.layers:  # 遍历每个layer  early_update
            layer.early_update(data)
        for layer in self.layers[::-1]:  # 遍历每个layer  update
            layer.update(data)
        for layer in self.layers:  # 遍历每个layer  late_update
            layer.late_update(data)

    def draw(self, screen):
        for layer in self.layers[::-1]:  # 逆序遍历每个layer
            layer.draw(screen)

    def add_layer(self, layer):
        self.layers.append(layer)

    def enter(self, director):
        director.title = self.title
        director.resolution = self.resolution

    def exit(self, director):
        pass
