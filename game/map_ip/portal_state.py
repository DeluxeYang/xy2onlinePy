from core.state.material_animation_state import MaterialAnimationState
from core.world.director import director


class PortalState(MaterialAnimationState):
    already_sent = False

    def update(self, context):
        super().update(context)

        if not self.already_sent and self.game_object.rect.collidepoint(director.account.get_main_role().get_xy()):
            director.network_client.request(send_data={  # 获取当前主要角色所在场景中的其他玩家
                "action": "jump",
                "account": director.account.account,
                "role_id": director.account.get_main_role().id,
                "role_name": director.account.get_main_role().name,
                "map_version": self.game_object.map_version,
                "map_id": self.game_object.map_id,
                "target_map_id": self.game_object.target_map_id,
                "target_map_version": self.game_object.target_map_version,
                "target_x": self.game_object.target_x,
                "target_y": self.game_object.target_y
            })
            self.already_sent = True
