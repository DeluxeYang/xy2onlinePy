from base.interactions.BaseInteractionObject import BaseInteractionObject
from base.interactions.Player import Player


class PlayerManager(BaseInteractionObject):
    def __init__(self):
        super().__init__()
        self.me = None
        self.others = []

    def interact(self, event):
        pass

    def update(self, data):
        players = [self.me] + self.others
        players.sort(key=lambda p: p.current[1])  # 排序
        for player in players:
            player.update(data)


    def init_data(self, player_list):
        self.others = []
        for player_data in player_list:
            self.others.append(Player(player_data))

    def choose_main_player(self, player_id):
        for i, player in enumerate(self.others):
            if player.id == player_id:
                self.me = self.others.pop(i)
                return

player_manager = PlayerManager()
