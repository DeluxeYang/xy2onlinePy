import math
from heapq import *

class AStar:
    def __init__(self, array):
        self.array = array
        self.h = self.array.shape[0]
        self.w = self.array.shape[1]

    def find_path(self, current, target):
        """
        游戏路径获取算法
        :param current: 当前点，起点
        :param target: 目标点，终点
        :return:
        """
        start = (int(current[1]) // 20, int(current[0] // 20))  # 初始坐标由像素地图坐标转为游戏坐标
        goal = (int(target[1] // 20), int(target[0] // 20))
        flag = True
        if 0 <= goal[0] < self.h and 0 <= goal[1] < self.w:
            if self.array[goal[0], goal[1]] > 0:
                flag = False
                goal = self.nearest_valid_coord(goal)
        path = self.a_star(start, goal)[::-1]  # A*算法得到路径
        path_list = self.adjust_path([start] + path)  # 去除多余点, 同时将游戏坐标转为地图像素坐标
        if flag and len(path_list) > 0:
            path_list[-1] = target  # 将最后一个坐标，设为target_pc
        return path_list

    @staticmethod
    def heuristic(a, b):
        """
        启发
        """
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) * 1.2

    def a_star(self, start, goal):
        """
        A*算法
        :param start:
        :param goal:
        :return:
        """
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        close_set = set()
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        o_heap = []
        heappush(o_heap, (f_score[start], start))
        while o_heap:
            current = heappop(o_heap)[1]
            if current == goal:
                data = []
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                return data
            close_set.add(current)
            for t in neighbors:
                neighbor = int(current[0] + t[0]), int(current[1] + t[1])
                tentative_g_score = g_score[current] + self.heuristic(current, neighbor)
                if 0 <= neighbor[0] < self.array.shape[0]:
                    if 0 <= neighbor[1] < self.array.shape[1]:
                        if self.array[neighbor[0]][neighbor[1]] == 1:
                            continue
                    else:
                        continue  # array bound y walls
                else:
                    continue  # array bound x walls
                if neighbor in close_set and tentative_g_score >= g_score.get(neighbor, 0):
                    continue
                if tentative_g_score < g_score.get(neighbor, 0) or neighbor not in [i[1] for i in o_heap]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heappush(o_heap, (f_score[neighbor], neighbor))
        return []

    def adjust_path(self, path):
        """
        如果两个点之间没有阻碍，则抛弃他们之间点
        :param path:
        :return:
        """
        left = 0
        right = len(path) - 1
        _path = []
        while left < right:
            x1 = path[left][0]
            y1 = path[left][1]
            x2 = path[right][0]
            y2 = path[right][1]
            if self.is_obstacle_in_between(x1, y1, x2, y2):
                right -= 1  # 有阻碍，则right - 1，检验前一个点
                continue
            _path.append((path[right][1] * 20 + 10, path[right][0] * 20 + 10))  # 没有阻碍，则可直接到这个点
            left = right
            right = len(path) - 1
        return _path

    def is_obstacle_in_between(self, x1, y1, x2, y2):
        """
        查看两点之间是否有阻碍，有则返回True
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return:
        """
        f = self.generate_function(x1, y1, x2, y2)
        anti_f = self.generate_function(y1, x1, y2, x2)
        for x in range(min(x1, x2) + 1, max(x1, x2)):
            if self.array[x][int(f(x)) + 1] > 0:
                return True
        for y in range(min(y1, y2) + 1, max(y1, y2)):
            if self.array[int(anti_f(y))][y] > 0:
                return True
        return False

    @staticmethod
    def generate_function(x1, y1, x2, y2):
        def f(x):
            return y1 + ((x - x1) * (y2 - y1)) / (x2 - x1)
        return f

    def nearest_valid_coord(self, point):
        """
        获取离障碍点最近的可达点，广度搜索该点的四周
        :param point:
        :return:
        """
        _stack = [point]
        been = {}
        neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        while _stack:
            _point = _stack.pop(0)
            if self.array[_point[0]][_point[1]] == 0:
                return _point
            been[_point] = 1
            for n in neighbors:
                temp = _point[0]+n[0], _point[1]+n[1]
                if temp not in been:
                    if 0 <= temp[0] < self.h and 0 <= temp[1] < self.w:
                        _stack.append(temp)
                        been[temp] = 1
