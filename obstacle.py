import pygame
import random
from constants import WIDTH, OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE, MIN_SPEED, MAX_SPEED, DIFFICULTIES, BLUE, GREEN, YELLOW, PURPLE, CYAN, WHITE

class Obstacle:
    def __init__(self, difficulty="Medium"):
        self.size = random.randint(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE)
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.speed = random.uniform(MIN_SPEED, MAX_SPEED) * DIFFICULTIES[difficulty]["speed_multiplier"]
        
        # Choose a random color from the palette
        colors = [BLUE, GREEN, YELLOW, PURPLE, CYAN]
        self.color = random.choice(colors)
        
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
    def update(self):
        self.y += self.speed
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        return self.y > WIDTH
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2) 