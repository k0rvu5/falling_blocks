import pygame
import random
import json
import os
import sys
from pygame.locals import *
from constants import WIDTH, HEIGHT
from game import Game
from menu import Menu

def initialize_pygame():
    """Initialize pygame and its subsystems."""
    pygame.init()
    pygame.mixer.init()

def create_starfield():
    """Create the starry background effect."""
    stars = []
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.uniform(0.5, 2)
        speed = random.uniform(0.2, 0.8)
        stars.append([x, y, size, speed])
    return stars

def handle_keyboard_input(game, current_screen):
    """Handle keyboard input for game controls."""
    if current_screen == "game" and not game.paused and not game.game_over:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        # Horizontal movement
        if keys[K_h] or keys[K_LEFT]:
            dx -= 1
        if keys[K_l] or keys[K_RIGHT]:
            dx += 1
            
        # Vertical movement
        if keys[K_k] or keys[K_UP]:
            dy -= 1
        if keys[K_j] or keys[K_DOWN]:
            dy += 1
        
        # Mouse movement
        if pygame.mouse.get_focused():
            mouse_pos = pygame.mouse.get_pos()
            game.player.move_to_mouse(mouse_pos)
        game.player.move(dx, dy)

def handle_events(game, menu, current_screen):
    """Handle pygame events and return the next screen state."""
    for event in pygame.event.get():
        if event.type == QUIT:
            return "quit"
            
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                if current_screen == "game":
                    pygame.event.set_grab(False)
                    pygame.mixer.music.stop()
                    return "menu"
                return "quit"
                    
            if event.key == K_p and current_screen == "game":
                if game.paused:
                    pygame.mouse.set_pos(game.player.x + game.player.size // 2, 
                                       game.player.y + game.player.size // 2)
                game.paused = not game.paused
                    
            if event.key == K_SPACE:
                if current_screen == "game" and not game.paused and not game.game_over:
                    game.fire_rocket()
                elif current_screen == "game" and game.game_over:
                    game.reset()
                
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and current_screen == "game" and not game.paused and not game.game_over:
                game.fire_rocket()
                
        if current_screen == "menu":
            result = menu.handle_event(event)
            if result:
                if result == "game":
                    game.reset()
                    pygame.mixer.music.play(-1)
                    pygame.event.set_grab(True)
                return result
                
    return current_screen

def main():
    # Initialize pygame and create window
    initialize_pygame()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Falling Squares Game")
    
    # Create game objects
    stars = create_starfield()
    game = Game()
    game.stars = stars
    menu = Menu(game)
    
    # Game loop variables
    clock = pygame.time.Clock()
    current_screen = "menu"
    running = True
    
    # Main game loop
    while running:
        # Handle events
        current_screen = handle_events(game, menu, current_screen)
        if current_screen == "quit":
            running = False
            continue
            
        # Handle keyboard input
        handle_keyboard_input(game, current_screen)
        
        # Update game state
        if current_screen == "game":
            game.update()
        
        # Draw current screen
        if current_screen == "menu":
            menu.draw(screen)
        else:
            game.draw(screen)

        # Update cursor visibility
        pygame.mouse.set_visible(current_screen != "game")

        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
