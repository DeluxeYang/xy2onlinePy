class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    x = property(get_x, set_x)

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    y = property(get_y, set_y)

    def __str__(self):
        return "x: {:.0f}".format(self._x) + ", y: {:.0f}".format(self._y)


if __name__ == "__main__":
    p = Point(2, 2)
    print(p)
