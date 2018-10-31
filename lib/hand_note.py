
class T:
    def __init__(self, a):
        self.__setattr__("on_a", a)

    def handle_event(self, name):
        return hasattr(self, "on_"+name)

    def on_q(self):
        return "123"

t = T(1)
print()
print(t.handle_event("a"))

l = []
l.insert(0,9)
l.insert(0,8)
print(l)