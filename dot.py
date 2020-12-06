import pygame
import random
from pygame.sprite import Sprite

class Dot(Sprite):
    """The dot who tries different rutes to find a more optimal one."""
    def __init__(self, game, list, color, ID):
        """Sets initial values for the dots."""
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen
        self.vect_list = list
        if self.settings.gen == 1:
            # if this is the first generation then make a random rute for the dot.
            self.rand_vect_list()
        self.x_dot = self.settings.dot_start_x
        self.y_dot = self.settings.dot_start_y
        self.color = color

        # Hitbox
        self.rect = pygame.Rect(
            self.x_dot,
            self.y_dot,
            self.settings.dot_radius * 2,
            self.settings.dot_radius * 2
        )
        self.ID = ID
        self.alive = True
        self.reached_goal = False
        self.time_alive = 0
        self.fitness = 0.0

    # Draw the dot
    def draw_dot(self):
        """Draws the dot."""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x_dot, self.y_dot),
            self.settings.dot_radius)

    def update(self):
        """Moves the dot along its rute. One step pr. time increment"""
        if self.alive:
            self.x_dot += self.vect_list[self.settings.time_step][0]
            self.y_dot += self.vect_list[self.settings.time_step][1]
            self.rect.centerx = self.x_dot
            self.rect.centery = self.y_dot
            self.time_alive = self.settings.time_step

    def rand_vect_list(self):
        """Creates a random rute for the dot. A list of vectors"""
        self.vect_list = []

        for i in range(int(self.settings.list_length/self.settings.dot_speed)):
            vect = self.settings.move_list[random.randint(0,7)]
            for j in range(self.settings.dot_speed):
                self.vect_list.append(vect)