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
import pyspy.instructions

if DEBUG:
    import pdb

class MenuScreen:
    def __init__(self, gameControlObj, screenRect, menu):
        self.gameControl = gameControlObj
        move_sound = pyspy.sound.SoundEffect(
                        os.path.join(SOUND_DIR,'menu_move.wav'))
        self.menu = menu
        self.menu.move_sound = move_sound
        self.firstDraw = 1

    def reset(self, type):
        self.menu.reset()
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        self.firstDraw = 1
        return

    def quit(self):
        self.gameControl.setMode("Main Menu")

    def eventHandle(self):
        mousepos = self.gameControl.gameEvent.mousePos
        collided = self.menu.collide(mousepos)
        # Check for quit
        if self.gameControl.gameEvent.newkeys[K_ESCAPE]:
            self.quit()

        # Move selection up and down
        if self.gameControl.gameEvent.newkeys[K_DOWN]:
            self.menu.selectNext("down")
            
        if self.gameControl.gameEvent.newkeys[K_UP]:
            self.menu.selectNext("up")

        # Process current selection
        # FIXME: Checking the menu item strings is a bad idea.
        if self.gameControl.gameEvent.newkeys[K_RETURN] or \
            self.gameControl.gameEvent.newkeys[K_KP_ENTER] or \
                (self.gameControl.gameEvent.mouseButtons[0] and \
                    collided):
            self.gameControl.setMode(self.menu.selectedItem.text)

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

class RootMenu(MenuScreen):
    def quit(self):
        self.gameControl.setMode("Quit")

class UpdateScreen:
    def __init__(self, gameControlObj, screenRect):
        self.gameControl = gameControlObj
        self.text_font = pygame.font.Font(os.path.join(FONT_DIR, MONO_FONT), 16)
        self.back_button = pyspy.gui.Button('back', can_disable=False)
        self.back_button.set_callback(self.quit)
        self.back_button.rect.topright = screenRect.topright
        self.back_button.rect.top += 210
        self.back_button.rect.right -= 45
        self.downloading = False
        self.download_button = pyspy.gui.Button('download')
        self.download_button.set_callback(self.download)
        self.paths = [REMOTE_LEVEL_DIR, REMOTE_LEVEL_DIR+'/spythis']
        self.drawn = 0
        self.checked = 0
        self.updatesAvailable = False
        self.status = pyspy.levels.GUIDownloadStatus()
        self.status.rect.center = screenRect.center
        self.download_button.rect.centerx = self.status.rect.centerx
        self.download_button.rect.top = self.status.rect.bottom + 5

    def checkForUpdates(self):
        updates = []
        for path in self.paths:
            [updates.append(i) for i in pyspy.levels.checkForUpdates(remotePath=path)]
        return updates

    def update(self):
        if not self.checked:
            self.updates = self.checkForUpdates()
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
        self.gameControl.setMode("Main Menu")
        return True

    def eventHandle(self):
        if self.gameControl.gameEvent.newkeys[K_ESCAPE]:
            self.quit()
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
        self.text_font = pygame.font.Font(os.path.join(FONT_DIR,MONO_FONT), 22)
        self.lines = self.get_instructions()
        self.back_button = pyspy.gui.Button('back', can_disable=False)
        self.back_button.set_callback(self.quit)
        self.back_button.rect.topright = screenRect.topright
        self.back_button.rect.top += 210
        self.back_button.rect.right -= 45
        self.drawn = 0

    def get_instructions(self):
        return pyspy.instructions.instructions

    def update(self):
        pass

    def reset(self, type=0):
        self.drawn = 0
        pass

    def quit(self):
        self.gameControl.setMode("Main Menu")
        return True

    def eventHandle(self):
        if self.gameControl.gameEvent.newkeys[K_ESCAPE]:
            self.quit()
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
        self.level_db = pyspy.database.DictDatabase()
        self.screenRect = screenRect
        self.score = pyspy.gui.Score()
        self.loaded = False
        self.indicator = pyspy.gui.LevelIndicator(
                (screenRect.width, screenRect.height))
        self.images = []
        self.image = None
       
        self.buttons = {'play': pyspy.gui.Button('play',
                callback=self.gameControl.music.unpause_track),
            'pause': pyspy.gui.Button('pause', callback=self.button_pause),
            'next': pyspy.gui.Button('next',
                callback=self.gameControl.music.next_track)}
        
    def button_pause(self):
        if self.gameControl.music.paused:
            self.gameControl.music.unpause_track()
        else:
            self.gameControl.music.pause_track()
        return True

    def set_image(self, imageObj):
        self.image = imageObj
    
    def update(self):
        self.state.update()

    def quit(self):
        self.gameControl.setMode("Main Menu")
        return True

    def set_level(self, level):
        """Search through images for those images which contain valid levels"""
        if level > 10:
            return False
        difficulty = pyspy.levels.convertLevelToDifficulty(level)
        valid_images = []
        for i in self.images:
            if self.spythis:
                if i.info.has_spythis:
                    valid_images.append(i)
            else:
                [valid_images.append(i) for j in i.info.masks if (j.level == difficulty and not j.used) and not j.spythis]

        # If there are images with levels to choose from, select a random one
        if valid_images:
            self.set_image(valid_images[random.randint(0,len(valid_images)-1)])
        else:
            return False
        return True

    def image_from_mask(self, mask):
        new = pygame.Surface((self.image.rect.width,
                              self.image.rect.height), pygame.SRCALPHA)
        new.blit(self.image, (0,0))
        #screen.blit(self.image.mask.image, (X_OFFSET, Y_OFFSET))
        brects = mask.mask.get_bounding_rects()
        mask.mask.invert()
        for brect in brects:
            for i in range(brect.width):
                for j in range(brect.height):
                    x = i+brect.left
                    y = j+brect.top
                    if mask.mask.get_at((x, y)):
                        new.set_at((x, y), (0,0,0,0))
        mask.mask.invert()
        return new, brects


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
                    pyspy.database.load_database_from_file(self.level_db, i)
                else:
                    print "Generating level: %s" %(i)
                    pyspy.levels.generateLevel(i)
            # Get all the images stored in the database and store them locally
            self.images = self.level_db.get_image(None)
            self.loaded = True

        for i in self.images:
            i.info.initMasks(self.level_db)
            for mask in i.info.masks:
                mask.used = False

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

class ISpyScreen(GameScreen):
    def __init__(self, gameControlObj, screenRect):
        GameScreen.__init__(self, gameControlObj, screenRect)
        self.spythis = False
        self.states = {'NextLevel': pyspy.original.states.NextLevel(self),
                       'Playing': pyspy.original.states.Playing(self),
                       'GameOver': pyspy.original.states.GameOver(self),
                       'Correct': pyspy.original.states.Correct(self),
                       'Error': pyspy.original.states.Error(self)}

    def set_image(self, imageObj):
        GameScreen.set_image(self, imageObj)
        self.image.set_mask(self.level)

class SpyThisScreen(GameScreen):
    def __init__(self, gameControlObj, screenRect):
        GameScreen.__init__(self, gameControlObj, screenRect)
        self.spythis = True
        self.states = {'NextLevel': pyspy.spythis.states.NextLevel(self),
                       'Playing': pyspy.spythis.states.Playing(self),
                       'GameOver': pyspy.spythis.states.GameOver(self),
                       'Correct': pyspy.spythis.states.Correct(self),
                       'Error': pyspy.original.states.Error(self)}

    def set_image(self, imageObj):
        GameScreen.set_image(self, imageObj)
        self.image.set_spythis_masks()
