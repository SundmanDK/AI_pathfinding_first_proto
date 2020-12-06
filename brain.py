import math
import random
import pandas

class Brain:
    """
    The Ai of the program.
    """
    def __init__(self, game):
        """Makes a link to the settings."""
        self.settings = game.settings
        self.reached_goal_value = self.settings.dot_start_x - self.settings.goal_pos_x + self.settings.dot_start_y - self.settings.goal_pos_y

        if self.settings.gather_data:
            # Dictionary for champion values
            self.champ_DataFrame = pandas.DataFrame({
                'Fitness': ['N/A' for _ in range(self.settings.max_gen)],
                'Nr. steps': ['N/A' for _ in range(self.settings.max_gen)],
                'Generation': ['N/A' for _ in range(self.settings.max_gen)],
                'ID': ['N/A' for _ in range(self.settings.max_gen)],
                'Reached goal': ['N/A' for _ in range(self.settings.max_gen)],
                'Round nr.': ['N/A' for _ in range(self.settings.max_gen)]
            })

    def find_champ(self, dead_list):
        """Finds the best rute of the generation."""
        self.fitness_calc(dead_list)
        max = 0
        for dot in dead_list:
            if max < dot.fitness:
                max = dot.fitness
                ID = dot.ID
                champ = dot
        if self.settings.gather_data == False:
            print(f"champ fitness {max}, nr. of steps {champ.time_alive}, generation {self.settings.gen}, champ id {ID}")
        return champ

    def fitness_calc(self, dead_list):
        """Calculates the fitness for each dot."""
        for dot in dead_list:
            if dot.reached_goal == True:
                fitness = self.reached_goal_value/(dot.time_alive) + 1  # Bonus points for reaching goal
            else:
                dist = self.dist_to_goal(dot)
                fitness = self.settings.goal_radius/(dist)
                # goal_radius = 2 * dot_radius lim dist->10 (f = 1) never reached
            dot.fitness = fitness

    def mutate(self, list):
        """Mutates the champion rute to create a new rute."""
        list2 = list.copy()
        mutate_factor = random.randint(0, len(list)-1)
        for _ in range(int(mutate_factor/self.settings.mutate_steps)):
            a = random.choice(self.settings.move_list)
            index = random.randint(0,len(list))-self.settings.mutate_steps
            for step in range(self.settings.mutate_steps):
                list2[index + step] = a
        return list2

    def dist_to_goal(self, dot):
        """Calculates the distance between a dot and the goal."""
        distance = math.sqrt((dot.x_dot - self.settings.goal_pos_x)**2
                                + (dot.y_dot - self.settings.goal_pos_y)**2)
        return distance

    def write_to_DataFrame(self, fitness, nr_steps, gen, ID, reached_goal, round):
        """Saves the data of each Champion in a dataframe."""
        #print(f"added gen nr. {self.settings.gen}")
        self.champ_DataFrame['Fitness'][self.settings.gen-1] = fitness
        self.champ_DataFrame['Nr. steps'][self.settings.gen-1] = nr_steps
        self.champ_DataFrame['Generation'][self.settings.gen-1] = gen
        self.champ_DataFrame['ID'][self.settings.gen-1] = ID
        self.champ_DataFrame['Reached goal'][self.settings.gen-1] = reached_goal
        self.champ_DataFrame['Round nr.'][self.settings.gen-1] = round

        if self.settings.gen == self.settings.max_gen:
            print("This run")
            print(self.champ_DataFrame)

            if self.settings.run_counter > 0:
                previous_data = self.final_data
                self.final_data = previous_data.append(self.champ_DataFrame, ignore_index=True)
            elif self.settings.run_counter == 0:
                self.final_data = self.champ_DataFrame.copy()

            print("Full set")
            print(self.final_data)
