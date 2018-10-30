class Event:
    def __init__(self, **kwargs):
        if "name" not in kwargs:
            raise KeyError("Event must have a 'name'.")
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        self.handled = False


events = {
    12: "quit",
}