class Mask:
    def __init__(self, rect, mask, collision_mask=None):
        self.rect = rect
        self.mask = mask
        self.collision_mask = collision_mask

    def destroy(self):
        self.rect = None
        self.mask = None
        self.collision_mask = None
