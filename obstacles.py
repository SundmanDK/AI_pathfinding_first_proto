import pygame
from pygame.sprite import Sprite
class Obstacle(Sprite):
    def __init__(self, game, x, y, width, height):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.rect = pygame.Rect(
        x, y, width, height
        )

    def draw_obstacle(self):
        pygame.draw.rect(self.screen, self.settings.obstacle_color, self.rect)

class Goal(Obstacle):
    def draw_goal(self):
        pygame.draw.circle(self.screen,
                           self.settings.goal_color,
                           (self.settings.goal_pos_x, self.settings.goal_pos_y),
                           self.settings.goal_radius)