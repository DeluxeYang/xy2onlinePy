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

        self.signals = ["mouse_left_down", "mouse_right_down", "transfer"]
        self.register()

    def interact(self, event):
        if event.signal == "mouse_left_down":
            pass
        elif event.signal == "mouse_right_down":
            print("right")

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


