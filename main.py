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
#TODO: Clean up these import statements
from pyspy.utilities import *
import pyspy.clue as clue
from pyspy.constants import *
from pyspy.menu import *
import pyspy.images as ims

if DEBUG:
    import pdb

class SpyImage(pygame.Surface):
    def __init__(self,size,name):
        pygame.Surface.__init__(self,size)
        self.image, self.rect = load_png(name, rootpath='levels')
        self.blit(self.image, (0,0))
        self.info = ims.ImageInfo(name + '.png')
        self.mask = []
        self.levels = self.load_levels()
        self.font = pygame.font.Font(os.path.join('fonts','FreeMono.ttf'), 36)
        self.clue = clue.ClueImage()
       
    def load_levels(self):
        levels = []
        for i in self.info.masks:
            levels.append(i.level)
        return levels

    def set_mask(self, level=1):
        # Take a random mask
        masks = [i for i in self.info.masks if i.level == level]
        if len(masks) > 0:
            self.mask = masks[random.randint(0,len(masks)-1)]
        else:
            self.mask = []
            print "No levels found"
            return self.mask
        self.clue.reset(self.mask.clue)
        # Replace this with a method of the clue class
        
class StartScreen:
    def __init__(self, gameControlObj, screenRect):
        self.gameControl = gameControlObj
        self.menuMax = 3
        move_sound = pyspy.sound.SoundEffect(
                        os.path.join('sounds','menu_move.wav'))
        self.menu = Menu(["Play Game", "Instructions", "Quit"], move_sound)
        self.firstDraw = 1

    def reset(self, type):
        self.menu.reset()
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        self.firstDraw = 1
        return

    def eventHandle(self):
        if self.gameControl.gameEvent.mouseMoved:
            mousepos = self.gameControl.gameEvent.mousePos
            self.menu.collide(mousepos)
        # Check for quit
        if self.gameControl.gameEvent.newkeys[K_ESCAPE]:
            self.gameControl.setMode(QUIT)

        # Move selection up and down
        if self.gameControl.gameEvent.newkeys[K_DOWN]:
            self.menu.selectNext("down")
            
        if self.gameControl.gameEvent.newkeys[K_UP]:
            self.menu.selectNext("up")

        # Process current selection
        if self.gameControl.gameEvent.newkeys[K_RETURN] or \
            self.gameControl.gameEvent.newkeys[K_KP_ENTER] or \
                self.gameControl.gameEvent.mouseButtons[0]:
            if self.menu.selectedItem.text == "Play Game":
                self.gameControl.setMode(GAME)
            if self.menu.selectedItem.text == "Instructions":
                self.gameControl.setMode(INSTRUCTIONS)
            if self.menu.selectedItem.text == "Quit":
                self.gameControl.setMode(QUIT)

    def update(self):
        return

    def draw(self, background, screen):
        if self.firstDraw:
            screen.blit(background, (0, 0))
            self.firstDraw = 0
        # The size of the menu items changes when they are selected so we
        # have to set the positions before we draw them.
        self.menu.setPositions(background.get_rect())
        #Draw Everything
        self.menu.draw(background, screen)
        
  
class InstructionsScreen:
    def __init__(self, gameControlObj, screenRect):
        self.gameControl = gameControlObj
        self.text_font = pygame.font.Font(os.path.join('fonts',MONO_FONT), 22)
        self.filename = 'Instructions.txt'
        self.lines = self.get_instructions()
        self.back_button = pyspy.gui.Button('back', can_disable=False)
        self.back_button.set_callback(self.quit)
        self.back_button.rect.topright = screenRect.topright
        self.back_button.rect.top += 210
        self.back_button.rect.right -= 45
        self.drawn = 0

    def get_instructions(self):
        f = file(self.filename, 'r')
        raw_lines = f.readlines()
        f.close()
        lines = [i.strip() for i in raw_lines]
        rendered_lines = []
        for i in lines:
            rendered_lines.append(self.text_font.render(i,1,(0,0,0)))
        return rendered_lines

    def update(self):
        pass

    def reset(self, type=0):
        self.drawn = 0
        pass

    def quit(self):
        self.gameControl.setMode(MAIN_MENU)
        return True

    def eventHandle(self):
        if self.gameControl.gameEvent.newkeys[K_ESCAPE]:
            self.gameControl.setMode(MAIN_MENU)
        mousepos = self.gameControl.gameEvent.mousePos
        if self.gameControl.gameEvent.mouseButtons[0]:
            if self.back_button.rect.collidepoint(mousepos):
                self.back_button()

    def draw(self, background, screen):
        if not self.drawn:
            screen.blit(background, (0,0))
            count = 0
            for i in self.lines:
                screen.blit(i, (50, 50 + count*22))
                count += 1
            self.back_button.draw(background, screen)
        self.drawn = 1


class GameScreen:
    def __init__(self, gameControlObj, screenRect):
        self.gameControl = gameControlObj
        self.level = 0
        self.indicator = pyspy.gui.LevelIndicator((screenRect.width, screenRect.height))
        self.images = []
        levels = pyspy.levels.getLevels()
        if not levels:
            #FIXME: Need to create custom Exception classes
            raise Exception, "No levels found"
        for i in levels:
            if pyspy.levels.checkLevel(i):
                self.images.append(SpyImage((640,480), i))
            else:
                print "Generating level: %s" %(i)
                pyspy.levels.generateLevel(i)
        
        self.buttons = {'unshuffle': pyspy.gui.Button('unshuffle'), 
            'more_letters': pyspy.gui.Button('more_letters'),
            'reveal': pyspy.gui.Button('reveal'),
            'play': pyspy.gui.Button('play',
                callback=self.gameControl.music.unpause_track),
            'pause': pyspy.gui.Button('pause', callback=self.button_pause),
            'next': pyspy.gui.Button('next',
                callback=self.gameControl.music.next_track)}
        self.states = {'NextLevel': pyspy.original.states.NextLevel(self),
                       'Playing': pyspy.original.states.Playing(self),
                       'GameOver': pyspy.original.states.GameOver(self),
                       'Correct': pyspy.original.states.Correct(self)}

    def button_pause(self):
        if self.gameControl.music.paused:
            self.gameControl.music.unpause_track()
        else:
            self.gameControl.music.pause_track()
        return True

    def set_image(self, imageObj):
        self.image = imageObj
        self.image.set_mask(self.level)
    
    def update(self):
        self.state.update()

    def set_level(self, level):
        valid_images = []
        for i in self.images:
            if level in i.levels:
                valid_images.append(i)

        if valid_images:
            self.set_image(valid_images[random.randint(0,len(valid_images)-1)])
        else:
            return False
        return True

    def eventHandle(self):
        self.state.eventHandle()
        return

    def reset(self, type = 0):
        self.level = 0
        for button in self.buttons.values():
            button.reset()
        self.state = self.states['NextLevel']
        self.state.enter()

    def draw(self, background, screen):
        self.state.draw(background, screen)



# Deals with events in the Game

class GameEvent:
    """Event system wrapped so that it is based on time things were pressed.  
            Otherwise repeats occur that we dont desire."""
            
    def __init__(self):
            # Run update to init all the variables
            self.keystate = pygame.key.get_pressed()
            self.keystate = [k for k in self.keystate]
            self.mousestate = pygame.mouse.get_pressed()
            self.mousestate = [b for b in self.mousestate]
            self.mouseMoved = 0
            self.mousePos = (0,0)
            self.update()

    def update(self):
            # See if the user wants to quit
            if pygame.event.peek(12):
                pygame.quit()
                exit(0)
            pygame.event.pump() #keep messages alive

            events = pygame.event.get()
            self.keystate = [False for k in self.keystate]
            self.mousestate = [False for b in self.mousestate]
            for e in events:
                if e.type == KEYUP:
                    #pdb.set_trace()
                    self.keystate[e.key] = True
                if e.type == MOUSEBUTTONUP:
                    if e.button in range(0,3):
                    # Sometimes there are mouse buttons that are outside
                    # this range which mouse.get_pressed() doesn't know about
                    # We only care about left-clicking really...
                        self.mousestate[e.button-1] = True
            
            self.newkeys = self.keystate
            self.mouseButtons = self.mousestate

            pygame.event.clear()

            # Get the mouse data
            self.oldMousePos = self.mousePos
            self.mousePos = pygame.mouse.get_pos()
            if self.oldMousePos == self.mousePos:
                self.mouseMoved = 0
            else:
                self.mouseMoved = 1
            
            
            # Get the time
            self.ticks = pygame.time.get_ticks()

       

class GameControl:
    def __init__(self):
        self.gameEvent = GameEvent()
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

    ver = pygame.version.vernum
    if ver[0] < 1 or (ver[0] < 2 and ver[1] < 9):
        print "Requires pygame 1.9.0 or greater"
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
        bkg_image, bkg_rect = load_png(bkg_name)
    except:
        print "Rescaling default background image"
        bkg_image, bkg_rect = load_png('background')
        bkg_image = pygame.transform.scale(bkg_image, mode)
    background.blit(bkg_image, (0,0))
    logo, logo_rect = load_png('logo')
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
    gameControl.addMode(StartScreen(gameControl, screen.get_rect()))
    gameControl.addMode(GameScreen(gameControl, screen.get_rect()))
    gameControl.addMode(InstructionsScreen(gameControl, screen.get_rect()))

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
