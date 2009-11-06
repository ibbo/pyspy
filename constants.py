#!/usr/bin/python
#constants.py - defines constants for use in pySpy# Some constants for the different menu codes
# TODO: Brainwave - the constants (ie offsets) could be different for different screen resolutions etc.
QUIT = -1
MAIN_MENU = 0
GAME = 1
INSTRUCTIONS = 2
# The offset of the image from the screen
X_OFFSET = 20
Y_OFFSET = 50
# Text Constants
TEXT_FONT = 'Ace.ttf'
MENU_SIZE_NORMAL = 30
MENU_SIZE_BIG = 40
CLUE_COLOUR = (221, 255, 33)
MENU_COLOUR = (255, 255, 255)
MENU_SELECTED_COLOUR = MENU_COLOUR # Using a pointer to represent the selected
#item, so don't need a separate colour
MENU_PADDING = 30
# Maximum number of levels
MAX_LEVEL = 10
# Time penalties for bonuses
SHUFFLE_PENALTY = 100
ADD_LETTER_PENALTY = 100
WARNING_TIME = 100
REVEAL_PENALTY = 100
# Number of bonuses
SHUFFLE_TIMES = 2
ADD_TIMES = 3
REVEALS = 1
# Timer decrease delay
TIMER_DELAY = {'slow':(15,1), 'medium':(10,1),
        'fast':(5,1), 'very fast':(2,1), 'impossible':(1,2)}
# Music control
MUSIC = 1
SOUND = 1
# Code control
DEBUG = 0
DEBUG_DRAW_OUTLINE = 0
