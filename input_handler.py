"""
input_handler.py

Handles user input for tower selection, placement, and other interactions.
This module processes events such as mouse clicks and key presses, 
allowing the player to interact with the game.

Changes:
    • Integrated logging to track input events and user actions.

Author: John Firnschild
Written: 8/18/2024
Version: 0.1.11
"""
version = "0.1.11"

import pygame
from log_config import logger
import os

# Dynamically get the file name and full path using dunder __file__
file_name = os.path.basename(__file__)
full_path = os.path.abspath(__file__)

# Log the version of input_handler.py
logger.debug("---------------------------------------------")
logger.debug("                                             ")
logger.debug(f"Running {full_path} version: {version}")
logger.debug("                                             ")
logger.debug("---------------------------------------------")

class InputHandler:
    def __init__(self, game_state):
        self.game_state = game_state
        # logger.info("InputHandler initialized.")

    def handle_event(self, event):
        """
        Processes a single Pygame event and triggers the appropriate action 
        based on the event type.

        Args:
            event (pygame.event.Event): The event to process.
        """
        if event.type == pygame.QUIT:
            logger.debug("Quit event detected. Exiting the game.")
            pygame.quit()
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Left-click to place tower
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.game_state.place_tower(mouse_x, mouse_y)
            logger.debug(f"Mouse click detected at ({mouse_x}, {mouse_y}).")

        elif event.type == pygame.KEYDOWN:
            # Select tower type using keys 1 and 2
            if event.key == pygame.K_1:
                self.game_state.selected_tower_type = "Light"
                logger.debug("Selected Light Tower")
            elif event.key == pygame.K_2 and self.game_state.score >= 10:
                self.game_state.selected_tower_type = "Heavy"
                logger.debug("Selected Heavy Tower")

    def handle_difficulty_slider(self, difficulty_level):
        """
        Adjusts the game's difficulty based on the slider selection.

        Args:
            difficulty_level (str): The difficulty level selected by the player ('Easy', 'Medium', 'Hard').
        """
        self.game_state.adjust_difficulty(difficulty_level)
        logger.info(f"Difficulty level changed to {difficulty_level}")