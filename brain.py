import math
import random

class Brain:

    def __init__(self, game):
        self.settings = game.settings

    def find_champ(self, dead_list):
        self.fitness_calc(dead_list)
        max = 0
        #print("dead_list", len(dead_list))
        for i in range(len(dead_list)):
            if max < dead_list[i].fitness:
                max = dead_list[i].fitness
                index = i
        print(f"champ choice{index}", end=", ")
        champ = dead_list[index]
        #dead_list.clear()
        return champ

    def fitness_calc(self, dead_list):
       # print("fitness")
       # print("dead_list", len(dead_list))
        for dot in dead_list:
            if dot.reached_goal == True:
                fitness = 100/(dot.time_alive**2)
            else:
                dist = self.dist_to_goal(dot)
                fitness = 1/(dist**2) # obs: fitness udregnet fra timestep ikke sammenlignelig med fitness udregnet fra afstand til mål
          #  print(f"{fitness}", end=", ")
            dot.fitness = fitness

    def mutate(self, list):
        list2 = list.copy()
        for _ in range(self.settings.mutate_factor):
            list2[random.randint(0,len(list))-1] = random.choice(self.settings.move_list)
        return list2

    def dist_to_goal(self, dot):
        distance = math.sqrt((dot.x_dot - self.settings.goal_pos_x)**2
                                + (dot.y_dot - self.settings.goal_pos_y)**2)
        print(f"({dot.x_dot},{dot.y_dot}) goal: {distance}", end="\n")

        return distance


