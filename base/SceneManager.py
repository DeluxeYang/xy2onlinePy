from base.world.Scene import Scene
from base.interactions.BaseInteractionObject import BaseInteractionObject
from base.events import event_manager


class SceneManager(BaseInteractionObject):
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.pool = {}
        self.current = None

        self.level = 0
        self.signals = ["mouse_left_down", "mouse_right_down", "transfer"]
        self.register()

    def interact(self, event):
        map_client = event.data["map_client"]
        me = event.data["me"]
        scene = event.data["scene"]
        if event.signal == "mouse_left_down":
            map_client.find_path(scene.map_info["map_file"], me.current,
                                 scene.get_map_xy(event.data["mouse_pos"]), False)
        elif event.signal == "mouse_right_down":
            map_client.find_path(scene.map_info["map_file"], me.current,
                                 scene.get_map_xy(event.data["mouse_pos"]), True)

    def update(self, data):
        masks = []
        if self.current.inited:
            self.current.quest(data["map_client"])  # QUEST
            masks = self.current.update()  # UPDATE
        return masks

    def init_scene(self, map_client, map_id):
        if map_id not in self.pool:
            self.pool[map_id] = Scene(map_id)
            self.pool[map_id].get_map(map_client)
        self.current = self.pool[map_id]

scene_manager = SceneManager()


