import pygame

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
BACKGROUND = (25, 25, 40)
RED = (220, 60, 60)
PLAYER_COLOR = (220, 60, 60)
BLUE = (60, 120, 220)
GREEN = (60, 200, 100)
YELLOW = (220, 200, 60)
PURPLE = (180, 80, 220)
CYAN = (60, 200, 220)
WHITE = (240, 240, 255)
LIGHT_GRAY = (180, 180, 200)
DARK_GRAY = (40, 40, 60)
MENU_BG = (35, 35, 55)
BUTTON_COLOR = (70, 100, 180)
BUTTON_HOVER = (90, 130, 220)
ROCKET_COLOR = (255, 100, 100)

# Game constants
PLAYER_SIZE = 40
OBSTACLE_MIN_SIZE = 80
OBSTACLE_MAX_SIZE = 120
MIN_SPEED = 4
MAX_SPEED = 8
SPAWN_RATE = 4.5  # obstacles per second
SCORE_PER_SECOND = 10

# Rocket constants
ROCKET_WIDTH = 10
ROCKET_HEIGHT = 30
ROCKET_SPEED = 15
MAX_ROCKETS = 3

# Difficulty settings
DIFFICULTIES = {
    "Easy": {
        "speed_multiplier": 0.7,
        "spawn_multiplier": 0.7,
        "rocket_refill_time": 3.0  # seconds
    },
    "Medium": {
        "speed_multiplier": 1.0,
        "spawn_multiplier": 1.0,
        "rocket_refill_time": 4.0  # seconds
    },
    "Hard": {
        "speed_multiplier": 1.5,
        "spawn_multiplier": 1.5,
        "rocket_refill_time": 5.0  # seconds
    }
}

# Save file
SAVE_FILE = "game_save.json"

# Initialize pygame fonts
pygame.init()
title_font = pygame.font.SysFont("Arial", 48, bold=True)
font_large = pygame.font.SysFont("Arial", 32, bold=True)
font_medium = pygame.font.SysFont("Arial", 24)
font_small = pygame.font.SysFont("Arial", 18) 