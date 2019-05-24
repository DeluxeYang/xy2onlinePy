from core.ui.state.static_ui_state import StaticUIState
from core.ui.state.animated_ui_state import AnimatedUIState
from settings import ResMargin, logger

# map_click = res_manager.get_res(wdf_name="gires.wdf", _hash="0x1C374751")


class MouseState(AnimatedUIState):
    res_index = "normal"


class MouseNormalState(MouseState):
    res_index = "normal"


class MousePressState(MouseState):
    res_index = "press"


class MouseDisabledState(MouseState):
    res_index = "disabled"
