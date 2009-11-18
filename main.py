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


import sys, os, random, math, getopt
import re
sys.path.append(os.path.split(os.getcwd())[0])
import pygame
from pygame.locals import *
import pyspy
from pyspy.constants import *

if DEBUG:
    import pdb

class GameControl:
    def __init__(self):
        self.gameEvent = pyspy.events.GameEvent()
        self.modeCur = 0
        self.modes = []
        self.players = []
        self.playerCur = 0
        self.music = pyspy.sound.MusicControl()
        return
		
    def addMode(self, newMode):
        """Insert the new mode into the modes list"""
        self.modes.append(newMode)
        
    def setMode(self, newMode, type = 0):
        """Set the new mode, and reset it"""
        self.modeCur = newMode
        
        # If we didn't set the mode to exit
        if self.modeCur != -1:
            self.modes[self.modeCur].reset(type)		

    def update(self):
        """Update the current mode and events"""
        self.gameEvent.update()
        self.music.update()
        
        if self.modeCur != -1:
            self.modes[self.modeCur].eventHandle()
                
        if self.modeCur != -1:
            self.modes[self.modeCur].update()

    def draw(self, background, screen):
        if self.modeCur != -1:
            self.modes[self.modeCur].draw(background, screen)

def usage():
    usage_string = """
    main.py - Play pySpy!
    Options: -q, --quiet: play pySpy quietly
             -d, --debug: Run in debug mode
             -h, --help: show this usage message
    """
    print usage_string

def main(argv):
    FULL = False
    # Command-line argument handling
    try:
        opts, args = getopt.getopt(argv, "hdqfu",
                ["help","debug","quiet","fullscreen","update"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-q", "--quiet"):
            print "Running in quiet mode"
            global MUSIC, SOUND
            MUSIC = 0
            SOUND = 0
        elif opt in ("-d", "--debug"):
            print "Debug mode"
            global DEBUG
            DEBUG = 1
        elif opt in ("-f", "--fullscreen"):
            print "Running in fullscreen mode"
            FULL = True
        elif opt in ("-u", "--update"):
            print "Checking for updates..."
            updates = pyspy.update.update()
            if not updates:
                print "No updates available"
            sys.exit()

    # Check that compatible versions of pygame and python are being used
    pygame_ver = pygame.version.vernum
    if pygame_ver[0] < 1 or (pygame_ver[0] < 2 and pygame_ver[1] < 9):
        print "Requires pygame 1.9.0 or greater"
        return 0
    python_ver = sys.version_info
    if python_ver[0] < 2 or (python_ver[0] > 1 and python_ver[1] < 6):
        print "Requires python 2.6 or greater"
        return 0
    if python_ver[0] > 2:
        print "This is not yet compatible with python 3.0 or greater"
        return 0

    # Initialise the screen
    pygame.init()
    modes = pygame.display.list_modes()
    #mode = modes[1]
    mode = (1024, 768)
    if FULL:
        screen = pygame.display.set_mode(mode, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(mode)
    pygame.display.set_caption('pySpy')

    background = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    background.fill((255,255,255))
    try:
        bkg_name = 'background_'+str(mode[0])+'x'+str(mode[1])
        bkg_image, bkg_rect = pyspy.utilities.load_png(bkg_name)
    except:
        print "Rescaling default background image"
        bkg_image, bkg_rect = pyspy.utilities.load_png('background')
        bkg_image = pygame.transform.scale(bkg_image, mode)
    background.blit(bkg_image, (0,0))
    logo, logo_rect = pyspy.utilities.load_png('logo')
    logo_rect.right = bkg_rect.right - 20
    logo_rect.top = bkg_rect.top + 20
    background.blit(logo, logo_rect)
    background = background.convert_alpha()

    bigFont = pygame.font.Font(os.path.join('fonts', TEXT_FONT), 
                                    MENU_SIZE_BIG)
    loadingText = bigFont.render('Loading...', 1, (255,255,255))
    loadingRect = loadingText.get_rect()
    loadingRect.center = screen.get_rect().center

    # Show the background while we're loading, with a loading symbol
    screen.blit(background, (0,0))
    screen.blit(loadingText, loadingRect)
    
    pygame.display.flip()

    clock = pygame.time.Clock()
    random.seed()

    gameControl = GameControl()
    gameControl.addMode(
            pyspy.screens.StartScreen(gameControl, screen.get_rect()))
    gameControl.addMode(
            pyspy.screens.GameScreen(gameControl, screen.get_rect()))
    gameControl.addMode(
            pyspy.screens.InstructionsScreen(gameControl, screen.get_rect()))
    gameControl.addMode(
            pyspy.screens.UpdateScreen(gameControl, screen.get_rect()))

    while 1:
        # Lock the framerate
        clock.tick(60)

        # Handle the modes
        gameControl.update()
        gameControl.draw(background, screen)

        # Handle game exit
        if gameControl.modeCur == -1:
            return

        #Flip to front
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__": main(sys.argv[1:])
