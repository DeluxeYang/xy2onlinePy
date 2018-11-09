class Component:
    """
    GameObject 的组件

    需重写的方法包括:

    early_update(self, data=None)

    update(self, data=None)

    late_update(self, data=None)

    draw(self, screen=None)

    late_draw(self, screen=None)

    handle_message(self, name=None, value=None)

    还有其他所有事件方法

    on_something(event)

    ****
    """
    def __init__(self):
        self.state = None

    def register(self, state):
        self.state = state

        self.state.components.append(self)

        method_list = [func for func in dir(self) if callable(getattr(self, func)) and func[:1] != "_"]
        event_flag = False
        do_not_register = False
        for method_name in method_list:
            try:
                getattr(self, method_name)()
            except NotImplementedError:
                do_not_register = True
            except Exception:
                pass
            finally:
                if not do_not_register:
                    if method_name == "update":
                        self.state.update_components.append(self)
                    elif method_name == "draw":
                        self.state.draw_components.append(self)
                    elif method_name[:2] == "on" and not event_flag:
                        self.state.event_components.append(self)
                        event_flag = True
                do_not_register = False

    def handle_event(self, event):
        if hasattr(self, "on_" + event.name):  # 如果self有该事件的处理方法
            getattr(self, "on_" + event.name)(event)  # 则处理

    def early_update(self, data=None):
        raise NotImplementedError

    def update(self, data=None):
        raise NotImplementedError

    def late_update(self, data=None):
        raise NotImplementedError

    def draw(self, screen=None):
        raise NotImplementedError

    def late_draw(self, screen=None):
        raise NotImplementedError

    def _handle_message(self, name=None, value=None):
        if hasattr(self, name):
            self.__setattr__(name, value)
