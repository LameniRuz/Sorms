import pygame as pg
from helper_functions import get_keycode_mapping

# Global variables #
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen_size = SCREEN_WIDTH, SCREEN_HEIGHT 

# Block, segment size
BLOCK_SIZE = 20 # width and height need to be divided by BLOCK_SIZE, giving a whole number

#Colors
PINK = (247, 144, 178)  ##f790b2
GREEN = (144, 247, 213) ##90f7d5
GREEN2 = (230, 247, 144)##e6f790
GREEN3 = pg.Color('#7c98b4')
GOLD = pg.Color('#E6CF4E')
GRAY = (64, 64, 64)
#Font sizes
SCORE_FTS = 40
ALERT_FTS = 60


# Directional mappings
DWDIR = {"x": 0, "y": 1} # down direction, zero x and positive y  increase means down
UPDIR = {"x": 0, "y": -1} # up direction, zero x and negative y  increase means up 
LFDIR = {"x": -1, "y": 0} # up direction, negative x and y  increase means up 
RTDIR = {"x": 1, "y": 0} # up direction, negative x and y  increase means up 
# "UP", "DOWN", "LEFT", "RIGHT" - are snake directions, 
#spawn in  the opposite direction of movement
SPAWN_IN_DIR = {"UP": DWDIR, "DOWN": UPDIR, "LEFT": RTDIR, "RIGHT":LFDIR}

#  move according to the current direction
MOVE_IN_DIR = {"UP": UPDIR, "DOWN": DWDIR, "LEFT": LFDIR, "RIGHT": RTDIR}

# Used to prevent direction change to the opposite of the current one
PREV_DIR_CHANGE = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}

# Control mappings for Players
direction_control_player_1_names = {"UP": "w", "DOWN": "s", "LEFT": "a" , "RIGHT": "d"}
direction_control_player_1 = get_keycode_mapping(direction_control_player_1_names)
direction_control_player_2_names = {"UP": "up", "DOWN": "down", "LEFT": "left" , "RIGHT": "right"}
direction_control_player_2 = get_keycode_mapping(direction_control_player_2_names)

direction_control_player_3_names = {"UP": "o", "DOWN": "l", "LEFT": "k" , "RIGHT": ";"}
direction_control_player_3 = get_keycode_mapping(direction_control_player_3_names)

