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
        self.missing_vectors = self.settings.list_length - len(list)
        if ID == 99:
            print("missing vectors =",self.missing_vectors)
        if self.missing_vectors != 0:
            # if this is the first generation then make a random rute for the dot.
            self.fill_vect_list_randomly(self.missing_vectors)
        self.x_dot = self.settings.dot_start_x
        self.y_dot = self.settings.dot_start_y
        self.color = color
        self.pos_list = []

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
            self.pos_list.append((self.x_dot,self.y_dot))

    def fill_vect_list_randomly(self, missing_vectors):
        """Creates a random rute for the dot. A list of vectors"""
        for i in range(int(missing_vectors/self.settings.dot_speed)):
            vect = self.settings.move_list[random.randint(0,7)]
            for j in range(self.settings.dot_speed):
                self.vect_list.append(vect)
        for i in range(self.settings.list_length - len(self.vect_list)):
            vect = random.choice(self.settings.move_list)
            self.vect_list.append(vect)