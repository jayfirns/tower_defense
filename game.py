"""
game.py

Manages the overall game state, including towers, enemies, score, base health, and logic updates.

Changes:
    • Integrated logging to track game state updates, tower placements, and enemy interactions.
    • Integrated dynamic difficulty adjustment based on slider input from the UIManager.
    • Ensured that towers, enemies, base, and projectiles (ammo) are properly drawn in the game loop.
    • Added the `increment_score()` method to track score when enemies are destroyed.
    • Added logic to restrict tower placement to within the playable area, excluding the UI ribbon.
    • Added `AmmoManager` to manage projectiles fired by towers and handle their updates and rendering.
    • Integrated the `Base` class to represent the player's base, which can be attacked by enemies and take damage.
    • Integrated UI elements (via `UIManager`), including the base health bar, score, and difficulty slider.
    • Added logic to update and render the base health bar as the base takes damage.
    • Added logic to check for game over condition and transition to game over state when base health reaches zero.
    • Integrated `self.game_over` to control the flow of the game and prevent updates after the game ends.

Author: John Firnschild
Written: 8/20/2024
Version: 0.3.212
"""

version = "0.3.212"

from enemy import EnemySpawner, Enemy
from tower import Tower
from base import Base
from ammo import AmmoManager
from ui import UIManager  # Import UIManager for UI rendering
from log_config import logger
from config import DIFFICULTY_CONFIGS, PLAYABLE_AREA_START_X, PLAYABLE_AREA_WIDTH, SCREEN_HEIGHT
import os

# Dynamically get the file name and full path using dunder __file__
file_name = os.path.basename(__file__)
full_path = os.path.abspath(__file__)

# Log the version of game.py
logger.debug("---------------------------------------------")
logger.debug("                                             ")
logger.debug(f"Running {full_path} version: {version}")
logger.debug("                                             ")
logger.debug("---------------------------------------------")


class GameState:
    """
    Manages the core game state, including towers, enemies, base health, score, and UI elements.

    Attributes:
        towers (list): A list of all placed tower objects.
        score (int): The player's current score.
        selected_tower_type (str): The currently selected tower type ("Light" or "Heavy").
        spawner (EnemySpawner): An instance of EnemySpawner to handle enemy spawning.
        ammo_manager (AmmoManager): An instance of AmmoManager to handle projectiles.
        ui_manager (UIManager): An instance of UIManager to handle all UI rendering and interactions.
        base (Base): The player's base that can be attacked by enemies and take damage.
        game_over (bool): A flag to track if the game is over.
    """

    def __init__(self, path):
        """
        Initializes the game state, setting up towers, score, enemy spawner, ammo, UI, and base.

        Args:
            path (Path): The path object that enemies will follow, providing waypoints.
        """
        self.towers = []  # Stores all placed towers
        self.score = 0  # Initialize player's score
        self.selected_tower_type = "Light"  # Default tower type
        self.spawner = EnemySpawner(spawn_interval=3, enemy_class=Enemy, path=path.get_waypoints(), game_state=self)
        self.ammo_manager = AmmoManager()  # Initialize the ammo manager for projectiles
        self.ui_manager = UIManager()  # Initialize the UI manager for UI rendering
        self.game_over = False  # Initialize the game_over flag as False

        # Instantiate the Base at the last waypoint of the enemy path, and link it to the UI manager
        self.base = Base(x=path.get_waypoints()[-1][0], y=path.get_waypoints()[-1][1], ui_manager=self.ui_manager)

        logger.info("GameState initialized.")

    def update(self, current_time, screen, difficulty_level):
        """
        Updates the game state, including tower actions, enemy spawning, ammo movement, base status, and difficulty adjustments.

        This method is responsible for updating all game entities (towers, enemies, ammo, and base)
        and for rendering the game elements on the screen. It also adjusts the difficulty based
        on player input.

        Args:
            current_time (float): The current time in seconds since the game started.
            screen (pygame.Surface): The screen surface where game entities are drawn.
            difficulty_level (str): The difficulty level selected by the player (e.g., "Easy", "Medium", "Hard").
        """
        if self.game_over:
            # If the game is over, display the game over screen and stop updating the game state
            self.ui_manager.render_game_over_screen(screen)
            return

        logger.debug(f"Updating game state. Difficulty level: {difficulty_level}")

        # Adjust difficulty based on the selected slider value
        self.adjust_difficulty(difficulty_level)
        
        # Spawn and update enemies on the screen
        self.spawner.spawn(current_time)
        self.spawner.update_enemies(screen)

        # Update and render towers, as well as their projectiles
        for tower in self.towers:
            tower.shoot(self.spawner.enemies, current_time, self.ammo_manager)  # Towers fire at enemies
            tower.draw(screen)  # Render the tower on the screen

        # Update and render the base
        self.base.draw(screen)

        # Check if the base's health has reached zero
        if self.base.health <= 0:
            self.game_over = True  # Set the game_over flag to True
            logger.info("Base health reached zero. Game over.")

        # Update and render all active ammo (projectiles)
        self.ammo_manager.update()  # Move all active projectiles towards enemies
        self.ammo_manager.draw(screen)  # Render projectiles on the screen

    def increment_score(self):
        """
        Increments the player's score when an enemy is destroyed.
        
        This method is called by enemy objects when they are destroyed,
        and it updates the score displayed in the UI.
        """
        self.score += 1
        logger.debug(f"Score incremented. New score: {self.score}")

    def place_tower(self, x, y):
        """
        Places a new tower at the specified position, if the player has enough score and
        the position is within the playable area.

        Args:
            x (int): The x-coordinate where the tower should be placed.
            y (int): The y-coordinate where the tower should be placed.
        """
        if self.game_over:
            logger.warning("Cannot place towers after the game is over.")
            return

        logger.debug(f"Attempting to place tower at ({x}, {y}) with current score: {self.score}")
        
        # Ensure that towers are only placed within the playable game area
        if not (PLAYABLE_AREA_START_X <= x <= PLAYABLE_AREA_START_X + PLAYABLE_AREA_WIDTH and 0 <= y <= SCREEN_HEIGHT):
            logger.warning(f"Invalid tower placement attempted at ({x}, {y}). Outside of the playable area.")
            return

        # Tower placement logic based on the selected tower type (Light or Heavy)
        if self.selected_tower_type == "Light":
            new_tower = Tower(x, y, name="Light")
        elif self.selected_tower_type == "Heavy" and self.score >= 10:
            new_tower = Tower(x, y, name="Heavy")
            self.score -= 10  # Deduct the cost of the Heavy tower from the score
        else:
            logger.debug("Not enough score to place Heavy tower.")
            return

        # Add the new tower to the list of active towers
        self.towers.append(new_tower)
        logger.debug(f"{new_tower.name} tower placed at ({x}, {y}). Current score: {self.score}")

    def adjust_difficulty(self, difficulty_level):
        """
        Adjusts the game's difficulty by modifying the spawn interval and enemy speed
        based on the player's selected difficulty level.

        Args:
            difficulty_level (str): The difficulty level selected by the player (e.g., "Easy", "Medium", "Hard").
        """
        logger.debug(f"Adjusting difficulty to {difficulty_level}.")
        
        # Retrieve configuration based on the selected difficulty level
        config = DIFFICULTY_CONFIGS[difficulty_level]
        
        # Adjust spawn interval and enemy speed based on the difficulty level
        self.spawner.base_spawn_interval = config['INITIAL_SPAWN_RATE']
        self.spawner.spawn_interval = config['INITIAL_SPAWN_RATE']

        # Adjust the speed of all active enemies to match the difficulty level
        for enemy in self.spawner.enemies:
            enemy.speed = config['INITIAL_ENEMY_SPEED']
            logger.debug(f"Enemy speed adjusted to {enemy.speed} based on difficulty level: {difficulty_level}")

    def reset_game(self, path):
        """
        Resets the game state to its initial values, allowing the player to start a new game.
        """
        logger.debug("Resetting game state.")

        # Reset all game-related variables
        self.towers.clear()
        self.score = 0
        self.selected_tower_type = "Light"
        self.spawner = EnemySpawner(spawn_interval=3, enemy_class=Enemy, path=path.get_waypoints(), game_state=self)
        self.ammo_manager = AmmoManager()

        # Initialize the base at the last waypoint's coordinates
        self.base = Base(x=path.get_waypoints()[-1][0], y=path.get_waypoints()[-1][1], ui_manager=self.ui_manager)
        
        self.game_over = False  # Reset the game_over flag

        logger.debug("Game state reset complete.")