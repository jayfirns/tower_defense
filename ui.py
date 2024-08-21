"""
ui.py

Manages the UI rendering of the game, including the ribbon, score display, notifications, difficulty slider,
base health bar, and the game over screen.

Changes:
    • Added debug logging to track health bar updates and rendering.
    • Removed direct reference to max_base_health, now receiving updates from Base class.

Author: John Firnschild
Written: 8/20/2024
Version: 0.2.318
"""

version = "0.2.318"

import pygame
from config import *
from log_config import logger
import sys
import os

# Dynamically get the file name and full path using dunder __file__
file_name = os.path.basename(__file__)
full_path = os.path.abspath(__file__)

# Log the version of ui.py
logger.debug("---------------------------------------------")
logger.debug("                                             ")
logger.debug(f"Running {full_path} version: {version}")
logger.debug("                                             ")
logger.debug("---------------------------------------------")


class UIManager:
    """
    Manages the user interface of the game, including rendering the ribbon, score display, tower counts,
    difficulty slider, base health bar, and the game over screen.

    Attributes:
        slider_rect (pygame.Rect): The rectangle representing the difficulty slider.
        slider_position (int): The current position of the slider (0 to 4, corresponding to difficulty levels).
        difficulty_levels (list): The list of difficulty levels available for the player to select.
        current_base_health (int): The current health of the player's base.
    """

    def __init__(self):
        """
        Initializes the UI manager, setting up the slider, difficulty levels, and base health tracking.
        """
        self.slider_rect = pygame.Rect(RIBBON_PADDING, SCREEN_HEIGHT - 100, RIBBON_WIDTH - (2 * RIBBON_PADDING), 20)
        self.slider_position = 1  # Initialize slider position (1: Medium difficulty)
        self.difficulty_levels = ["Easy", "Medium", "Hard", "Spicy", "Hell"]  # Difficulty levels

        self.current_base_health = 0  # Initialize current health to 0
        self.game_over = False  # Track game over state

        logger.info("UI Manager initialized.")

    # Render Ribbon method with explicit health sync
    def render_ribbon(self, screen, score, selected_tower_type, num_light_towers, num_heavy_towers, num_enemies, base_health, max_health):
        """
        Renders the ribbon UI on the left side of the screen, displaying the player's score, tower counts,
        enemy counts, and the base health bar.

        Args:
            screen (pygame.Surface): The surface to render the UI on.
            score (int): The player's current score.
            selected_tower_type (str): The tower type currently selected by the player.
            num_light_towers (int): The number of light towers the player has.
            num_heavy_towers (int): The number of heavy towers the player has.
            num_enemies (int): The current number of enemies on the field.
            base_health (int): The current health of the base.
            max_health (int): The maximum health of the base (received from Base class).
        """
        logger.debug(f"Rendering ribbon UI with score: {score}, selected tower: {selected_tower_type}, "
                     f"light towers: {num_light_towers}, heavy towers: {num_heavy_towers}, enemies: {num_enemies}")

        # Sync the latest base health before rendering
        self.current_base_health = base_health  

        ribbon_x, ribbon_y = 0, 0
        pygame.draw.rect(screen, (0, 0, 0), (ribbon_x, ribbon_y, RIBBON_WIDTH, SCREEN_HEIGHT))
        pygame.draw.rect(screen, (255, 255, 255), (ribbon_x, ribbon_y, RIBBON_WIDTH, SCREEN_HEIGHT), RIBBON_BORDER_THICKNESS)

        font = pygame.font.SysFont(None, RIBBON_FONT_SIZE)
        small_font = pygame.font.SysFont(None, RIBBON_SMALL_FONT_SIZE)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        selection_text = font.render(f"Selected Tower: {selected_tower_type}", True, (255, 255, 255))

        screen.blit(score_text, (ribbon_x + RIBBON_PADDING, ribbon_y + RIBBON_PADDING))
        screen.blit(selection_text, (ribbon_x + RIBBON_PADDING, ribbon_y + RIBBON_PADDING + score_text.get_height() + 10))

        enemy_count_text = small_font.render(f"Enemies: {num_enemies}", True, (255, 255, 255))
        light_tower_count_text = small_font.render(f"Light Towers: {num_light_towers}", True, (255, 255, 255))
        heavy_tower_count_text = small_font.render(f"Heavy Towers: {num_heavy_towers}", True, (255, 255, 255))

        screen.blit(enemy_count_text, (ribbon_x + RIBBON_PADDING, ribbon_y + 80))
        screen.blit(light_tower_count_text, (ribbon_x + RIBBON_PADDING, ribbon_y + 100))
        screen.blit(heavy_tower_count_text, (ribbon_x + RIBBON_PADDING, ribbon_y + 120))

        # Render the base health bar with the provided base health and max health
        self.render_base_health_bar(screen, max_health)

    # Render Base Health Bar method with proper ratio calculation
    def render_base_health_bar(self, screen, max_health):
        """
        Renders the base health bar based on the current health and max health received from the Base class.

        Args:
            screen (pygame.Surface): The surface to render the health bar on.
            max_health (int): The maximum health of the base (provided by Base class).
        """
        bar_x, bar_y = 10, SCREEN_HEIGHT - 150
        bar_width = RIBBON_WIDTH - 20
        bar_height = 20

        # Calculate the health ratio based on current health and max health
        health_ratio = max(0, min(self.current_base_health / max_health, 1))

        red_value = int(255 * (1 - health_ratio))
        green_value = int(255 * health_ratio)
        health_color = (max(0, min(red_value, 255)), max(0, min(green_value, 255)), 0)

        filled_width = bar_width * health_ratio

        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, filled_width, bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

        logger.info(f"Rendered base health bar at position ({bar_x}, {bar_y}) with width {filled_width} and color {health_color}")

    # Update Base Health method
    def update_base_health(self, new_health):
        """
        Updates the current health value of the base for rendering purposes.

        Args:
            new_health (int): The new health value to be applied to the base.
        """
        self.current_base_health = new_health
        logger.info(f"Base health updated to {self.current_base_health}")


    def render_heavy_tower_message(self, screen, score):
        """
        Renders a message in the ribbon when heavy towers become available, based on the player's score.
        
        Args:
            screen (pygame.Surface): The surface where the message will be drawn.
            score (int): The player's current score, used to determine when to display the message.
        """
        small_font = pygame.font.SysFont(None, RIBBON_SMALL_FONT_SIZE)
        
        if score >= 20:
            heavy_tower_text = small_font.render("2 Heavy Towers Available!", True, (255, 255, 0))
        elif score >= 10:
            heavy_tower_text = small_font.render("Heavy Tower Available!", True, (255, 255, 0))
        else:
            heavy_tower_text = None

        if heavy_tower_text:
            screen.blit(heavy_tower_text, (RIBBON_PADDING, 150))
            logger.debug(f"Displayed heavy tower message based on score: {score}")

    def render_game_over_screen(self, screen):
        """
        Renders the game over screen with options for "Play Again" and "Quit."

        This method renders a centered "Game Over" message along with two buttons:
        "Play Again" and "Quit". The player can interact with these options to either
        restart the game or exit the game.

        Args:
            screen (pygame.Surface): The surface where the game over screen will be drawn.
        """
        # Define the font for the game over text and buttons
        game_over_font = pygame.font.SysFont(None, 72)
        button_font = pygame.font.SysFont(None, 48)

        # Render the "Game Over" text and center it
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(game_over_text, game_over_rect)

        logger.debug(f"Rendered 'Game Over' text at position: {game_over_rect.topleft}")

        # Render the "Play Again" button and center it
        play_again_text = button_font.render("Play Again", True, (255, 255, 255))
        play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        pygame.draw.rect(screen, (0, 0, 0), play_again_rect.inflate(20, 10))  # Draw button background
        screen.blit(play_again_text, play_again_rect)

        logger.debug(f"Rendered 'Play Again' button at position: {play_again_rect.topleft}")

        # Render the "Quit" button and center it below the "Play Again" button
        quit_text = button_font.render("Quit", True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        pygame.draw.rect(screen, (0, 0, 0), quit_rect.inflate(20, 10))  # Draw button background
        screen.blit(quit_text, quit_rect)

        logger.debug(f"Rendered 'Quit' button at position: {quit_rect.topleft}")

        logger.debug("Finished rendering game over screen.")

    def handle_game_over_input(self, event, game_state, path):
        """
        Handles user input for the game over screen, allowing the player to either play again or quit.

        Args:
            event (pygame.event.Event): The event triggered by user input.
            game_state (GameState): The current game state instance, used for restarting the game.
            path (Path): The path instance to be passed to the reset_game method.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Define the "Play Again" button area
            play_again_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30, 200, 60)
            # Define the "Quit" button area
            quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 60)

            if play_again_button_rect.collidepoint(mouse_pos):
                logger.info("Play Again button clicked.")
                game_state.reset_game(path)  # Reset the game state and pass the path

            elif quit_button_rect.collidepoint(mouse_pos):
                logger.info("Quit button clicked.")
                pygame.quit()  # Quit the game and close the window
                sys.exit()