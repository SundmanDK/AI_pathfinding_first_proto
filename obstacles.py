import pygame
from pygame.sprite import Sprite


class Obstacle(Sprite):  # Subclass of pygame's Sprite class.
    """Objects used to block the way for the dot or the goal. Boundaries for the game and walls on the screen."""
    def __init__(self, game, x, y, width, height, color):
        """Initial process. Links to screen and settings. Makes the object."""
        super().__init__()
        self.settings = game.settings  # Connection to the instance of settings through the Game class.
        self.screen = game.screen  # Connection to the screen through the Game class.
        # Hitbox. Dot being a subclass of the Sprite lets us use the pygame rect object as a hitbox using sprite.groupcollide()
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color  # receives a color, red for walls and boundaries, green for the goal.

    def draw_obstacle(self):
        """Draws the obstacle."""
        pygame.draw.rect(self.screen, self.color, self.rect)
