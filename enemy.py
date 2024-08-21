"""
enemy.py

Defines the Enemy class, which represents enemies in the game, and the EnemySpawner class, 
which is responsible for spawning enemies at set intervals.

Changes:
    • Enemy Sprites: Replaced the rectangle representation of enemies with sprites.
    • Death Detection: Ensured that when an enemy’s health reaches zero, it is properly removed from the game and the score is updated in main.py.
    • Dynamic Difficulty: Adjusted the spawn interval dynamically based on the player's score, making the game harder as the player progresses.
    • Adjusted enemy speed based on dynamic difficulty.
    • Added logic to handle enemies reaching the base and dealing damage to it.
    • Integrated base damage handling when enemies reach the base.
    • Integrated sprites from the assets directory, randomly assigning them to each enemy.
    • Updated draw method to render sprites instead of rectangles.

Author: John Firnschild
Written: 8/20/2024
Version: 0.3.12
"""

version = "0.3.12"

import pygame
import os
import random
from log_config import logger
from config import PLAYABLE_AREA_START_X, PLAYABLE_AREA_WIDTH, SCREEN_HEIGHT

# Dynamically get the file name and full path using dunder __file__
file_name = os.path.basename(__file__)
full_path = os.path.abspath(__file__)

# Log the version of enemy.py
logger.debug("---------------------------------------------")
logger.debug("                                             ")
logger.debug(f"Running {full_path} version: {version}")
logger.debug("                                             ")
logger.debug("---------------------------------------------")


class Enemy:
    def __init__(self, health, speed, path, game_state):
        """
        Initializes an enemy object with health, speed, path, and a randomly assigned sprite.

        Args:
            health (int): The health of the enemy.
            speed (int): The speed at which the enemy moves along the path.
            path (list): The path that the enemy will follow.
            game_state (GameState): The game state to notify when the enemy is destroyed or reaches the base.
        """
        self.health = health
        self.speed = speed
        self.path = path
        self.current_position = pygame.Vector2(path[0])  # Start at the first waypoint
        self.target_index = 1  # Start heading towards the second waypoint
        self.target_position = pygame.Vector2(self.path[self.target_index])  # The next target
        self.game_state = game_state  # Reference to the game state

        # Load enemy sprites
        sprite_paths = [
            os.path.join('assets', 'images', 'characters', 'red_top.png'),
            os.path.join('assets', 'images', 'characters', 'soul_sista_1.png')
        ]

        # Randomly select a sprite for this enemy
        selected_sprite_path = random.choice(sprite_paths)
        self.sprite = pygame.image.load(selected_sprite_path).convert_alpha()

        # Scale the sprite to fit game requirements
        self.sprite = pygame.transform.scale(self.sprite, (40, 40))
        self.rect = self.sprite.get_rect()

        # Ensure enemy starts within the playable area
        if not (PLAYABLE_AREA_START_X <= self.current_position.x <= PLAYABLE_AREA_START_X + PLAYABLE_AREA_WIDTH):
            logger.warning(f"Enemy spawned outside playable area at position: {self.current_position}")
        else:
            logger.debug(f"Enemy created at position: {self.current_position} with health: {self.health}, speed: {self.speed}")

    def move(self):
        """
        Moves the enemy along the path by updating its position.
        """
        if self.target_index < len(self.path):
            direction = self.target_position - self.current_position
            distance_to_move = self.speed

            if direction.length() <= distance_to_move:
                # Enemy reached the target position
                self.current_position = self.target_position
                logger.debug(f"Enemy reached waypoint {self.target_index} at position: {self.current_position}")

                # Increment target index to move to the next waypoint
                self.target_index += 1

                if self.target_index < len(self.path):
                    self.target_position = pygame.Vector2(self.path[self.target_index])
                    logger.debug(f"Enemy now moving towards waypoint {self.target_index} at position: {self.target_position}")
            else:
                # Normalize direction and move enemy towards the target
                direction.normalize_ip()
                self.current_position += direction * distance_to_move
                logger.debug(f"Enemy moving towards waypoint at position: {self.target_position}, current position: {self.current_position}")
        else:
            logger.info(f"Enemy has reached the end of the path at position: {self.current_position} and damaged the base.")
            self.reach_end_of_path()

    def reach_end_of_path(self):
        """
        Logic to handle when an enemy reaches the end of the path.
        This includes damaging the base and removing the enemy from the game.
        """
        logger.debug(f"Enemy reached the final waypoint and is being removed.")
        self.health = 0  # Mark the enemy as "destroyed" so it can be removed from the game
        self.game_state.base.take_damage(10)  # Deal damage to the base

    def draw(self, screen):
        """
        Draws the enemy sprite on the screen.

        Args:
            screen (pygame.Surface): The game screen surface where the enemies will be drawn.
        """
        # Ensure that the enemy is drawn within the playable area
        if PLAYABLE_AREA_START_X <= self.current_position.x <= PLAYABLE_AREA_START_X + PLAYABLE_AREA_WIDTH:
            self.rect.center = self.current_position  # Update the rect position to the center
            screen.blit(self.sprite, self.rect)  # Draw the sprite
            logger.debug(f"Drawing enemy sprite at position: {self.current_position}")
        else:
            logger.warning(f"Attempting to draw enemy outside of playable area at position: {self.current_position}")

    def take_damage(self, damage):
        """
        Reduces the enemy's health by the given damage amount.

        Args:
            damage (int): The amount of damage to apply to the enemy.
        """
        self.health -= damage
        logger.debug("Enemy took %d damage, remaining health: %d", damage, self.health)
        if self.health <= 0:
            self.destroy()

    def destroy(self):
        """
        Destroys the enemy when health reaches zero and increments the player's score.
        """
        logger.debug("Enemy destroyed.")
        self.game_state.increment_score()  # Increment the score when the enemy is destroyed


class EnemySpawner:
    def __init__(self, spawn_interval, enemy_class, path, game_state):
        """
        Initializes the EnemySpawner responsible for spawning enemies at set intervals.

        Args:
            spawn_interval (float): The time interval in seconds between enemy spawns.
            enemy_class (class): The class of the enemy to spawn.
            path (list): The path that the enemies will follow.
            game_state (GameState): The game state to notify when enemies are spawned.
        """
        self.spawn_interval = spawn_interval
        self.enemy_class = enemy_class
        self.path = path
        self.game_state = game_state
        self.last_spawn_time = 0
        self.enemies = []

        logger.debug("EnemySpawner created with interval: %.2f seconds", spawn_interval)

    def spawn(self, current_time):
        """
        Spawns a new enemy if the time interval since the last spawn exceeds the spawn_interval.

        Args:
            current_time (float): The current time in seconds.
        """
        if current_time - self.last_spawn_time >= self.spawn_interval:
            # Ensure enemies spawn within the playable area
            start_position = self.path[0]
            if PLAYABLE_AREA_START_X <= start_position[0] <= PLAYABLE_AREA_START_X + PLAYABLE_AREA_WIDTH:
                new_enemy = self.enemy_class(health=100, speed=2, path=self.path, game_state=self.game_state)
                self.enemies.append(new_enemy)
                self.last_spawn_time = current_time
                logger.debug("New enemy spawned.")
            else:
                logger.warning(f"Enemy spawn position {start_position} is outside the playable area.")

    def update_enemies(self, screen):
        """
        Updates and draws all the enemies spawned by this spawner.

        Args:
            screen (pygame.Surface): The game screen surface where the enemies will be drawn.
        """
        # Remove destroyed enemies
        self.enemies = [enemy for enemy in self.enemies if enemy.health > 0]

        # Update and draw remaining enemies
        for enemy in self.enemies:
            enemy.move()
            enemy.draw(screen)