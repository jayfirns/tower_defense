"""
ammo.py

Defines the Ammo class and AmmoManager class, which are responsible for representing and managing tower attacks in real-time.

Changes:
    • Replaced the green square with `blast.png` for the ammo's visual representation.
    • Added enhanced debugging visuals to confirm projectile visibility.
    • Verified boundary and movement logic for proper rendering of projectiles.

Author: John Firnschild
Written: 8/20/2024
Version: 0.1.22
"""

version = "0.1.22"

import pygame
from log_config import logger
import os

# Dynamically get the file name and full path using dunder __file__
file_name = os.path.basename(__file__)
full_path = os.path.abspath(__file__)

# Log the version of ammo.py
logger.debug("---------------------------------------------")
logger.debug("                                             ")
logger.debug(f"Running {full_path} version: {version}")
logger.debug("                                             ")
logger.debug("---------------------------------------------")

class Ammo:
    def __init__(self, start_pos, target_enemy, speed, damage):
        """
        Initializes an ammo object that will move towards a target enemy.

        Args:
            start_pos (tuple): The starting position of the ammo (x, y).
            target_enemy (Enemy): The enemy this ammo is targeting.
            speed (float): The speed at which the ammo moves.
            damage (int): The damage this ammo will deal to the enemy.
        """
        self.position = pygame.Vector2(start_pos)  # Set initial position
        self.target_enemy = target_enemy  # Reference to the enemy being targeted
        self.speed = speed  # Speed of the projectile
        self.damage = damage  # Damage this ammo will deal
        self.active = True  # Track if the ammo is still active (not hit or off-screen)

        # Load the blast.png image for the ammo sprite
        self.sprite = pygame.image.load("/Users/johnfirnschild/Documents/HomeLab/Python/projects/games/tower_defense/assets/images/projectiles/blast.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (30, 30))  # Scale the sprite if necessary
        self.rect = self.sprite.get_rect(center=(int(self.position.x), int(self.position.y)))  # Create a rect for positioning the sprite

    def move(self):
        """
        Moves the ammo towards the target enemy. If the ammo reaches the target,
        it will hit the enemy and deactivate.
        """
        # If ammo is inactive or the enemy is already dead, do nothing
        if not self.active or self.target_enemy.health <= 0:
            self.active = False
            return

        # Calculate the direction towards the target enemy
        direction = self.target_enemy.current_position - self.position

        # Check if the ammo can reach the target in this move
        if direction.length() <= self.speed:
            self.position = self.target_enemy.current_position  # Snap to the enemy's position
            self.hit_target()  # Handle the hit logic
        else:
            direction.normalize_ip()  # Normalize the direction vector
            self.position += direction * self.speed  # Move the ammo
            self.rect.center = (int(self.position.x), int(self.position.y))  # Update the rect's position
            logger.debug(f"Ammo moving to {self.position}")  # Log movement for confirmation

    def hit_target(self):
        """
        Handles the logic when the ammo hits the target enemy. It deals damage to the enemy
        and deactivates the ammo.
        """
        if self.active:
            self.target_enemy.take_damage(self.damage)  # Deal damage to the enemy
            logger.debug(f"Ammo hit enemy at {self.target_enemy.current_position}, dealing {self.damage} damage.")
            self.active = False  # Mark the ammo as inactive

    def draw(self, screen):
        """
        Draws the ammo sprite on the screen. It will only draw if the ammo is active.
        """
        if self.active:
            screen.blit(self.sprite, self.rect)  # Draw the sprite at its current position
            logger.debug(f"Drawing ammo at position {self.position}")  # Log the draw position


class AmmoManager:
    def __init__(self):
        """
        Initializes the ammo manager, which tracks all active ammo in the game.
        """
        self.ammo_list = []  # List of active ammo objects

    def shoot(self, start_pos, target_enemy, speed, damage):
        """
        Spawns a new ammo object aimed at a target enemy and adds it to the ammo list.

        Args:
            start_pos (tuple): The starting position of the ammo.
            target_enemy (Enemy): The enemy the ammo is targeting.
            speed (float): The speed of the ammo.
            damage (int): The damage the ammo will deal when it hits the target.
        """
        # Create a new Ammo object and add it to the list
        ammo = Ammo(start_pos, target_enemy, speed, damage)
        self.ammo_list.append(ammo)
        logger.debug(f"Ammo created from {start_pos} towards enemy at {target_enemy.current_position}.")

    def update(self):
        """
        Updates all active ammo, moving them towards their targets and checking for hits.
        Inactive ammo (either after hitting the target or going off-screen) will be removed.
        """
        for ammo in self.ammo_list:
            ammo.move()  # Move the ammo towards its target

        # Remove inactive ammo after updating
        self.ammo_list = [ammo for ammo in self.ammo_list if ammo.active]

    def draw(self, screen):
        """
        Draws all active ammo on the screen.
        """
        for ammo in self.ammo_list:
            ammo.draw(screen)