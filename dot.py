import pygame
import random
from pygame.sprite import Sprite


class Dot(Sprite):  # Subclass of pygame's Sprite class
    """The dot who tries different rutes to find a more optimal one."""
    def __init__(self, game, list, color, ID):
        """Sets initial values for the dots."""
        super().__init__()
        self.settings = game.settings  # Connection to the instance of settings through the Game class.
        self.screen = game.screen  # Connection to the screen through the Game class.
        self.vect_list = list  # receives a list.
        # calculate how many vectors are missing from the list. The list must have a certain length otherwise we get index erros.
        self.missing_vectors = self.settings.list_length - len(list)
        if ID == 99:
            # look at how many vectors were removed using Brain method: remove_loops().
            print("missing vectors =", self.missing_vectors)
        if self.missing_vectors != 0:
            # If this is the first generation then make a random rute for the dot.
            self.fill_vect_list_randomly(self.missing_vectors)
        self.x_dot = self.settings.dot_start_x
        self.y_dot = self.settings.dot_start_y
        self.color = color  # receives a color, white for every dot except the champion which is blue.
        self.pos_list = []  # Used to keep track of the coordinates visited by each dot.

        # Hitbox. Dot being a subclass of the Sprite lets us use the pygame rect object as a hitbox using sprite.groupcollide()
        self.rect = pygame.Rect(
            self.x_dot,
            self.y_dot,
            self.settings.dot_radius * 2,
            self.settings.dot_radius * 2
        )
        # Important values exclusive to each dot.
        self.ID = ID
        self.alive = True
        self.reached_goal = False
        self.time_alive = 0
        self.fitness = 0.0

    # Draw the dot
    def draw_dot(self):
        """Draws the dot on screen."""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x_dot, self.y_dot),
            self.settings.dot_radius)

    def update(self):
        """Moves the dot along its rute. One step pr. time increment"""
        if self.alive:
            # Visual coordinate movement.
            self.x_dot += self.vect_list[self.settings.time_step][0]
            self.y_dot += self.vect_list[self.settings.time_step][1]
            # Hitbox coordinate movement.
            self.rect.centerx = self.x_dot
            self.rect.centery = self.y_dot
            self.time_alive = self.settings.time_step  # Keep track of how many steps the dot takes before dying.
            # Fill coordinate list. excluding start position to avoid index problems in the Brain method: remove_loops().
            self.pos_list.append((self.x_dot,self.y_dot))

    def fill_vect_list_randomly(self, missing_vectors):
        """Fills the vector list according with its need. For a first generation dot i creates a random rute."""
        # Fill the list with vectors.
        for i in range(int(missing_vectors/self.settings.dot_speed)):
            vect = self.settings.move_list[random.randint(0,7)]  # Pick a random vector
            for j in range(self.settings.dot_speed):  # Add the vector a given amount of times. Smoother movement.
                self.vect_list.append(vect)
        # If the list is still to short fill the last with random vectors.
        # This happens when missing_vector % dot_speed != 0
        for i in range(self.settings.list_length - len(self.vect_list)):
            vect = random.choice(self.settings.move_list)
            self.vect_list.append(vect)