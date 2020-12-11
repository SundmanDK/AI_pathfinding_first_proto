import math
import random
import pandas

class Brain:
    """The Ai of the program."""
    def __init__(self, game):
        """Makes a link to the settings."""
        self.settings = game.settings
        self.reached_goal_value = self.settings.dot_start_x - self.settings.goal_pos_x + self.settings.dot_start_y - self.settings.goal_pos_y
        self.champ_vect_list = "N/A"
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
        #if self.settings.gather_data == False:
        print(f"champ fitness {max}, nr. of steps {champ.time_alive}, generation {self.settings.gen}, champ id {ID}, reached goal {dot.reached_goal}")
        return champ

    def fitness_calc(self, dead_list):
        """Calculates the fitness for each dot."""
        for dot in dead_list:
            if dot.reached_goal:
                fitness = self.reached_goal_value/(dot.time_alive) + 1  # Bonus points for reaching goal
            else:
                dist = self.dist_to_goal(dot.x_dot, dot.y_dot)
                fitness = self.settings.goal_radius/(dist)
                # goal_radius = 2 * dot_radius limit of distance is 10 (max fitness = 1) never reached because when ditance
                # equals 10 the goal has been reached and fitness is calculated differently.
            dot.fitness = fitness

    def remove_loops(self, vect_list, pos_list):
        """"""
        pos_list_copy = pos_list.copy()
        pos_list_copy.reverse()
        removed = False

        for index_, position in enumerate(pos_list):
            rev_index = len(pos_list) - pos_list_copy.index(position) - 1
            if rev_index != index_:
                pos_before = pos_list[:index_ + 1]
                pos_after = pos_list[rev_index + 1:]
                new_pos_list = pos_before + pos_after

                vect_before = vect_list[:index_ + 1]
                vect_after = vect_list[rev_index + 1:]
                new_vect_list = vect_before + vect_after

                removed = True

                break
        if not removed:
            return vect_list
        else:
            return self.remove_loops(new_vect_list, new_pos_list)

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

    def dist_to_goal(self, x_pos, y_pos):
        """Calculates the distance between a dot and the goal."""
        distance = math.sqrt((x_pos - self.settings.goal_pos_x)**2
                                + (y_pos - self.settings.goal_pos_y)**2)
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