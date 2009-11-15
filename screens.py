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
import os
import random
import pygame
import pyspy
from pygame.locals import *
from pyspy.constants import *

class StartScreen:
    def __init__(self, gameControlObj, screenRect):
        self.gameControl = gameControlObj
        self.menuMax = 3
        move_sound = pyspy.sound.SoundEffect(
                        os.path.join('sounds','menu_move.wav'))
        self.menu = pyspy.menu.Menu(
                ["Play Game", "Instructions", "Quit"], move_sound)
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
                self.images.append(pyspy.images.SpyImage((640,480), i))
            else:
                print "Generating level: %s" %(i)
                pyspy.levels.generateLevel(i)
        
        self.buttons = {'play': pyspy.gui.Button('play',
                callback=self.gameControl.music.unpause_track),
            'pause': pyspy.gui.Button('pause', callback=self.button_pause),
            'next': pyspy.gui.Button('next',
                callback=self.gameControl.music.next_track)}
        self.states = {'NextLevel': pyspy.spythis.states.NextLevel(self),
                       'Playing': pyspy.spythis.states.Playing(self),
                       'GameOver': pyspy.spythis.states.GameOver(self),
                       'Correct': pyspy.spythis.states.Correct(self)}

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


