import pygame
from pygame.sprite import Sprite
class Obstacle(Sprite):
    """
    Objects used to block the way for the dot or be the goal.
    Boundaries for the game and walls on the screen.
    """
    def __init__(self, game, x, y, width, height, color):
        """
        Initial process.
        Links to screen and settings.
        Makes the object.
        """
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw_obstacle(self):
        """Draws the obstacle."""
        pygame.draw.rect(self.screen, self.color, self.rect)
