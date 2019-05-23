class Account:
    def __init__(self, account):
        self.account = account

        self.roles_num = 0
        self.roles = {}

        self.main_role = None
        self.main_role_id = ''

    def add_role(self, role):
        self.roles_num += 1
        self.roles[role.id] = role

    def set_main_role(self, _id):
        self.main_role_id = _id
        self.main_role = self.roles[_id]
        for role_name, role in self.roles.items():
            role.is_main_role = False
        self.main_role.is_main_role = True

    def get_main_role(self):
        return self.main_role

    def empty_roles(self):
        self.main_role = None
        self.main_role_id = ''
        self.roles = {}
        self.roles_num = 0


