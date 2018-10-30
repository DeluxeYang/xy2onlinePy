class EventComponent:
    @staticmethod
    def update(obj, event):
        if hasattr(obj, "on_" + event.name):  # 如果self有该事件的处理方法
            getattr(obj, "on_" + event.name)(event)  # 则处理
        if not event.handled and hasattr(obj, "children"):  # 如果该事件没有被handle & obj对象有Children属性
            for child in obj.children:  # 则循环遍历每个layer
                child.handle_event(event)  # 调用其handle_event方法
                if event.handled:  # 如果被handle则退出
                    break
