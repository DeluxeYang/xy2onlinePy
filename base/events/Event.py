class Event:
    """
    Event事件包装
    """

    __slots__ = ["signal", "data", "handled"]

    def __init__(self, signal):
        self.signal = signal
        self.data = None
        self.handled = False

    def set_data(self, data):
        self.data = data


PredefinedEvents = {
    "mouse_left_down": Event("mouse_left_down"),
    "mouse_left_up": Event("mouse_left_up"),
    "mouse_mid_down": Event("mouse_mid_down"),
    "mouse_mid_up": Event("mouse_mid_up"),
    "mouse_right_down": Event("mouse_right_down"),
    "mouse_right_up": Event("mouse_right_up"),
    "mouse_motion": Event("mouse_motion"),

    "transfer": Event("transfer"),
    "player_moving": Event("player_moving"),
}
