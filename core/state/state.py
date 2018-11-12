from core.component.component import Component


class State:
    def __init__(self):
        self.game_object = None

        self.components = []
        self.event_components = []
        self.update_components = []
        self.draw_components = []

    def register(self, obj):
        self.game_object = obj

    def add_component(self, component):
        if isinstance(component, Component):
            component.register(self)

    def send_message(self, message, data=None):
        for component in self.components:
            result = component.handle_message(message, data)
            if result is not None:
                return result

    def handle_event(self, event):  # 事件组件处理
        for component in self.event_components:
            component.handle_event(event)

    def early_update(self, data):
        pass

    def update(self, data):  # update 处理
        for component in self.update_components:
            component.update(data)

    def late_update(self, data):
        pass

    def draw(self, screen):  # draw 处理
        for component in self.draw_components:
            component.draw(screen)

    def late_draw(self, screen):
        pass

    def enter(self):
        pass

    def exit(self):
        self.destroy()

    def destroy(self):
        del self


def state_factory(state_class, component_classes):
    state = state_class()
    for component_class in component_classes:
        component = component_class()
        state.add_component(component)
    return state
