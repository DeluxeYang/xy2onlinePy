from res.Characters import characters
from base.animations.role_animation import RoleAnimation


class Role:
    def __init__(self, race, version, _id):
        super().__init__()
        self.res_index = characters[race][version][_id]

        self.stand_status = 0

        self.run_ani = None
        self.walk_ani = None
        self.stand_ani = None
        self.stand_action_ani = None

    def run(self, other_masks, left_top, world_pc, direction, ticks, rate=100):
        if not self.run_ani:
            self.run_ani = RoleAnimation(self.res_index["run"])
        self.run_ani.update(other_masks, world_pc, direction, ticks, rate)
        # self.run_ani.draw(left_top, world_pc, True)
        return self.run_ani

    def walk(self, other_masks, left_top, world_pc, direction, ticks, rate=100):
        if not self.walk_ani:
            self.walk_ani = RoleAnimation(self.res_index["walk"])
        self.walk_ani.update(other_masks, world_pc, direction, ticks, rate)
        # self.walk_ani.draw(left_top, world_pc)
        return self.walk_ani

    def stand(self, other_masks, left_top, world_pc, direction, ticks, rate=100):
        if not self.stand_ani:
            self.stand_ani = RoleAnimation(self.res_index["stand"][0])
            self.stand_action_ani = RoleAnimation(self.res_index["stand"][1])
        if self.stand_status < 3:
            one_loop = self.stand_ani.update(other_masks, world_pc, direction, ticks, rate)
            # self.stand_ani.draw(left_top, world_pc)
            if one_loop:
                self.stand_status += 1
            return self.stand_ani
        else:
            one_loop = self.stand_action_ani.update(other_masks, world_pc, direction, ticks, rate)
            # self.stand_action_ani.draw(left_top, world_pc)
            if one_loop:
                self.stand_status = 0
            return self.stand_action_ani
