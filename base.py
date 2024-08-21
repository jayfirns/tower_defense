"""
base.py

Represents the player's base, which can be attacked by enemies and take damage. 
Handles health updates and communicates with the UIManager to update the UI.

Changes:
    • Added logic to ensure base health updates are reflected in the UI.
    • Added logic to confirm that game over is triggered when health reaches zero.

"/Users/johnfirnschild/Documents/HomeLab/Python/projects/games/tower_defense/assets/images/bases/coffee_shop_sm.png")

Author: John Firnschild
Written: 8/20/2024
Version: 0.2.112
"""

version = "0.2.112"

import pygame
from log_config import logger
import os

# Dynamically get the file name and full path using dunder __file__
file_name = os.path.basename(__file__)
full_path = os.path.abspath(__file__)

# Log the version of base.py
logger.debug("---------------------------------------------")
logger.debug("                                             ")
logger.debug(f"Running {full_path} version: {version}")
logger.debug("                                             ")
logger.debug("---------------------------------------------")

class Base:
    """
    Represents the player's base in the game, which can be attacked and take damage.
    The base is responsible for handling its own health and for updating the UI when damage occurs.

    Attributes:
        position (pygame.Vector2): The position of the base on the screen.
        health (int): The current health of the base.
        image (pygame.Surface): The sprite used to represent the base on the screen.
        rect (pygame.Rect): The rectangular area for the base's sprite.
        ui_manager (UIManager): A reference to the UIManager to update the health bar.
    """

    def __init__(self, x, y, ui_manager, max_health=500):
        """
        Initializes the base object with its position, health, and sprite.

        Args:
            x (int): The x-coordinate of the base's position.
            y (int): The y-coordinate of the base's position.
            ui_manager (UIManager): The UIManager instance used to update the base's health in the UI.
            max_health (int): The maximum health of the base.
        """
        self.position = pygame.Vector2(x, y)
        self.max_health = max_health
        self.health = self.max_health
        self.ui_manager = ui_manager
        self.image = pygame.image.load("/Users/johnfirnschild/Documents/HomeLab/Python/projects/games/tower_defense/assets/images/bases/coffee_shop_sm.png")
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))
        # Initialize UIManager with current health
        self.ui_manager.update_base_health(self.health)

    def take_damage(self, damage):
        """
        Reduces the base's health and updates the UI with the current health.
        """
        self.health = max(0, self.health - damage)  # Ensure health doesn't drop below 0
        self.ui_manager.update_base_health(self.health)  # Update the UIManager with current health
        
        if self.health == 0:
            logger.info("Base health has reached zero. Game over.")
            self.ui_manager.game_over = True

    def draw(self, screen):
        """
        Draws the base sprite on the screen.

        Args:
            screen (pygame.Surface): The surface on which to draw the base sprite.
        """
        screen.blit(self.image, self.rect)