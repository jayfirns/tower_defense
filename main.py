"""
main.py

This script sets up the game window using Pygame, runs the main game loop, 
and handles interactions between the different modules, including UI, game state, 
and input handling.

Changes:
    • Integrated the UI, game, and input modules for better code organization.
    • Delegated responsibilities to the respective modules for rendering, game logic, and input handling.
    • Implemented dynamic difficulty adjustments based on slider input.
    • Fixed missing screen argument for updating game state and passed the screen object to update functions.
    • Added difficulty slider using pygame_gui.
    • Ensured proper draw order of game entities before UI elements.
    • Integrated `AmmoManager` to handle tower projectile attacks.
    • Updated the game loop to manage and render projectiles alongside other entities.
    • Prevented interactions during the game over state and added logic to handle game reset and quit events.

Author: John Firnschild
Written: 8/20/2024
Version: 0.5.21
"""

version = "0.5.21"

import pygame
import sys
import time
import pygame_gui
from config import *
from log_config import logger
from path import Path
from ui import UIManager
from game import GameState
from input_handler import InputHandler
from ammo import AmmoManager  # Import the AmmoManager

# Dynamically get the file name and full path using dunder __file__
file_name = os.path.basename(__file__)
full_path = os.path.abspath(__file__)

# Log the version of main.py
logger.debug("---------------------------------------------")
logger.debug("                                             ")
logger.debug(f"Running {full_path} version: {version}")
logger.debug("                                             ")
logger.debug("---------------------------------------------")

# Initialize Pygame and create the game window
pygame.init()
logger.info("Pygame initialized successfully.")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Tower Defense Game")
clock = pygame.time.Clock()

# Initialize pygame_gui
ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

# Dynamically center the slider in the ribbon
slider_x_position = (RIBBON_WIDTH - SLIDER_CONFIG['slider_width']) // 2

# Create the difficulty slider
difficulty_slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
    relative_rect=pygame.Rect(slider_x_position, SLIDER_CONFIG['position_y'], 
                              SLIDER_CONFIG['slider_width'], SLIDER_CONFIG['slider_height']),
    start_value=SLIDER_CONFIG['start_value'],
    value_range=SLIDER_CONFIG['value_range'],
    manager=ui_manager
)

# Font for slider labels
slider_font = pygame.font.SysFont(None, RIBBON_SMALL_FONT_SIZE)

# Initialize the game world with random waypoints in the path
path = Path(num_waypoints=5)  # Create the path with randomized waypoints
game_state = GameState(path)  # Create the game state manager
input_handler = InputHandler(game_state)  # Handle user inputs
ammo_manager = AmmoManager()  # Initialize the AmmoManager
custom_ui_manager = UIManager()  # Manage the custom UI elements

def main():
    """
    Main function to run the game loop. Handles events, updates the game state,
    and renders graphics to the screen.
    """
    logger.debug("Entering the main game loop.")
    
    running = True
    difficulty_level = 'Medium'  # Set the default difficulty level

    # Track the previous slider value to avoid constant updates
    previous_slider_value = difficulty_slider.get_current_value()

    while running:
        try:
            # Get the delta time for pygame_gui updates
            time_delta = clock.tick(FPS) / 1000.0

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                # Process events for pygame_gui
                ui_manager.process_events(event)

                # If the game is over, only allow interaction with the game over screen
                if game_state.game_over:
                    # Handle game over screen input
                    # Ensure passage of the correct path object
                    custom_ui_manager.handle_game_over_input(event, game_state, path)
                else:
                    # Handle other game events
                    input_handler.handle_event(event)

                    # Pass event to UIManager for slider handling
                    # Comment this out if not needed
                    # custom_ui_manager.handle_slider_event(event)
                    pass

            # Update pygame_gui manager
            ui_manager.update(time_delta)

            # Clear the screen at the start
            screen.fill(BACKGROUND_COLOR)

            # If the game is over, render the game over screen and stop further updates
            if game_state.game_over:
                custom_ui_manager.render_game_over_screen(screen)
            else:
                # Get the current value of the slider
                slider_value = difficulty_slider.get_current_value()

                # Adjust the difficulty only if the slider value has changed
                if slider_value != previous_slider_value:
                    if slider_value == 1:
                        difficulty_level = 'Easy'
                    elif slider_value == 2:
                        difficulty_level = 'Medium'
                    elif slider_value == 3:
                        difficulty_level = 'Hard'
                    elif slider_value == 4:
                        difficulty_level = 'Spicy'
                    elif slider_value == 5:
                        difficulty_level = 'Hell'

                    logger.debug(f"Adjusting difficulty to {difficulty_level}.")
                    game_state.adjust_difficulty(difficulty_level)

                    # Update previous_slider_value to avoid repeated changes
                    previous_slider_value = slider_value

                # Update the game state with the current time and difficulty level
                game_state.update(time.time(), screen, difficulty_level)

                # Draw the game entities first (towers, enemies)
                for tower in game_state.towers:
                    tower.draw(screen)

                for enemy in game_state.spawner.enemies:
                    enemy.draw(screen)

                # Draw the projectiles (ammo) after towers and enemies
                ammo_manager.draw(screen)  # Ensure projectiles appear above game entities

                # Draw the custom UI (ribbon, score, etc.)
                custom_ui_manager.render_ribbon(
                    screen, 
                    game_state.score, 
                    game_state.selected_tower_type, 
                    num_light_towers=len([t for t in game_state.towers if t.name == "Light"]),
                    num_heavy_towers=len([t for t in game_state.towers if t.name == "Heavy"]),
                    num_enemies=len(game_state.spawner.enemies),
                    base_health=game_state.base.health,  # Pass the base health to the UI
                    max_health=game_state.base.max_health  # Pass the max health to the UI
                )

                # Draw the heavy tower message
                custom_ui_manager.render_heavy_tower_message(screen, game_state.score)

                # Render the slider and labels via UIManager
                # Comment this line out if not needed
                # custom_ui_manager.render_difficulty_slider(screen)

            # Now draw the pygame_gui elements (slider)
            ui_manager.draw_ui(screen)

            # Update the display
            pygame.display.flip()

        except Exception as e:
            logger.error("An unexpected error occurred during the game loop: %s", str(e), exc_info=True)
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()  # Run the main game loop if this script is executed directly