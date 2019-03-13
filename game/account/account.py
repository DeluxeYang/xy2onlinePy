class Account:
    def __init__(self, account, roles_num):
        self.account = account
        self.roles_num = roles_num
        self.roles = {}

    def add_role(self, role):
        self.roles[role.name] = role
