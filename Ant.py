#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys
import math
import copy
import matplotlib.pyplot as plt
(ALPHA, BETA, RHO, Q) = (10, 15, 0.8, 10.0)
(city_num, ant_num, iter_max) = (48, 10, 10)
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
            if distance[self.currentCity][i] == 0:
                next_city = i
                self.allowedCites.remove(next_city)
                self.tabu.append(next_city)
                self.currentCity = next_city
                return
            total_prob += pow(pheromone[self.currentCity][i],ALPHA) *\
                pow(1.0 / distance[self.currentCity][i],BETA)
        for k in xrange(city_num):
            if k in self.allowedCites:
                probs[k] = pow(pheromone[self.currentCity][k],ALPHA) *\
                    pow(1.0 / distance[self.currentCity][k],BETA) / total_prob
            else:
                probs[k] = 0

        next_city = -1
        rand = random.uniform(0,1)
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

        for i in xrange(city_num):
            for j in xrange(city_num):
                distance[i][j] = math.sqrt((distance_x[i] - distance_x[j]) * (distance_x[i] - distance_x[j]) +\
                                          (distance_y[i] - distance_y[j]) * (distance_y[i] - distance_y[j]))
                pheromone[i][j] = 1.0

    def search_path(self):
        for g in xrange(iter_max):
            for ant in self.ants:
                for i in xrange(city_num-1):
                    ant.select_next_city()

                ant.tabu.append(ant.startCity)
                ant.calculate_path()
                if ant.total_distance < self.best_ant.total_distance:
                    self.best_ant = copy.deepcopy(ant)

            self.update_pheromone()

            for ant in self.ants:
                ant = ant.data_init()
    def update_pheromone(self):
        delta = [[0.0 for i in xrange(city_num)]
                  for j in xrange(city_num)]
        for ant in self.ants:
            for i in xrange(1, city_num):
                start, end = ant.tabu[i - 1], ant.tabu[i]
                delta[start][end] += Q / ant.total_distance
                delta[end][start] = delta[start][end]

            end = ant.tabu[0]
            delta[start][end] += Q / ant.total_distance
            delta[end][start] = delta[start][end]

        for i in xrange(city_num):
            for j in xrange(city_num):
                pheromone[i][j] = pheromone[i][j] * RHO + delta[i][j]

test = AntColony()
test.search_path()
print "Best Distance: ", test.best_ant.total_distance
print "Best Path: ", test.best_ant.tabu

for i in range(city_num):
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



