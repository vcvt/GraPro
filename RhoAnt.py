#!/usr/bin/python
# -*- coding: utf-8 -*-#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys
import math
import copy
import time
import matplotlib.pyplot as plt
"""
    ALPHA:信息素启发因子
    BETA:期望启发因子
    RHO:信息素挥发系数
    Q:蚂蚁循环一周产生的信息量总量
    city_num:城市数目
    ant_num:蚂蚁数目
    iter_max:迭代次数
    distance_x:城市的x坐标
    distance_y:城市的y坐标
"""
"""
    最优解：
    att48.33522
    a280:2579
    berlin52:7542
"""
RHO_MIN = 0.1
(ALPHA, BETA, RHO, Q) = (4, 5, 1, 100)
(city_num, ant_num, iter_max) = (48, 40, 300)
distance_x = []
distance_y = []
for line in open('att48.tsp'):
    items = line.strip('\n').split()
    distance_x.append(float(items[1]))
    distance_y.append(float(items[2]))
distance = [[0.0 for i in xrange(city_num)]
                  for j in xrange(city_num)]
pheromone = [[1.0 for m in xrange(
    city_num)] for n in xrange(city_num)]

class Ant(object):
    def __init__(self, ID):
        self.ID = ID
        self.data_init()

    def data_init(self):
        self.total_distance = 0
        self.tabu = []
        self.allowedCites = [i for i in xrange(city_num)]
        self.startCity = random.randint(0,city_num-1)
        self.currentCity = self.startCity
        self.tabu.append(self.startCity)
        self.allowedCites.remove(self.currentCity)

    def select_next_city(self):
        probs = [0.0 for i in xrange(city_num)]
        total_prob = 0.0

        for i in self.allowedCites:
            """
            #防止某些数据中存在坐标相同的情况
            if distance[self.currentCity][i] == 0:
                next_city = i
                self.allowedCites.remove(next_city)
                self.tabu.append(next_city)
                self.currentCity = next_city
                return
            """
            total_prob += pow(pheromone[self.currentCity][i], ALPHA) * \
                          pow(1.0 / distance[self.currentCity][i], BETA)
        for k in xrange(city_num):
            if k in self.allowedCites:
                probs[k] = pow(pheromone[self.currentCity][k], ALPHA) * \
                           pow(1.0 / distance[self.currentCity][k], BETA) / total_prob
            else:
                probs[k] = 0
        next_city = -1
        rand = random.uniform(0, 1)
        ps = 0.0
        for i in xrange(city_num):
            ps += probs[i]
            if ps >= rand:
                next_city = i
                break
        self.allowedCites.remove(next_city)
        self.tabu.append(next_city)
        self.currentCity = next_city

    def calculate_path(self):
        length = 0
        for i in xrange(city_num):
            length += distance[self.tabu[i]][self.tabu[i+1]]
        self.total_distance = length

class AntColony:
    def __init__(self):
        self.ants = [Ant(ID) for ID in xrange(ant_num)]
        self.best_ant = Ant(-1)
        self.best_ant.total_distance = sys.maxint
        self.all_best_distance = [] #存储所有最优解,主要用来求达到最优解所需的迭代次数
        for i in xrange(city_num):
            for j in xrange(city_num):
                distance[i][j] = math.sqrt((distance_x[i] - distance_x[j]) * (distance_x[i] - distance_x[j]) +\
                                          (distance_y[i] - distance_y[j]) * (distance_y[i] - distance_y[j]))
                pheromone[i][j] = 1

    def search_path(self):
        for g in xrange(iter_max):
            for ant in self.ants:
                for i in xrange(city_num-1):
                    ant.select_next_city()
                ant.tabu.append(ant.startCity)
                ant.calculate_path()
                if ant.total_distance < self.best_ant.total_distance:
                    self.best_ant = copy.deepcopy(ant)
            self.all_best_distance.append(self.best_ant.total_distance)
            sameBefore = 0
            temp = self.all_best_distance[-1]
            for i in range(0, self.all_best_distance.__len__())[::-1]:
                if self.all_best_distance[i] == temp:
                    sameBefore += 1
                else:
                    break
            global RHO
            # 设置超过15则更新
            if sameBefore >= 15:
                if 0.95 * RHO >= RHO_MIN:
                    RHO = 0.95 * RHO
                else:
                    RHO = RHO_MIN
            self.update_pheromone()
            for ant in self.ants:
                ant.data_init()
            self._print()

    def _print(self):
        print "Best Distance: ", self.best_ant.total_distance
        print "Best Path: ", self.best_ant.tabu
        print "r",RHO

    def update_pheromone(self):
        delta = [[0.0 for i in xrange(city_num)]
                  for j in xrange(city_num)]
        for ant in self.ants:
            for i in xrange(1, city_num + 1):
                start, end = ant.tabu[i - 1], ant.tabu[i]
                delta[start][end] += Q # Ant-Density模型
                delta[end][start] = delta[start][end]
        for i in xrange(city_num):
            for j in xrange(city_num):
                pheromone[i][j] = pheromone[i][j] * RHO + delta[i][j]

if __name__ == '__main__':
    time_start = time.time()
    test = AntColony()
    test.search_path()
    print "Last Best Distance: ", test.best_ant.total_distance
    print "Last Best Path: ", test.best_ant.tabu
    time_end = time.time()
    print "Cost Time: ",time_end - time_start
    print RHO
    for i in xrange(iter_max):
        if test.all_best_distance[i] == test.best_ant.total_distance:
            print "Iter Times: ", i
            break
    plt.figure("Ant Colony Algorithm For TSP")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title('ACO RESULT')
    for i in range(city_num):
        if i == test.best_ant.tabu[0]:
            plt.plot(distance_x[i], distance_y[i], 'or')
        else:
            plt.plot(distance_x[i], distance_y[i], 'ok')
    x = []
    y = []
    for i in range(city_num):
        x.append(distance_x[test.best_ant.tabu[i]])
        y.append(distance_y[test.best_ant.tabu[i]])
    x.append(distance_x[test.best_ant.tabu[0]])
    y.append(distance_y[test.best_ant.tabu[0]])
    plt.plot(x, y)
    plt.show()



