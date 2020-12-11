import math
import random
import pandas

class Brain:
    """The Ai of the program."""
    def __init__(self, game):
        """Makes a link to the settings."""
        self.settings = game.settings
        self.reached_goal_value = self.settings.dot_start_x - self.settings.goal_pos_x + self.settings.dot_start_y - self.settings.goal_pos_y

        if self.settings.gather_data:
            # Dictionary for champion values. Made to the size we need it with temporary values.
            self.champ_DataFrame = pandas.DataFrame({
                'Fitness': ['N/A' for _ in range(self.settings.max_gen)],
                'Nr. steps': ['N/A' for _ in range(self.settings.max_gen)],
                'Generation': ['N/A' for _ in range(self.settings.max_gen)],
                'ID': ['N/A' for _ in range(self.settings.max_gen)],
                'Reached goal': ['N/A' for _ in range(self.settings.max_gen)],
                'Round nr.': ['N/A' for _ in range(self.settings.max_gen)]
            })

    def find_champ(self, dead_list):
        """Finds the best rute of the generation. Determined based on the highest fitness."""
        self.fitness_calc(dead_list)
        max = 0
        for dot in dead_list:
            if max < dot.fitness:
                max = dot.fitness
                ID = dot.ID
                champ = dot
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
        """
        Inspired by function developed in cooperation with Maja H. Krikeby.
        The function identifies loops in a route and cuts them out
        """
        # List of positions used to compare with original list.
        pos_list_copy = pos_list.copy()
        pos_list_copy.reverse()
        removed = False  # Used to determine if a loop was removed from the lists.

        # for loop which looks at both the data at each point and accompanying index.
        for index_, position in enumerate(pos_list):
            # finds the "normal" index of the last time the coordinate is visited
            rev_index = len(pos_list) - pos_list_copy.index(position) - 1
            if rev_index != index_:  # compares to see if the coordinate is visited multiple times.
                # takes a slice before and after the loop and gathers them in to one list.
                pos_before = pos_list[:index_ + 1]
                pos_after = pos_list[rev_index + 1:]
                new_pos_list = pos_before + pos_after
                # repeat for the vector list
                vect_before = vect_list[:index_ + 1]
                vect_after = vect_list[rev_index + 1:]
                new_vect_list = vect_before + vect_after

                removed = True  # A loop was removed

                break  # Break out of for loop to avoid index errors.
        if not removed:
            # If no loop was removed, correction of the route must be over.
            return vect_list
        else:
            # Call the method again to work through the route again, there might be more loops.
            return self.remove_loops(new_vect_list, new_pos_list)

    def mutate(self, vect_list):
        """Mutates the champion rute to create a new rute."""
        vect_list_copy = vect_list.copy()  # copy to avoid shallow copy issues.
        mutate_factor = random.randint(0, len(vect_list) - 1)  # gives each dot a random amount of mutations.

        # mutates a number of times:
        for _ in range(int(mutate_factor/self.settings.mutate_steps)):
            new_vect = random.choice(self.settings.move_list)
            index_ = random.randint(0, len(vect_list)) - self.settings.mutate_steps
            # Changes a given number of vector for each mutation. Smoother movements.
            for step in range(self.settings.mutate_steps):
                vect_list_copy[index_ + step] = new_vect
        return vect_list_copy

    def dist_to_goal(self, x_pos, y_pos):
        """Calculates the distance between a dot and the goal."""
        distance = math.sqrt((x_pos - self.settings.goal_pos_x)**2 + (y_pos - self.settings.goal_pos_y)**2)
        return distance

    def write_to_DataFrame(self, fitness, nr_steps, gen, ID, reached_goal, round):
        """Saves the data of each Champion in a dataframe."""
        # Fill in the DataFrame.
        self.champ_DataFrame['Fitness'][self.settings.gen-1] = fitness
        self.champ_DataFrame['Nr. steps'][self.settings.gen-1] = nr_steps
        self.champ_DataFrame['Generation'][self.settings.gen-1] = gen
        self.champ_DataFrame['ID'][self.settings.gen-1] = ID
        self.champ_DataFrame['Reached goal'][self.settings.gen-1] = reached_goal
        self.champ_DataFrame['Round nr.'][self.settings.gen-1] = round

        if self.settings.gen == self.settings.max_gen:
            if self.settings.run_counter == 0:
                # Makes the initial final DataFrame.
                self.final_data = self.champ_DataFrame.copy()
            elif self.settings.run_counter > 0:
                # Adds to the final DataFrame.
                previous_data = self.final_data
                self.final_data = previous_data.append(self.champ_DataFrame, ignore_index=True)
