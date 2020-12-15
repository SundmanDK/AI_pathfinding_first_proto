"""
Program Developed by:
Martin Sundman (Sundman@ruc.dk, 70464)
Mathias Marquar Arhipenko Larsen (mamaar@ruc.com, 70434)
Oliver Skjellerup Demuth Heinecke (osdh@ruc.dk, 71604)
Rasmus Beyer Andersen (rbeyera@ruc.dk, 71466)
Zaïna Miranda Brunse Parly (zmbp@ruc.dk, 70455)

Advisor:
Maja H. Kirkeby (majaht@ruc.dk)
"""

import pygame
import sys
from settings import Settings
from dot import Dot
from obstacles import Obstacle
from brain import Brain


class Game:
    """Main class for organizing and running the program."""
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,
             self.settings.screen_height)
        )
        pygame.display.set_caption("AI Pathfinding")
        self.dot_group = pygame.sprite.Group()  # Will contain all dots. Used for collision detection and group update
        self.objects()  # Creates all the objects in the game
        self.dead_dots = []  # List used when we calculate fitness
        self.brain = Brain(self)  # Ai of the game
        self.gen_counter()  # Graphical element showing which generation is currently running
        self.create_background([])  # draws a black background for the moment
        self.background_image = pygame.image.load("rute_image.bmp")  # Will later include rute of previous champion

    def run(self):
        """Main loop of the program."""
        while self.settings.running:
            self.check_events()
            self.check_alive()
            self.update_screen()
            if self.settings.allow_update:  # If you press space then the dots stop updating.
                for dot in self.dot_group.sprites():
                    if dot.alive:
                        dot.update()
                self.settings.time_step += 1

            if self.settings.all_dead:
                self.create_next_gen()

            if not self.settings.gather_data:
                self.clock.tick(self.settings.FPS)

    def check_events(self):
        """Checks for user input and acts accordingly."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Click the red X to shut down program.
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press space to pause dot updates. (screen captures and other)
                    self.settings.allow_update = not(self.settings.allow_update)
                if event.key == pygame.K_ESCAPE:  # Press ESC to shut down program.
                    pygame.quit()
                    sys.exit()

    def update_screen(self):
        """Graphical updates. Background, walls, goal and dots."""
        self.screen.blit(self.background_image, self.screen.get_rect())

        for wall in self.wall_group.sprites():
            wall.draw_obstacle()
        self.goal.draw_obstacle()
        self.screen.blit(self.gen_count_text, self.textRect)
        for dot in self.dot_group.sprites():
            dot.draw_dot()

        # Flip screen
        pygame.display.flip()

    def gen_counter(self):
        """Draws the gen counter as an image to be drawn on screen."""
        self.font = pygame.font.Font(None, 32)
        self.gen_count_text = self.font.render(f'Generation: {self.settings.gen}', True, self.settings.WHITE, self.settings.BLACK)
        self.textRect = self.gen_count_text.get_rect()
        # Assign location
        self.textRect.left = 10
        self.textRect.top = 10

    def create_background(self, champ_list):
        """
        Creates the background for the game.
        It is necessary to make the background an image because we want to show a line behind the dots representing the
        champions path. Making it in to a picture and blit'ing it on to the screen makes the program run much faster.
        """
        pygame.display.flip()
        self.screen.fill(self.settings.bg_color)
        startpos_x = self.settings.dot_start_x
        startpos_y = self.settings.dot_start_y

        # Draws lines representing the champion path
        for i in range(len(champ_list)-1):
            startpos_x += champ_list[i][0]
            startpos_y += champ_list[i][1]
            endpos_x = startpos_x + champ_list[i+1][0]
            endpos_y = startpos_y + champ_list[i+1][1]
            pygame.draw.line(self.screen,
                             self.settings.GREEN,
                             (startpos_x, startpos_y),
                             (endpos_x, endpos_y),
                             )

        pygame.image.save(self.screen, "rute_image.bmp")

    def objects(self):
        """
        Creates the initial objects of the program. inner and outer walls, the goal, and calls for creation of the dots.
        """
        # Outer bounds and inner walls. made using a dictionary containing info for each element.
        self.wall_group = pygame.sprite.Group()
        for i in range(len(self.settings.wall_dict['x_coordinate'])):
            new_obstacle_or_wall = Obstacle(self,
                                    self.settings.wall_dict["x_coordinate"][i],
                                    self.settings.wall_dict["y_coordinate"][i],
                                    self.settings.wall_dict["width"][i],
                                    self.settings.wall_dict["height"][i],
                                    self.settings.obstacle_color
                                    )
            self.wall_group.add(new_obstacle_or_wall)

        # Goal
        self.goal_group = pygame.sprite.GroupSingle()
        # Creates the goal as an instance of Obstacle at the coordinates (0,0)
        # Using same class because all we need is a sprite object for collision detection.
        self.goal = Obstacle(self,
                             0,0,
                             self.settings.goal_radius * 2,
                             self.settings.goal_radius * 2,
                             self.settings.goal_color)
        # Moves the goal to its correct position.
        self.goal.rect.centerx = self.settings.goal_pos_x
        self.goal.rect.centery = self.settings.goal_pos_y
        self.goal_group.add(self.goal)

        # Separated to a new function because we use it again when we gather data.
        self.create_first_gen_dots()

    def create_first_gen_dots(self):
        """Creates 100 dots of 1. generation i.e. with empty lists to be filled randomly."""
        ID = 0  # given ID to keep track of each dot
        for dot in range(self.settings.dot_amount):
            new_dot = Dot(self,[], self.settings.dot_color, ID)
            self.dot_group.add(new_dot)
            ID += 1

    def check_collision(self):
        """Checks for collision between the dots and the walls and boundaries, and the goal. And acts accordingly."""
        obs_collision_list = pygame.sprite.groupcollide(self.dot_group, self.wall_group, False, False)
        goal_collision_list = pygame.sprite.groupcollide(self.dot_group, self.goal_group, False, False)
        for dot in obs_collision_list:
            dot.alive = False
        for dot in goal_collision_list:
            dot.alive = False
            dot.reached_goal = True

    def check_alive(self):
        """
        Checks if the individual dot is alive.
        Kills dots if they run out of steps on their rute.
        Adds all dots to a list to be worked on by the Ai.
        """
        self.check_collision()
        if self.settings.time_step >= self.settings.list_length:
            for dot in self.dot_group:
                dot.alive = False
                self.dead_dots.append(dot)
            self.settings.all_dead = True

    def create_next_gen(self):
        """Deletes the old generation(?) and creates a new one."""
        champion = self.brain.find_champ(self.dead_dots)
        self.champion_vect_list = self.brain.remove_loops(champion.vect_list, champion.pos_list)

        # Gather Data for analysis
        if self.settings.gather_data:
            self.auto_gather_data(champion)

        # Kill previous generation
        for dot in self.dot_group:
            del dot
        self.dot_group.empty()

        # Make the next generation
        self.settings.gen += 1
        self.gen_counter()
        ID = 0
        for dot in range(self.settings.dot_amount -1):
            mutated_list = self.brain.mutate(self.champion_vect_list)
            next_gen_dot = Dot(self, mutated_list, self.settings.dot_color, ID)
            self.dot_group.add(next_gen_dot)
            ID += 1
        champion_dot = Dot(self, self.champion_vect_list, self.settings.champ_color, ID)
        self.dot_group.add(champion_dot)

        # Draws the champion rute
        self.create_background(self.champion_vect_list)
        self.background_image = pygame.image.load("rute_image.bmp")

        # reset
        self.dead_dots.clear()
        self.settings.time_step = 0
        self.settings.all_dead = False

    def auto_gather_data(self, champion):
        """
        Makes the program automatically work through a given number of generations a given number of times to gather
        data for analysis.
        If we Say 50 generations and 3 runs the program will perform this and gather information on the Champion of each
        Generation.
        """

        # Save a row of data in Pandas DataFrame.
        self.brain.write_to_DataFrame(champion.fitness,
                                      champion.time_alive,
                                      self.settings.gen,
                                      champion.ID,
                                      champion.reached_goal,
                                      self.settings.run_counter)

        # Keeps track of generation and runs and acts accordingly.
        if self.settings.gen == self.settings.max_gen:
            self.settings.gen = 1  # Resests dot generation when one run is completed.
            self.settings.run_counter += 1  # keeps track of how many runs have been completed
            if self.settings.run_counter == self.settings.runs:
                # Write finished DataFrame to CSV
                self.brain.final_data.to_csv('Final_data.csv')  # all runs completed so we write to csv
                print(f"run nr. {self.settings.run_counter} over")  # lets us know the right amount of runs were completed
                # Data collection complete so we terminate the program
                pygame.quit()
                sys.exit()
            else:
                # reset to new run
                self.dead_dots.clear()
                self.settings.time_step = 0
                self.settings.all_dead = False
                self.create_first_gen_dots()
                self.gen_counter()
                print(f"run nr. {self.settings.run_counter} over")


if __name__ == '__main__':
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
