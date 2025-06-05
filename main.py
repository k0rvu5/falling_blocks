import pygame
import random
import json
import os
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Squares Game")

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

# Game constants
PLAYER_SIZE = 40
OBSTACLE_MIN_SIZE = 80
OBSTACLE_MAX_SIZE = 120
MIN_SPEED = 4
MAX_SPEED = 8
SPAWN_RATE = 4.5  # obstacles per second
SCORE_PER_SECOND = 10

# Difficulty settings
DIFFICULTIES = {
    "Easy": {"speed_multiplier": 0.7, "spawn_multiplier": 0.7},
    "Medium": {"speed_multiplier": 1.0, "spawn_multiplier": 1.0},
    "Hard": {"speed_multiplier": 1.5, "spawn_multiplier": 1.5}
}

# Save file
SAVE_FILE = "game_save.json"

# Generate starry background
stars = []
for _ in range(100):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.uniform(0.5, 2)
    speed = random.uniform(0.2, 0.8)
    stars.append([x, y, size, speed])

try:
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
except pygame.error as e:
    print(f"Could not load music: {e}")
    # Fallback: create silent music to prevent errors
    silent_sound = pygame.mixer.Sound(buffer=bytearray([0]*44))
    pygame.mixer.music = silent_sound


# Fonts
title_font = pygame.font.SysFont("Arial", 48, bold=True)
font_large = pygame.font.SysFont("Arial", 32, bold=True)
font_medium = pygame.font.SysFont("Arial", 24)
font_small = pygame.font.SysFont("Arial", 18)

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        
    def draw(self, surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)
        
        text_surf = font_medium.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.action:
                return self.action()
        return None

class Player:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.size = PLAYER_SIZE
        self.speed = 5
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
        return self.y > HEIGHT
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)

class Game:
    def __init__(self):
        self.reset()
        self.load_settings()
        try:
            pygame.mixer.music.load("background_music.mp3")
            pygame.mixer.music.set_volume(0.5)
        except:
            pass

        
    def reset(self):
        self.player = Player()
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.paused = False
        self.last_spawn_time = pygame.time.get_ticks()
        self.start_time = pygame.time.get_ticks()
        pygame.mixer.music.play(-1)  # Loop indefinitely
        
    def load_settings(self):
        self.difficulty = "Medium"
        self.high_score = 0
        
        # Try to load from save file
        try:
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, "r") as f:
                    data = json.load(f)
                    self.difficulty = data.get("difficulty", "Medium")
                    self.high_score = data.get("high_score", 0)
        except:
            pass  # If loading fails, use defaults
        
    def save_settings(self):
        data = {
            "difficulty": self.difficulty,
            "high_score": self.high_score
        }
        try:
            with open(SAVE_FILE, "w") as f:
                json.dump(data, f)
        except:
            pass  # If saving fails, ignore
        
    def spawn_obstacle(self):
        current_time = pygame.time.get_ticks()
        spawn_rate = SPAWN_RATE * DIFFICULTIES[self.difficulty]["spawn_multiplier"]
        
        if current_time - self.last_spawn_time > 1000 / spawn_rate:
            self.obstacles.append(Obstacle(self.difficulty))
            self.last_spawn_time = current_time
            
    def update(self):
        if self.game_over or self.paused:
            return
            
        # Update score based on time survived
        elapsed_seconds = (pygame.time.get_ticks() - self.start_time) / 1000
        self.score = int(elapsed_seconds * SCORE_PER_SECOND)
        
        # Spawn new obstacles
        self.spawn_obstacle()
        
        # Update obstacles
        for obstacle in self.obstacles[:]:
            if obstacle.update():
                self.obstacles.remove(obstacle)
                
            # Check collision
            if self.player.rect.colliderect(obstacle.rect):
                self.game_over = True
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_settings()
                    
    def draw(self, surface):
        # Draw starry background
        surface.fill(BACKGROUND)
        
        # Draw stars
        for star in stars:
            x, y, size, speed = star
            # Update star position (create parallax effect)
            y += speed * 0.1
            if y > HEIGHT:
                y = 0
                x = random.randint(0, WIDTH)
            star[1] = y
            
            pygame.draw.circle(surface, WHITE, (int(x), int(y)), size)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(surface)
            
        # Draw player
        self.player.draw(surface)
        
        # Draw score
        score_text = font_large.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_text, (20, 20))
        
        # Draw high score
        hs_text = font_medium.render(f"High Score: {self.high_score}", True, LIGHT_GRAY)
        surface.blit(hs_text, (20, 60))
        
        # Draw difficulty
        diff_text = font_medium.render(f"Difficulty: {self.difficulty}", True, LIGHT_GRAY)
        surface.blit(diff_text, (WIDTH - diff_text.get_width() - 20, 20))
        
        # Draw game over message
        if self.game_over:
            pygame.mixer.music.stop()
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))
            
            game_over_text = title_font.render("GAME OVER", True, RED)
            surface.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 80))
            
            final_score = font_large.render(f"Final Score: {self.score}", True, WHITE)
            surface.blit(final_score, (WIDTH//2 - final_score.get_width()//2, HEIGHT//2))
            
            restart_text = font_medium.render("Press SPACE to restart or ESC for menu", True, LIGHT_GRAY)
            surface.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 60))
        
        # Draw pause message
        if self.paused:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))
            
            pause_text = title_font.render("PAUSED", True, YELLOW)
            surface.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 40))
            
            continue_text = font_medium.render("Press P to continue", True, LIGHT_GRAY)
            surface.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 20))

class Menu:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.create_buttons()
        
    def create_buttons(self):
        button_width = 300
        button_height = 60
        button_spacing = 10
        start_y = HEIGHT // 2 - 100
        
        # Play button
        self.buttons.append(
            Button(WIDTH//2 - button_width//2, start_y, 
                   button_width, button_height, "Play Game", self.start_game)
        )
        
        # Difficulty button
        self.buttons.append(
            Button(WIDTH//2 - button_width//2, start_y + button_height + button_spacing, 
                   button_width, button_height, f"Difficulty: {self.game.difficulty}", self.toggle_difficulty)
        )
        
        # Quit button
        self.buttons.append(
            Button(WIDTH//2 - button_width//2, start_y + 2*(button_height + button_spacing), 
                   button_width, button_height, "Quit Game", self.quit_game)
        )
        
    def start_game(self):
        return "game"
    
    def toggle_difficulty(self):
        difficulties = list(DIFFICULTIES.keys())
        current_index = difficulties.index(self.game.difficulty)
        self.game.difficulty = difficulties[(current_index + 1) % len(difficulties)]
        self.game.save_settings()
        self.create_buttons()  # Recreate buttons to update difficulty text
        return "menu"
    
    def quit_game(self):
        pygame.quit()
        sys.exit()
        
    def draw(self, surface):
        # Draw background
        surface.fill(MENU_BG)
        
        # Draw stars
        for star in stars:
            x, y, size, speed = star
            pygame.draw.circle(surface, WHITE, (int(x), int(y)), size)
        
        # Draw title
        title_text = title_font.render("FALLING SQUARES", True, CYAN)
        surface.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 90))
        
        subtitle_text = font_medium.render("Avoid the falling squares!", True, LIGHT_GRAY)
        surface.blit(subtitle_text, (WIDTH//2 - subtitle_text.get_width()//2, 150))
        
        # Draw high score
        hs_text = font_large.render(f"High Score: {self.game.high_score}", True, YELLOW)
        surface.blit(hs_text, (WIDTH//2 - hs_text.get_width()//2, 220))
        
        # Draw controls
        controls = [
            "Controls:",
            "Move - Mouse or HJKL keys",
            "Pause - P key",
            "Menu - ESC key"
        ]
        
        for i, line in enumerate(controls):
            ctrl_text = font_small.render(line, True, LIGHT_GRAY)
            surface.blit(ctrl_text, (WIDTH//2 - ctrl_text.get_width()//2, 420 + i*30))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
        
        # Draw footer
        footer_text = font_small.render("Created with PyGame", True, LIGHT_GRAY)
        surface.blit(footer_text, (WIDTH//2 - footer_text.get_width()//2, HEIGHT - 40))

    def handle_event(self, event):
        if event.type == MOUSEMOTION:
            for button in self.buttons:
                button.check_hover(event.pos)
                
        if event.type == MOUSEBUTTONDOWN:
            for button in self.buttons:
                result = button.handle_event(event)
                if result:
                    return result
        return "menu"

def main():
    clock = pygame.time.Clock()
    game = Game()
    menu = Menu(game)
    
    current_screen = "menu"  # "menu" or "game"
    
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if current_screen == "game":
                        pygame.event.set_grab(False)
                        pygame.mixer.music.stop()
                        current_screen = "menu"
                    else:
                        running = False
                        
                if event.key == K_p and current_screen == "game":
                    game.paused = not game.paused
                    
                if event.key == K_SPACE and current_screen == "game" and game.game_over:
                    game.reset()
                    
            if current_screen == "menu":
                result = menu.handle_event(event)
                if result:
                    if result == "game":
                        pygame.mixer.music.play(-1)  # Loop indefinitely
                        pygame.event.set_grab(True)
                    current_screen = result
                    
        # Handle keyboard movement
        if current_screen == "game" and not game.paused and not game.game_over:
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[K_h] or keys[K_LEFT]:
                dx -= 1
            if keys[K_l] or keys[K_RIGHT]:
                dx += 1
            if keys[K_k] or keys[K_UP]:
                dy -= 1
            if keys[K_j] or keys[K_DOWN]:
                dy += 1
            
            # Mouse movement
            if pygame.mouse.get_focused():
                mouse_pos = pygame.mouse.get_pos()
                game.player.move_to_mouse(mouse_pos)
            game.player.move(dx, dy)
        
        # Update game
        if current_screen == "game":
            game.update()
        
        # Draw current screen
        if current_screen == "menu":
            menu.draw(screen)
        else:
            game.draw(screen)

        # Hide cursor when in gameplay, show in menu
        pygame.mouse.set_visible(current_screen != "game")

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
