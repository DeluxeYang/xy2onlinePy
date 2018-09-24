class PixelCoordinate:
    """
    像素坐标
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0  # 关于地图的绝对像素坐标
        self.y = 0

    def get_map_pc(self, left_top, mouse_pos):
        """
        获得地图像素坐标
        :param left_top:
        :param mouse_pos:
        :return:
        """
        x = left_top[0] + mouse_pos[0]  # 屏幕左上角地图绝对像素点 + 鼠标相对点 = 地图绝对点
        y = left_top[1] + mouse_pos[1]
        if x < 0:
            self.x = 0
        elif x > self.width:
            self.x = self.width
        else:
            self.x = x
        if y < 0:
            self.y = 0
        elif y > self.height:
            self.y = self.height
        else:
            self.y = y
        return self.get()

    def set(self, pos):
        self.x = int(pos[0])
        self.y = int(pos[1])

    def get(self):
        return self.x, self.y