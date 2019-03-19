class Account:
    def __init__(self, account, roles_num):
        self.account = account

        self.roles_num = roles_num
        self.roles = {}

        self.current_role = None
        self.current_role_name = ''

    @property
    def current_role(self):
        self.current_role = self.roles[self.current_role_name]
        return self.current_role

    @current_role.setter
    def current_role(self, role_name):
        self.current_role_name = role_name
        self.current_role = self.roles[self.current_role_name]

    def add_role(self, role):
        self.roles[role.name] = role


