from base.events.Event import PredefinedEvents


class EventManager:
    """
    时间分发管理器
    """
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.queues = {}
        self._grabber = None
        self.event_grabber = None

    def __len__(self):
        """
        返回各个事件的列队总长度
        :return:
        """
        length = 0
        event_list = self.queues.keys()
        for signal in event_list:
            length += len(self.queues[signal])
        return length

    def add_object(self, obj, signals):
        """
        添加一个交互对象
        :param obj:
        :param signals:
        :return:
        """
        self._verify_obj(obj)  # 验证是否是可交互对象
        for key in signals:
            self.queues.setdefault(key, []).append(obj)

    def add_high_priority_object(self, obj, *signals):
        """
        添加高优先级交互对象
        :param obj:
        :param signals:
        :return:
        """
        self._verify_obj(obj)  # 验证是否是可交互对象
        for key in signals:
            self.queues.setdefault(key, []).insert(0, obj)

    def remove_object(self, obj, *signals):
        """
        移除交互对象
        :param obj:
        :param signals:
        :return:
        """
        if signals:
            event_list = signals
        else:
            event_list = self.queues.keys()

        for signal in event_list:
            if obj in self.queues[signal]:
                self.queues[signal].remove(obj)

    def clear(self):
        """
        清空对象管理器
        :return:
        """
        self.event_grabber = None
        self.queues = {}

    def grab_events(self, obj):
        self._verify_obj(obj)
        self._grabber = obj

    def emit(self, key, data):
        _event = PredefinedEvents[key]
        _event.set_data(data)
        self.emit_event(_event)

    def emit_event(self, event):
        objects_of_this_event_list = self.queues.get(event.signal, [])
        objects_of_this_event_list.sort(key=lambda _obj: _obj.level, reverse=True)  # 排序
        for obj in objects_of_this_event_list:
            obj.interact(event)
            if event.handled:
                break

    @staticmethod
    def _verify_obj(obj):
        if not hasattr(obj, "interact") or not callable(obj.interact):
            raise AttributeError("interact() method not found in object %s" % obj)

