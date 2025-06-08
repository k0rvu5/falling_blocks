import pygame
import json
import os
import random
from constants import (
    WIDTH, HEIGHT, BACKGROUND, WHITE, LIGHT_GRAY, RED, YELLOW,
    SPAWN_RATE, SCORE_PER_SECOND, DIFFICULTIES, SAVE_FILE,
    title_font, font_large, font_medium
)
from player import Player
from obstacle import Obstacle

class Game:
    def __init__(self):
        try:
            pygame.mixer.music.load("background_music.mp3")
            pygame.mixer.music.set_volume(0.5)
        except:
            pass
        self.reset()
        self.load_settings()

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
        for star in self.stars:
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