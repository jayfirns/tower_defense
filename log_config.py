"""
log_config.py

Configure logging format, levels, and handlers. 
This file sets up both a console logger and a log file logger with rotating log files, 
to track key events throughout the game. 

Changes:

    • Enhanced Logging: Ensure we log critical events such as tower placement, score updates, 
      enemy destruction, and errors related to game events.
    • Introduced file-size-based log rotation to prevent logs from growing indefinitely.

High-Level Actions:

    • Added more detailed logging for significant game events, which will help with debugging and tracking player actions 
      (e.g., when towers are placed or when enemies are killed).
    • Implemented log rotation to manage log size and preserve disk space.

Author: John Firnschild
Written: 8/17/2024
Version: 0.1.12
"""

version = "0.1.12"

import logging
import os
from logging.handlers import RotatingFileHandler

# Dynamically get the file name and full path using dunder __file__
file_name = os.path.basename(__file__)
full_path = os.path.abspath(__file__)

# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the global logger level to DEBUG

# Log the version of log_config.py
logger.debug("---------------------------------------------")
logger.debug("                                             ")
logger.debug(f"Running {full_path} version: {version}")
logger.debug("                                             ")
logger.debug("---------------------------------------------")

# Create a RotatingFileHandler for logging to a file with rotation
# - The log file will rotate when it exceeds 5 MB
# - A maximum of 3 backup logs will be kept
file_handler = RotatingFileHandler('tower_defense.log', maxBytes=5*1024*1024, backupCount=3)
file_handler.setLevel(logging.DEBUG)  # Log file will record all DEBUG and above messages

# Create a console handler for logging to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Console will display all INFO and above messages

# Define a formatter and set it for both handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Ensure existing logs aren't duplicated by disabling propagation
logger.propagate = False