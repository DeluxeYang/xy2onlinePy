class State:
    def __init__(self):
        self.game_object = None

    def register(self, obj):
        self.game_object = obj

    def update(self, data):
        pass

    def draw(self, screen):
        pass

    def late_draw(self, screen):
        pass