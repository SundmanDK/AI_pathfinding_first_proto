import math
import random

class Brain:
    """
    The Ai of the program.
    """
    def __init__(self, game):
        """Makes a link to the settings."""
        self.settings = game.settings

    def find_champ(self, dead_list):
        """Finds the best rute of the generation."""
        self.fitness_calc(dead_list)
        max = 0
        for i in range(len(dead_list)):
            if max < dead_list[i].fitness:
                max = dead_list[i].fitness
                index = i
        print(f"champ choice{index}", end=", ")
        champ = dead_list[index]
        return champ

    def fitness_calc(self, dead_list):
        """Calculates the fitness for each dot."""
        for dot in dead_list:
            if dot.reached_goal == True:
                fitness = 1/(dot.time_alive**2)+100
            else:
                dist = self.dist_to_goal(dot)
                fitness = 1/(dist**2) # obs: fitness udregnet fra timestep ikke sammenlignelig med fitness udregnet fra afstand til mål
          #  print(f"{fitness}", end=", ")
            dot.fitness = fitness

    def mutate(self, list):
        """Mutates the champion rute to create a new rute."""
        list2 = list.copy()
        mutate_factor = random.randint(0, len(list)-1)
        for _ in range(int(mutate_factor/self.settings.mutate_steps)):
            a = random.choice(self.settings.move_list)
            index = random.randint(0,len(list))-self.settings.mutate_steps
            for i in range(self.settings.mutate_steps):
                list2[index + i] = a #random.choice(self.settings.move_list)
        return list2

    def dist_to_goal(self, dot):
        """Calculates the distance between a dot and the goal."""
        distance = math.sqrt((dot.x_dot - self.settings.goal_pos_x)**2
                                + (dot.y_dot - self.settings.goal_pos_y)**2)
        #print(f"({dot.x_dot},{dot.y_dot}) goal: {distance}", end="\n")

        return distance


