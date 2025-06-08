import pygame
from constants import (
    WIDTH, HEIGHT, MENU_BG, WHITE, LIGHT_GRAY, CYAN, YELLOW,
    title_font, font_large, font_medium, font_small, DIFFICULTIES
)
from button import Button

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
        import sys
        sys.exit()
        
    def draw(self, surface):
        # Draw background
        surface.fill(MENU_BG)
        
        # Draw stars
        for star in self.game.stars:
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
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.check_hover(event.pos)
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                result = button.handle_event(event)
                if result:
                    return result
        return "menu" 