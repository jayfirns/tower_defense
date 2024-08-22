"""
tower.py

Defines the Tower class which will be used to represent towers in the game,
with different types (Light and Heavy), each having unique properties.

Changes:

    • Improved range detection and shooting logic.
    • Added logging to validate positions of towers when they are placed and drawn.
    • Ensured that towers are being drawn within the visible screen area.
    • Introduced checks to avoid drawing or creating towers off-screen.
    • Refined the shooting mechanism for clarity and consistency.
    • Incorporated checks to ensure towers are placed only within the playable game space.
    • Integrated `AmmoManager` to handle projectile-based tower attacks.
    • Updated the shoot method to create ammo instead of directly applying damage.
    • Replaced circle drawing with sprite-based rendering for the Light and Heavy towers.

Author: John Firnschild
Written: 8/20/2024
Version: 0.3.2
"""

version = "0.3.2"

import pygame
from log_config import logger
import os
import config  # Importing config to use PLAYABLE_AREA_START_X and PLAYABLE_AREA_WIDTH

# Dynamically get the file name and full path using dunder __file__
file_name = os.path.basename(__file__)
full_path = os.path.abspath(__file__)

# Log the version of tower.py
logger.debug("---------------------------------------------")
logger.debug("                                             ")
logger.debug(f"Running {full_path} version: {version}")
logger.debug("                                             ")
logger.debug("---------------------------------------------")


class Tower:
    def __init__(self, x, y, name="Light"):
        """
        Initializes a tower object with position, range, fire rate, damage, and a sprite based on its type (name).

        Args:
            x (int): The x-coordinate of the tower's position.
            y (int): The y-coordinate of the tower's position.
            name (str): The type of the tower ("Light" or "Heavy").
        """
        # Create better path to the sprite
        sprite_path_heavy = os.path.join('assets', 'images', 'towers', 'ufo_1.png')
        sprite_path_light = os.path.join('assets', 'images', 'towers', 'missle_launcher_2.png')
        self.position = pygame.Vector2(x, y)
        self.name = name

        # Load the appropriate sprite for the tower
        if self.name == "Heavy":
            self.sprite = pygame.image.load(sprite_path_heavy)
            self.range = 200
            self.fire_rate = 1.5  # Fire every 1.5 seconds
            self.damage = 30
            self.cost = 10  # Cost in points
        else:  # Default to Light tower
            self.sprite = pygame.image.load(sprite_path_light)
            self.range = 150
            self.fire_rate = 1  # Fire every 1 second
            self.damage = 25
            self.cost = 0  # Light towers are free or cost very little

        # Scale the sprite to a uniform size
        self.sprite = pygame.transform.scale(self.sprite, (40, 40))

        # Create a rect for positioning the sprite
        self.rect = self.sprite.get_rect(center=(x, y))

        self.last_shot_time = 0  # Track the last time the tower fired

        # Log tower creation with position check to ensure it's within the playable area
        if config.PLAYABLE_AREA_START_X <= x <= config.PLAYABLE_AREA_START_X + config.PLAYABLE_AREA_WIDTH and 0 <= y <= config.SCREEN_HEIGHT:
            logger.debug(f"{self.name} Tower created at position: ({x}, {y}) with range: {self.range}, fire rate: {self.fire_rate}, damage: {self.damage}, cost: {self.cost}")
        else:
            logger.warning(f"{self.name} Tower created at an invalid position: ({x}, {y}). This may be outside the playable area.")

    def detect_enemies(self, enemies):
        """
        Detects enemies within the tower's range and prioritizes the closest one.

        Args:
            enemies (list): A list of enemy objects to check.

        Returns:
            tuple: A list of enemies within range and the closest enemy.
        """
        enemies_in_range = []
        closest_enemy = None
        closest_distance = float('inf')

        for enemy in enemies:
            distance = self.position.distance_to(enemy.current_position)
            if distance <= self.range:
                enemies_in_range.append(enemy)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_enemy = enemy
                logger.debug(f"Enemy detected within range at distance: {distance}")

        return enemies_in_range, closest_enemy

    def shoot(self, enemies, current_time, ammo_manager):
        """
        Shoots at the prioritized enemy in range if the tower's fire rate allows it,
        and creates a projectile (ammo) instead of directly applying damage.

        Args:
            enemies (list): A list of enemy objects to target.
            current_time (float): The current time in seconds.
            ammo_manager (AmmoManager): The manager responsible for handling ammo.
        """
        if current_time - self.last_shot_time >= self.fire_rate:
            enemies_in_range, closest_enemy = self.detect_enemies(enemies)
            if closest_enemy:
                # Create a projectile (ammo) that travels towards the closest enemy
                ammo_manager.shoot(self.position, closest_enemy, speed=16, damage=self.damage)
                self.last_shot_time = current_time
                logger.debug(f"{self.name} Tower fired at enemy, creating a projectile.")
            else:
                logger.debug(f"{self.name} Tower found no enemies within range to shoot at.")
        else:
            logger.debug(f"{self.name} Tower is waiting for fire rate cooldown.")

    def draw(self, screen, is_selected=False):
        """
        Draws the tower's sprite on the screen. Optionally, draws the range if the tower is selected.

        Args:
            screen (pygame.Surface): The game screen surface where the tower will be drawn.
            is_selected (bool): Whether the tower is selected and its range should be displayed.
        """
        # Ensure the tower is within the playable area before drawing
        if config.PLAYABLE_AREA_START_X <= self.position.x <= config.PLAYABLE_AREA_START_X + config.PLAYABLE_AREA_WIDTH and 0 <= self.position.y <= config.SCREEN_HEIGHT:
            # Draw the tower sprite
            screen.blit(self.sprite, self.rect.topleft)
            
            # Optionally draw the tower range if selected
            if is_selected:
                pygame.draw.circle(screen, (0, 0, 255), (int(self.position.x), int(self.position.y)), self.range, 1)
            logger.debug(f"Drawing {self.name} Tower at position: ({self.position.x}, {self.position.y})")
        else:
            logger.warning(f"Attempting to draw {self.name} Tower at an off-screen or out-of-bounds position: ({self.position.x}, {self.position.y})")