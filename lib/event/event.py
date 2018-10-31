class Event:
    def __init__(self, **kwargs):
        if "name" not in kwargs:
            raise KeyError("Event must have a 'name'.")
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        self.handled = False


events = {
    12: "quit",
    5: {1: "mouse_left_down",  # MOUSE BUTTON DOWN = 5
        2: "mouse_mid_down",
        3: "mouse_right_down",
        4: "mouse_wheel_forward_down",
        5: "mouse_wheel_backward_down"},
    6: {1: "mouse_left_up",  # MOUSE BUTTON UP = 6
        2: "mouse_mid_up",
        3: "mouse_right_up",
        4: "mouse_wheel_forward_up",
        5: "mouse_wheel_backward_up"},
    4: "mouse_motion"
}