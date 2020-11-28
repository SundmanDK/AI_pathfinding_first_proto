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
        self.objects()
        self.dead_dots = []
        self.brain = Brain(self)
        self.gen_counter()

    def gen_counter(self):
        """draw the gen counter on screen"""
        self.font = pygame.font.Font(None, 32)
        self.text = self.font.render(f'Generation: {self.settings.gen}', True, self.settings.WHITE, self.settings.BLACK)
        self.textRect = self.text.get_rect()
        self.textRect.left = 10
        self.textRect.top = 10

    def objects(self):
        """Creates the initial objects of the program."""
        # Outer bounds
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
        self.goal = Obstacle(self,
                             0,0,
                             self.settings.goal_radius * 2,
                             self.settings.goal_radius * 2,
                             self.settings.goal_color)
        # Moves the goal to its correct position.
        self.goal.rect.centerx = self.settings.goal_pos_x
        self.goal.rect.centery = self.settings.goal_pos_y
        self.goal_group.add(self.goal)

        # Dots
        self.dot_group = pygame.sprite.Group()
        for dot in range(self.settings.dot_amount):
            new_dot = Dot(self,[], self.settings.dot_color)
            self.dot_group.add(new_dot)

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

    def create_next_gen(self):
        """Deletes the old generation(?) and creates a new one. """
        self.settings.gen += 1
        self.gen_counter()
        self.champion_vect_list = self.brain.find_champ(self.dead_dots).vect_list
        for dot in self.dot_group:
            del dot
        self.dot_group.empty()
        for dot in range(self.settings.dot_amount -1):
            mutated_list = self.brain.mutate(self.champion_vect_list)
            next_gen_dot = Dot(self, mutated_list, self.settings.dot_color)
            self.dot_group.add(next_gen_dot)
        champion_dot = Dot(self, self.champion_vect_list, self.settings.champ_color)
        self.dot_group.add(champion_dot)

        # reset
        self.dead_dots.clear()
        self.settings.time_step = 0
        self.settings.all_dead = False

    def update_screen(self):
        """Graphical updates."""
        self.screen.fill(self.settings.bg_color)
        if self.settings.gen > 1:
            self.draw_champion_path(self.champion_vect_list)
        for wall in self.wall_group.sprites():
            wall.draw_obstacle()
        self.goal.draw_obstacle()
        self.screen.blit(self.text, self.textRect)
        for dot in self.dot_group.sprites():
            dot.draw_dot()


        # Flip screen
        pygame.display.flip()
        self.clock.tick(self.settings.FPS)

    def draw_champion_path(self, champ_list):
        """draws a line along the champions path."""

        startpos_x = self.settings.dot_start_x
        startpos_y = self.settings.dot_start_y

        for i in range(len(champ_list)-1):
            startpos_x += champ_list[i][0]
            startpos_y += champ_list[i][1]
            endpos_x = startpos_x + champ_list[i+1][0]
            endpos_y = startpos_y + champ_list[i+1][1]
            pygame.draw.line(self.screen,
                             self.settings.champ_color,
                             (startpos_x, startpos_y),
                             (endpos_x, endpos_y),
                             )

    def check_collision(self):
        """Checks for collision between the dots and the walls and boundaries, and the goal."""
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
            self.all_dots_dead()

    def all_dots_dead(self):
        """
        Manages the boolean value for running the create_next_gen() function,
        i.e. telling the program when to let the Ai work on the result of the generation.
        """
        for dot in self.dot_group:
            if dot.alive == True:
                self.settings.all_dead = False
            else:
                self.settings.all_dead = True

    def check_events(self):
        """Checks user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.settings.allow_update = not(self.settings.allow_update)
