class Role:
    def __init__(self, *args, **kwargs):
        self.account = kwargs['account']
        self.res = kwargs['res']

        self.id = kwargs['id']
        self.name = kwargs['name']

        self.level = kwargs['level']
        self.reborn = kwargs['reborn']

        self.map = kwargs['map']
        self.x = kwargs['x']
        self.y = kwargs['y']
