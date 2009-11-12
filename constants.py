#!/usr/bin/python
#    This file is part of pySpy.
#
#    pySpy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    pySpy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pySpy.  If not, see <http://www.gnu.org/licenses/>.
import pygame
#constants.py - defines constants for use in pySpy
# Some constants for the different menu codes
QUIT = -1
MAIN_MENU = 0
GAME = 1
INSTRUCTIONS = 2
# The offset of the image from the screen
X_OFFSET = 20
Y_OFFSET = 50
# Text Constants
TEXT_FONT = 'Ace.ttf'
MONO_FONT = 'FreeMono.ttf'
MENU_SIZE_NORMAL = 30
MENU_SIZE_BIG = 40
BONUS_SIZE = 20
BONUS_COUNT_COLOUR = pygame.Color("yellow")
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
        'fast':(5,1), 'very fast':(2,2), 'impossible':(1,2)}
# Music control
MUSIC = 1
SOUND = 1
# Code control
DEBUG = False
DEBUG_DRAW_OUTLINE = 0
# Server address
SERVER_URL = 'http://pyspy.game-host.org/levels/'
