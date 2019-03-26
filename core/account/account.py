class Account:
    def __init__(self, account, roles_num):
        self.account = account

        self.roles_num = roles_num
        self.roles = {}

        self.main_role = None
        self.main_role_name = ''

    def add_role(self, role):
        self.roles[role.name] = role

    def set_main_role(self, name):
        self.main_role_name = name
        self.main_role = self.roles[name]

    def get_main_role(self):
        return self.main_role

