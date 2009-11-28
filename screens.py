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
                ["Play Game", "Instructions", "Update levels", "Quit"], move_sound)
        self.firstDraw = 1

    def reset(self, type):
        self.menu.reset()
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        self.firstDraw = 1
        return

    def eventHandle(self):
        mousepos = self.gameControl.gameEvent.mousePos
        
        # Check for quit
        if self.gameControl.gameEvent.newkeys[K_ESCAPE]:
            self.gameControl.setMode(QUIT)

        # Move selection up and down
        if self.gameControl.gameEvent.newkeys[K_DOWN]:
            self.menu.selectNext("down")
            
        if self.gameControl.gameEvent.newkeys[K_UP]:
            self.menu.selectNext("up")

        # Process current selection
        # FIXME: Checking the menu item strings is a bad idea.
        collided = self.menu.collide(mousepos)
        if self.gameControl.gameEvent.newkeys[K_RETURN] or \
            self.gameControl.gameEvent.newkeys[K_KP_ENTER] or \
                (self.gameControl.gameEvent.mouseButtons[0] and \
                    collided):
            if self.menu.selectedItem.text == "Play Game":
                self.gameControl.setMode(GAME)
            if self.menu.selectedItem.text == "Instructions":
                self.gameControl.setMode(INSTRUCTIONS)
            if self.menu.selectedItem.text == "Update levels":
                self.gameControl.setMode(UPDATE)
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

class UpdateScreen:
    def __init__(self, gameControlObj, screenRect):
        self.gameControl = gameControlObj
        self.text_font = pygame.font.Font(os.path.join('fonts', MONO_FONT), 16)
        self.back_button = pyspy.gui.Button('back', can_disable=False)
        self.back_button.set_callback(self.quit)
        self.back_button.rect.topright = screenRect.topright
        self.back_button.rect.top += 210
        self.back_button.rect.right -= 45
        self.downloading = False
        self.download_button = pyspy.gui.Button('download')
        self.download_button.set_callback(self.download)
        self.path = ''
        self.drawn = 0
        self.checked = 0
        self.updatesAvailable = False
        self.status = pyspy.levels.GUIDownloadStatus()
        self.status.rect.center = screenRect.center
        self.download_button.rect.centerx = self.status.rect.centerx
        self.download_button.rect.top = self.status.rect.bottom + 5

    def checkForUpdates(self, path):
        if path:
            updates = pyspy.levels.checkForUpdates(path=path)
        else:
            updates = pyspy.levels.checkForUpdates()
        return updates

    def update(self):
        if not self.checked:
            self.updates = self.checkForUpdates(self.path)
            self.checked = True
            if self.updates:
                self.status.set_text('Updates available')
            else:
                self.status.set_text('No updates available at this time')
            #TODO: Check whether this is the best place for this.
            self.gameControl.updated = False

    def download(self):
        self.downloading = True
        if self.updates:
            pyspy.levels.downloadUpdates(self.updates, statusObj=self.status)
            self.status.set_text('All updates downloaded, enjoy!')
            self.download_button.active = False
            self.gameControl.updated = True
        return True

    def reset(self, type):
        self.drawn = 0
        self.checked = 0
        self.status.reset()

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
            if self.download_button.rect.collidepoint(mousepos):
                self.download_button()

    def draw(self, background, screen):
        if not self.drawn:
            screen.blit(background, (0,0))
            self.back_button.draw(background, screen)
            self.status.set_drawables(background, screen)
            self.drawn = True
        else:
            self.status.draw()
            if self.updates:
                self.download_button.draw(background, screen)

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
        self.screenRect = screenRect
        self.score = pyspy.gui.Score()
        self.loaded = False
        self.indicator = pyspy.gui.LevelIndicator((screenRect.width, screenRect.height))
        self.images = []
                
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
                       'Correct': pyspy.original.states.Correct(self),
                       'Error': pyspy.original.states.Error(self)}

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
        # The user may have updated their levels, so need to check them
        # again.
        if self.gameControl.updated or self.loaded == False:
            self.levels = pyspy.levels.getLevels()
            self.images = []
            for i in self.levels:
                if pyspy.levels.checkLevel(i):
                    self.images.append(pyspy.images.SpyImage((640,480), i))
                else:
                    print "Generating level: %s" %(i)
                    pyspy.levels.generateLevel(i)
            self.loaded = True

        if self.levels:
            self.state = self.states['NextLevel']
            self.state.enter()
        else:
            err = "No levels found, try updating levels from main menu."
            self.state = self.states['Error']
            self.state.set_error_message(err)
            self.state.enter()

    def draw(self, background, screen):
        self.state.draw(background, screen)


