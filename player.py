import pygame
from constants import WIDTH, HEIGHT, PLAYER_SIZE, PLAYER_COLOR, WHITE

class Player:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.size = PLAYER_SIZE
        self.speed = 15
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
    def move(self, dx, dy):
        self.x = max(0, min(WIDTH - self.size, self.x + dx * self.speed))
        self.y = max(0, min(HEIGHT - self.size, self.y + dy * self.speed))
        pygame.mouse.set_pos(self.x + self.size // 2, self.y + self.size // 2)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
    def move_to_mouse(self, pos):
        self.x = max(0, min(WIDTH - self.size, pos[0] - self.size//2))
        self.y = max(0, min(HEIGHT - self.size, pos[1] - self.size//2))
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        # Draw player details
        pygame.draw.rect(surface, (200, 200, 230), 
                        (self.x + self.size//4, self.y + self.size//4, 
                         self.size//2, self.size//2)) 