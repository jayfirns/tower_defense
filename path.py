"""
path.py

Defines the Path class to represent the route that enemies will follow in the game.

Author: John Firnschild
Written: 8/18/2024
Version: 0.1.11
"""

version = "0.1.11"

from log_config import logger
import random
from config import PLAYABLE_AREA_START_X, GAME_SPACE_WIDTH, SCREEN_HEIGHT
import os

# Dynamically get the file name and full path using dunder __file__
file_name = os.path.basename(__file__)
full_path = os.path.abspath(__file__)

# Log the version of path.py
logger.debug("---------------------------------------------")
logger.debug("                                             ")
logger.debug(f"Running {full_path} version: {version}")
logger.debug("                                             ")
logger.debug("---------------------------------------------")

class Path:
    def __init__(self, num_waypoints=8):
        """
        Initializes a Path object with random waypoints. The first waypoint is fixed on the left side of the playable area,
        and the last waypoint is fixed on the right side of the playable area. The intermediate waypoints are randomized.
        
        Args:
            num_waypoints (int): The number of random waypoints to generate between the start and end.
        """
        logger.debug(f"Initializing {full_path}, version: {version}")

        # Start waypoint (fixed on the left side of the playable area)
        start_point = (PLAYABLE_AREA_START_X, random.randint(0, SCREEN_HEIGHT))

        # End waypoint (fixed on the right side within the playable game space)
        end_point = (GAME_SPACE_WIDTH, random.randint(0, SCREEN_HEIGHT))

        # Generate random waypoints in between, ensuring they stay within the playable game space
        intermediate_waypoints = [
            (random.randint(PLAYABLE_AREA_START_X, GAME_SPACE_WIDTH), random.randint(0, SCREEN_HEIGHT))
            for _ in range(num_waypoints)
        ]

        # Define the waypoints list: Start -> Intermediate -> End
        self.waypoints = [start_point] + intermediate_waypoints + [end_point]

    def get_waypoints(self):
        """
        Returns the list of waypoints that define the path.
        
        Returns:
            list: A list of tuples representing the waypoints as (x, y) coordinates.
        """
        return self.waypoints