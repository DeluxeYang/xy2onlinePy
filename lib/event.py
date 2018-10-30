class Event:
    def __init__(self, **kwargs):
        if "name" not in kwargs:
            raise KeyError("Event must have a 'name'.")
        for key, value in kwargs:
            self.__setattr__(key, value)
        self.handled = False

    @property
    def handled(self):
        return self.handled

    @handled.setter
    def handled(self, value):
        self.handled = value

events = {
    12: "quit",
}