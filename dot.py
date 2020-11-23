import pygame
import random
import numpy as np
from pygame.sprite import Sprite

class Dot(Sprite):
    def __init__(self, game, list, color):
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen
        self.vect_list = list
        if self.settings.gen == 1:
            self.rand_vect_list()
        self.x_dot = self.settings.dot_start_x #self.vect_list[self.settings.time_step][0]
        self.y_dot = self.settings.dot_start_y #self.vect_list[self.settings.time_step][1]
        self.color = color

        # Hitbox
        self.rect = pygame.Rect(
            self.x_dot,
            self.y_dot,
            self.settings.dot_radius * 2,
            self.settings.dot_radius * 2
        )
        self.alive = True
        self.reached_goal = False
        self.time_alive = 0
        self.fitness = 0.0

    # Draw the dot
    def draw_dot(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x_dot, self.y_dot),
            self.settings.dot_radius
        )
    def rand_vect_list(self):

        self.vect_list = []

        for i in range(int(self.settings.list_length/self.settings.dot_speed)):
            vect = self.settings.move_list[random.randint(0,7)] #np.array([random.randint(-1,1), random.randint(-1,1)])
            for j in range(self.settings.dot_speed):
                self.vect_list.append(vect)


    def update(self):
        if self.alive:
            self.x_dot += self.vect_list[self.settings.time_step][0]
            self.y_dot += self.vect_list[self.settings.time_step][1]
            self.rect.centerx = self.x_dot
            self.rect.centery = self.y_dot
            self.time_alive = self.settings.time_step

