

def get_window_pc(left_top, map_pc):
    return int(map_pc[0] - left_top[0]), int(map_pc[1] - left_top[1])


def is_same_coordinate(current, target):
    return abs(target[0] - current[0]) < 5 and abs(target[1] - current[1]) < 5


def cal_direction_8(self):
    x = self.target[0] - self.current[0]
    y = self.target[1] - self.current[1]
    if x == 0:
        if y < 0:
            return 6
        else:
            return 4
    y = y * 4096 / abs(x)
    if x > 0:
        if y < -9889:
            return 6
        if y < -1697:
            return 3
        if y < 1697:
            return 7
        if y < 9889:
            return 0
        return 4
    if y < -9889:
        return 6
    if y < -1697:
        return 2
    if y < 1697:
        return 5
    if y < 9889:
        return 1
    return 4


def cal_direction_4(self):
    delta_x = self.target[0] - self.current[0]
    delta_y = self.target[1] - self.current[1]
    if delta_x >= 0:
        if delta_y >= 0:
            return 0
        else:
            return 3
    else:
        if delta_y > 0:
            return 1
        else:
            return 2
