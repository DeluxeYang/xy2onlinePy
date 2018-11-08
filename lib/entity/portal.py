from .game_object import GameObject


class Portal(GameObject):
    def __init__(self):
        super().__init__()
        self.position = (0, 0)
        self.target_map_id = ""
        self.target_position = (0, 0)
        self.is_show = True
        self.wdf = ""
        self.hash = ""
