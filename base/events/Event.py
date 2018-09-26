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
