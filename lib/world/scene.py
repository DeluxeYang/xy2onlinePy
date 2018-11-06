from lib.world.layer import map_layer_factory, shape_layer_factory, ui_layer_factory

class Scene:
    def __init__(self, map_id, director):
        self.director = director
        self.layers = []  # layer层，其z序固定，由近及远，z越大则越远

        self.map_id = map_id
        self.title = ""
        self.resolution = (800, 600)

    def load(self):
        data = self.director.network_client.get_scene(self.map_id)
        self.title = data["title"]
        self.resolution = data["resolution"]

    def handle_event(self, event):
        # if hasattr(self, "on_" + event.name):  # 如果self有该事件的处理方法
        #     getattr(self, "on_" + event.name)(event)  # 则处理
        if not event.handled:  # 如果该事件没有被handle & obj对象有Children属性
            for layer in self.layers:  # 则循环遍历每个layer
                layer.handle_event(event)  # 调用其handle_event方法
                if event.handled:  # 如果被handle则退出
                    break

    def update(self, data):
        reversed_layers = self.layers[::-1]
        for layer in reversed_layers:  # 遍历每个layer  early_update
            layer.early_update(data)
        for layer in reversed_layers:  # 遍历每个layer  update
            layer.update(data)
        for layer in reversed_layers:  # 遍历每个layer  late_update
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


def scene_factory(map_id, director):
    scene = Scene(map_id, director)
    scene.load()

    ui_layer = ui_layer_factory(director.network_client)  # ui层，最近
    scene.add_layer(ui_layer)

    shape_layer = shape_layer_factory(director.network_client)
    scene.add_layer(shape_layer)

    map_layer = map_layer_factory(map_id, director.map_client, director.network_client)
    scene.add_layer(map_layer)

    return scene
