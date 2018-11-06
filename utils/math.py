

def get_screen_rect_pc(left_top, world_pc):
    return int(world_pc[0] - left_top[0]), int(world_pc[1] - left_top[1])


def is_same_coordinate(current, target):
    return abs(target[0] - current[0]) < 1 and abs(target[1] - current[1]) < 1


def calc_direction_8(obj):
    x = obj.target[0] - obj.x
    y = obj.target[1] - obj.y
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


def calc_direction_4(obj):
    delta_x = obj.target[0] - obj.x
    delta_y = obj.target[1] - obj.y
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

def quest_25(window_rect, row, col):
    """
    根据地图像素位置，获取需要的units_num
    :param window_rect: Pygame Rect
    :param row: 总行数
    :param col: 总列数
    :return:
    """
    _row = window_rect.centery // 240 if window_rect.centery // 240 != row else window_rect.centery // 240 - 1  # 向下取整
    _col = window_rect.centerx // 320 if window_rect.centerx // 320 != col else window_rect.centerx // 320 - 1  # 向下取整
    pos = int(_row * col + _col)  # 当前单元格
    _units = [pos]  # 正在
    left = right = up = down = 0
    if _col == 0:  # 左1，右边+2
        _units += [pos + 1, pos + 2]
        right += 2
    elif _col == 1:  # 左2， 右边+2， 左边+1
        _units += [pos - 1, pos + 1, pos + 2]
        right += 2
        left += 1
    elif _col == col - 1:  # 靠右，左边+2
        _units += [pos - 1, pos - 2]
        left += 2
    elif _col == col - 2:  # 右2，右边+1，左边+2
        _units += [pos + 1, pos - 1, pos - 2]
        right += 1
        left += 2
    else:
        _units += [pos + 1, pos + 2, pos - 1, pos - 2]
        right += 2
        left += 2

    if _row == 0:
        _units += [pos + col, pos + col * 2]
        down += 2
    elif _row == 1:
        _units += [pos - col, pos + col, pos + col * 2]
        up += 1
        down += 2
    elif _row == row - 1:
        _units += [pos - col, pos - col * 2]
        up += 2
    elif _row == row - 2:
        _units += [pos + col, pos - col, pos - col * 2]
        up += 2
        down += 1
    else:
        _units += [pos + col, pos + col * 2, pos -
                   col, pos - col * 2]
        up += 2
        down += 2
    if left * up > 0:
        for i in range(1, left + 1):
            for j in range(1, up + 1):
                _units.append((pos - i) - col * j)
    if left * down > 0:
        for i in range(1, left + 1):
            for j in range(1, down + 1):
                _units.append((pos - i) + col * j)
    if right * up > 0:
        for i in range(1, right + 1):
            for j in range(1, up + 1):
                _units.append((pos + i) - col * j)
    if right * down > 0:
        for i in range(1, right + 1):
            for j in range(1, down + 1):
                _units.append((pos + i) + col * j)
    _units.sort()
    return _units

def quest_16(window_rect, row, col, width_margin=160, height_margin=120):
    """
    根据地图像素位置，获取需要的units_num
    :param window_rect: Pygame Rect
    :param row: 总行数
    :param col: 总列数
    :param width_margin:
    :param height_margin:
    :return:
    """
    _row = window_rect.centery // 240 if window_rect.centery // 240 != row else window_rect.centery // 240 - 1  # 向下取整
    _col = window_rect.centerx // 320 if window_rect.centerx // 320 != col else window_rect.centerx // 320 - 1  # 向下取整
    pos = int(_row * col + _col)  # 当前单元格
    _units = [pos]  # 正在
    left = right = up = down = 0
    if _col == 0:  # 靠左，就把右边的单元格放进来
        _units.append(pos + 1)
        right += 1
        if _col + 2 <= col - 1:
            _units.append(pos + 2)
            right += 1
    elif _col == col - 1:  # 靠右，就把左边的单元格放进来
        _units.append(pos - 1)
        left += 1
        if _col - 2 >= 0:
            _units.append(pos - 2)
            left += 1
    else:  # 中间
        _units += [pos + 1, pos - 1]
        left = right = 1
        if window_rect.centerx % 320 >= 320 - width_margin and _col + 2 <= col - 1:  # 单元格内靠右，则右边预读
            _units.append(pos + 2)
            right += 1
        elif window_rect.centerx % 320 <= width_margin and _col - 2 >= 0:  # 单元格内靠左，左边预读
            _units.append(pos - 2)
            left += 1

    if _row == 0:  # 靠上，则把下面的格子放进来
        _units.append(pos + col)
        down += 1
        if _row + 2 <= row - 1:
            _units.append(pos + col * 2)
            down += 1
    elif _row == row - 1:  # 靠下，则把上面的格子放进来
        _units.append(pos - col)
        up += 1
        if _row - 2 >= 0:
            _units.append(pos - col * 2)
            up += 1
    else:
        _units += [pos + col, pos - col]
        up = down = 1
        if window_rect.centery % 240 >= 240 - height_margin and _row + 2 <= row - 1:  # 单元格内靠下，则预读下面
            _units.append(pos + col * 2)
            down += 1
        elif window_rect.centery % 240 <= height_margin and _row - 2 >= 0:  # 单元格内靠上，则预读上面
            _units.append(pos - col * 2)
            up += 1
    if left * up > 0:
        for i in range(1, left + 1):
            for j in range(1, up + 1):
                _units.append((pos - i) - col * j)
    if left * down > 0:
        for i in range(1, left + 1):
            for j in range(1, down + 1):
                _units.append((pos - i) + col * j)
    if right * up > 0:
        for i in range(1, right + 1):
            for j in range(1, up + 1):
                _units.append((pos + i) - col * j)
    if right * down > 0:
        for i in range(1, right + 1):
            for j in range(1, down + 1):
                _units.append((pos + i) + col * j)
    _units.sort()
    return _units
