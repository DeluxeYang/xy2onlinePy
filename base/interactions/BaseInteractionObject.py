import pygame
from base.events import event_manager


class BaseInteractionObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.signals = []
        self.is_shown = True
        self.level = 0

    def register(self):
        event_manager.add_object(self, self.signals)

    def interact(self, event):
        """
        This method has to be implemented by inherited classes. Its
        signature matches the basic requirements of the EventManager
        class.
        """
        raise NotImplementedError

    def update(self, data):
        """
        This method has to be implemented by inherited classes. Its
        signature matches the basic requirements of the EventManager
        class.
        """
        raise NotImplementedError
