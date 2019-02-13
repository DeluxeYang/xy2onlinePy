class Account:
    def __init__(self, account):
        self.account = account
        self.role_num = 0
        self.roles = []

    def accept_roles(self, roles):
        self.roles += roles

    def add_role(self):
        pass
