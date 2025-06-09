import pygame
from constants import ROCKET_WIDTH, ROCKET_HEIGHT, ROCKET_SPEED, ROCKET_COLOR, WHITE

class Rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = ROCKET_WIDTH
        self.height = ROCKET_HEIGHT
        self.speed = ROCKET_SPEED
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def update(self):
        """Update rocket position and return True if rocket is off screen."""
        self.y -= self.speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return self.y + self.height < 0
        
    def draw(self, surface):
        """Draw the rocket on the surface."""
        # Draw rocket body
        pygame.draw.rect(surface, ROCKET_COLOR, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        # Draw rocket flame
        flame_points = [
            (self.x, self.y + self.height),
            (self.x - 5, self.y + self.height + 10),
            (self.x + self.width + 5, self.y + self.height + 10)
        ]
        pygame.draw.polygon(surface, (255, 200, 100), flame_points)
        pygame.draw.polygon(surface, WHITE, flame_points, 1)
        
    