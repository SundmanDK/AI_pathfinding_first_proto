import math
import random

class Brain:

    def __init__(self, game):
        self.settings = game.settings
        self.fitness_list = []
        self.dot_group = game.dot_group

    def run_brain(self):
        self.fitness_calc()
        self.champion = self.find_champ()

    def find_champ(self):
        max = 0
        for i in range(len(self.fitness_list)):
            if max < self.fitness_list[i]:
                max = self.fitness_list[i]
                index = i
        champ = self.dot_group[index]
        return champ

    def fitness_calc(self):
        for dot in self.dot_group:
            if dot.reached_goal == True:
                fitness = 1/(dot.time_alive**2)
            else:
                dist = self.dist_to_goal(dot)
                fitness = 1/(dist**2) # obs: fitness udregnet fra timestep ikke sammenlignelig med fitness udregnet fra afstand til mål
            #dot.fitness = fitness
            self.fitness_list.append(fitness)

    def mutate(self, champ):
        for i in range(self.settings.mutate_factor):
            champ.vect_list[random.randint(0,len(champ.vect_list))] = random.choice(self.settings.move_list)

    def dist_to_goal(self, dot):
        distance = int(math.sqrt((dot.x_dot - self.settings.goal_pos_x)**2
                                + (dot.y_dot - self.settings.goal_pos_y)**2))
        return distance


