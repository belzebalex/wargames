from random import randrange
import random
import math
import numpy as np
from bullet import Coord
from fightingentity import FightingEntity

class NeuralNetwork:
    def __init__(self):
        self.input_layer_size = 2
        self.layers_size = [7]


        self.weights = []

        for i, layer in enumerate(self.layers_size):
            if(i == 0): self.weights.append(np.random.randn(self.input_layer_size, layer))
            else:       self.weights.append(np.random.randn(self.layers_size[i-1], layer))

        print(self.weights)
        self.nearest_opponent_distance = 0
        self.nearest_opponent_angle = 0
        self.nearest_friend_distance = 0
        self.nearest_friend_angle = 0

    def forwardPropagation(self, X):
        for i, w in enumerate(self.weights):
            if(i == 0): z = np.dot(X, w)
            else:
                a = self.sigmoid(z)
                z = np.dot(a, w)

        y_hat = self.sigmoid(z)

        return y_hat


    def mutate(self, mutation_factor):
        weight_number = 0
        for i, layer in enumerate(self.layers_size):
            if(i == 0): weight_number += self.input_layer_size * layer
            else:       weight_number += self.layers_size[i-1] * layer
        proba = 1/weight_number

        for w in self.weights:
            for (x,y), el in np.ndenumerate(w):
                if(random.random() < proba):
                    w[x,y] = random.uniform(-2.0,2.0)






    def sigmoid(self, z):
        return 1/(2+np.exp(-z))

class Soldier(FightingEntity):
    def __init__(self, x_pos, y_pos, team):
        FightingEntity.__init__(self, x_pos, y_pos, team)
        self.neurons = NeuralNetwork()
        self.nearest_opponent_distance = 0
        self.nearest_opponent_angle = 0
        self.nearest_friend_distance = 0
        self.nearest_friend_angle = 0


    def giveEnvironnement(self, soldiers):
        self.nearest_opponent_distance = 0
        self.nearest_opponent_angle = 0
        self.nearest_friend_distance = 0
        self.nearest_friend_angle = 0

        for sol in soldiers:
            if sol is not self:
                distance = math.sqrt( (sol.position_x - self.position_x ) ** 2 + (sol.position_y - self.position_y) ** 2 )
                sol_to_self_vec = Coord(self.position_x - sol.position_x, self.position_y - sol.position_y)
                angle = 0
                if(sol_to_self_vec.y != 0):
                    angle = (self.angle % 360) - (math.degrees(math.atan(sol_to_self_vec.x/sol_to_self_vec.y))) - 180
                if(sol_to_self_vec.y > 0 and sol_to_self_vec.x < 0):
                    angle -= 180
                if(sol_to_self_vec.y > 0 and sol_to_self_vec.x > 0):
                    angle += 180

                if(sol.team == self.team):
                    if(self.nearest_friend_distance == 0 or self.nearest_friend_distance > distance):
                        self.nearest_friend_distance = distance
                        self.nearest_friend_angle = math.fabs(angle)
                else:
                    if(self.nearest_opponent_distance == 0 or self.nearest_opponent_distance > distance):
                        self.nearest_opponent_distance = distance
                        self.nearest_opponent_angle = math.fabs(angle)


    def mutate(self, mutation_factor):
        self.neurons.mutate(mutation_factor)


    def resetNeurons(self):
        self.neurons = NeuralNetwork()



    def update(self):
        FightingEntity.update(self)
        neural_input = np.array([#self.nearest_friend_angle / 180, \
                                #self.nearest_friend_distance / 500, \
                                (self.nearest_opponent_angle )/ 90, \
                                self.nearest_opponent_distance / 150
                                ])



        neural_output = self.neurons.forwardPropagation(neural_input)
        if(neural_output[0] > 0): self.shooting = True
        else:                       self.shooting = False

        move = Coord(0,0)
        move.x = neural_output[1] * 10 - neural_output[2] * 10
        move.y = neural_output[3] * 10 - neural_output[4] * 10
        self.move(move.x, move.y)

        rotation =  neural_output[5] * 10 - neural_output[6] * 10
        self.rotate(rotation)
