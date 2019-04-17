from res.characters import characters


class Role:
    def __init__(self, name):
        self.name = name
        self.res = None

        self.level = None
        self.reborn = None

        self.race = None
        self.version = None
        self.character = None

        self.map_id = None
        self.x = None
        self.y = None

    def specify(self, level, reborn,
                race, version, character,
                map_id, x, y):
        self.res = characters[race][version][character]

        self.level = level
        self.reborn = reborn

        self.race = race
        self.version = version
        self.character = character

        self.map_id = map_id
        self.x = x
        self.y = y

    def get_xy(self):
        return self.x, self.y

    def set_xy(self, x, y):
        self.x = x
        self.y = y
