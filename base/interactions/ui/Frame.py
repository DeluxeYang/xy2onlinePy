from base.interactions.BaseInteractionObject import BaseInteractionObject
from base.animations.ItemAnimation import ItemAnimation


class Frame(BaseInteractionObject):
    def __init__(self, address, position):
        super().__init__()
        self.ani = ItemAnimation(address)
        self.position = position
        self.is_shown = False

    def interact(self, event):
        pass

    def update(self, data):
        pass
