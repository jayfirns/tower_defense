"""
config.py

Defines constants used throughout the game.
This file centralizes game settings such as screen size, frame rate, ribbon UI, and other configurations.

Changes:

    • Increased ribbon width to better accommodate longer messages.
    • Adjusted padding and font sizes for better display in the ribbon.
    • Updated screen width to account for the wider ribbon.
    • Prepared for dynamic difficulty adjustment with sliders.
    • Added background color setting.
    • Added slider configuration for difficulty adjustment.
    • Introduced PLAYABLE_AREA constants to separate the playable game space from the ribbon.
    • Ensured that all gameplay elements (enemies, towers, etc.) are placed in the defined playable area.

Author: John Firnschild
Written: 8/17/2024
Version: 0.1.512
"""

version = "0.1.512"

from log_config import logger
import pygame
pygame.init()
import os

# Dynamically get the file name and full path using dunder __file__
file_name = os.path.basename(__file__)
full_path = os.path.abspath(__file__)

# Log the version of config.py
logger.debug("---------------------------------------------")
logger.debug("                                             ")
logger.debug(f"Running {full_path} version: {version}")
logger.debug("                                             ")
logger.debug("---------------------------------------------")

# Screen dimensions
GAME_SPACE_WIDTH = 800  # Width of the actual game space
RIBBON_WIDTH = 300  # Width of the ribbon on the left-hand side of the screen
SCREEN_WIDTH = GAME_SPACE_WIDTH + RIBBON_WIDTH  # Total screen width (game space + ribbon)
SCREEN_HEIGHT = 600  # Height of the game window in pixels

# Define the playable area, which excludes the ribbon
PLAYABLE_AREA_START_X = RIBBON_WIDTH  # The game space starts after the ribbon
PLAYABLE_AREA_WIDTH = GAME_SPACE_WIDTH  # The width of the playable area is the same as the game space width

# Frame rate
FPS = 20  # Frames per second for the game loop

# Ribbon UI constants
RIBBON_PADDING = 15  # Increased padding for better spacing in the ribbon
RIBBON_BORDER_THICKNESS = 3  # Thickness of the border around the ribbon

# Font sizes
RIBBON_FONT_SIZE = 36  # Font size for the main text in the ribbon
RIBBON_SMALL_FONT_SIZE = 18  # Font size for the smaller messages in the ribbon

# Background color
BACKGROUND_COLOR = (50, 50, 50)  # Background color of the game space

# Difficulty constants for the slider-based selection
DIFFICULTY_CONFIGS = {
    'Easy': {
        'INITIAL_SPAWN_RATE': 3,
        'INITIAL_ENEMY_SPEED': 3,
        'SCORE_THRESHOLD': 15,
        'SPAWN_RATE_DECREASE_PERCENTAGE': 0.3,
        'ENEMY_SPEED_INCREASE_PERCENTAGE': 0.3,
    },
    'Medium': {
        'INITIAL_SPAWN_RATE': 2,
        'INITIAL_ENEMY_SPEED': 5,
        'SCORE_THRESHOLD': 10,
        'SPAWN_RATE_DECREASE_PERCENTAGE': 0.4,
        'ENEMY_SPEED_INCREASE_PERCENTAGE': 0.4,
    },
    'Hard': {
        'INITIAL_SPAWN_RATE': 1,
        'INITIAL_ENEMY_SPEED': 8,
        'SCORE_THRESHOLD': 5,
        'SPAWN_RATE_DECREASE_PERCENTAGE': 0.5,
        'ENEMY_SPEED_INCREASE_PERCENTAGE': 0.5,
    },
    'Spicy': {
        'INITIAL_SPAWN_RATE': 0.8,
        'INITIAL_ENEMY_SPEED': 10,
        'SCORE_THRESHOLD': 3,
        'SPAWN_RATE_DECREASE_PERCENTAGE': 0.6,
        'ENEMY_SPEED_INCREASE_PERCENTAGE': 0.6,
    },
    'Hell': {
        'INITIAL_SPAWN_RATE': 0.5,
        'INITIAL_ENEMY_SPEED': 12,
        'SCORE_THRESHOLD': 1,
        'SPAWN_RATE_DECREASE_PERCENTAGE': 0.7,
        'ENEMY_SPEED_INCREASE_PERCENTAGE': 0.7,
    },
}

# Slider configuration for adjusting difficulty
SLIDER_CONFIG = {
    'slider_width': 300,  # Adjust slider width to accommodate more stages
    'slider_height': 30,  
    'position_y': SCREEN_HEIGHT - 90,  
    'value_range': (1, 5),  # 1 for Easy, 5 for Hell
    'start_value': 2,  # Default to Medium difficulty
}

# Slider label positions for "Easy", "Hard", "Spicy", and "Hell"
SLIDER_LABELS = {
    'easy_label_position': (RIBBON_WIDTH - 380, SCREEN_HEIGHT - 50),
    'medium_label_position': (RIBBON_WIDTH - 280, SCREEN_HEIGHT - 50),
    'hard_label_position': (RIBBON_WIDTH - 180, SCREEN_HEIGHT - 50),
    'spicy_label_position': (RIBBON_WIDTH - 100, SCREEN_HEIGHT - 50),
    'hell_label_position': (RIBBON_WIDTH - 40, SCREEN_HEIGHT - 50),
}

### Removed AI Halucinations