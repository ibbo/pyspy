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
import pygame
import pyspy
import math
from pygame.locals import *
from pyspy.constants import *

class LevelNumber:
    def __init__(self, level, font, font_big):
        self.colour = (0,0,0)
        self.image = font.render(str(level), 1, self.colour)
        self.image_big = font_big.render(str(level), 1, self.colour)
        self.rect = self.image.get_rect()
        self.rect_big = self.image_big.get_rect()

class LevelIndicator(pygame.Surface):
    def __init__(self, size):
        self.font_big = pygame.font.Font(
                os.path.join(FONT_DIR,TEXT_FONT), 44)
        self.font = pygame.font.Font(
                os.path.join(FONT_DIR,TEXT_FONT), 36)

        self.mag_image, self.mag_rect = pyspy.utilities.load_png('level_mag')
        self.levels = range(1, MAX_LEVEL+1)
        self.level_images = []
        for i in reversed(self.levels):
            self.level_images.append(LevelNumber(i, self.font, self.font_big))

        maxWidth = max([i.rect_big.width for i in self.level_images])
        maxWidth = max([maxWidth, self.mag_rect.width])
        height = sum([i.rect.height for i in self.level_images])
        height += self.mag_rect.height
        size = (maxWidth, height)
        pygame.Surface.__init__(self, size, SRCALPHA)
        self.rect = self.get_rect()
        self.fill([0,0,0,0])
        for i in self.level_images:
            i.rect.centerx = self.rect.centerx
            i.rect_big.centerx = self.rect.centerx
        self.rect.left = X_OFFSET + 650
        self.rect.top = Y_OFFSET

    def draw(self, level):
        self.fill([0,0,0,0])
        for l,j,i in zip(self.level_images, self.levels, reversed(self.levels)):
            if i == level:
                l.rect.top = (j-1)*41 - 5 + 20
                self.blit(l.image_big, l.rect)
                self.mag_rect.center = l.rect.center
                self.mag_rect.centery += 5
                self.blit(self.mag_image, self.mag_rect)
            else:
                l.rect.top = (j-1)*41 + 20
                self.blit(l.image, l.rect)

class Score:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(os.path.join(FONT_DIR, MONO_FONT), 26)
        self.rect = []
        self.old_rect = []
        self.render()

    def reset(self):
        self.score = 0
        self.render()

    def __add__(self, amount):
        self.score += math.floor(amount)
        self.render()
        return self

    def __sub__(self, amount):
        self.score -= math.floor(amount)
        self.render()
        return self
    
    def render(self):
        self.text = self.font.render('Score: %5d' %(self.score),1,(0,0,0))
        if self.rect:
            self.old_rect = Rect(self.rect)
        self.rect = self.text.get_rect()
        if self.old_rect:
            self.rect.topleft = self.old_rect.topleft
        self.changed = True

    def draw(self, background, screen):
        if self.changed:
            screen.blit(background, self.rect, self.rect)
            screen.blit(self.text, self.rect)
            self.changed = False

class Button:
    def __init__(self, name, callback=None, can_disable=True):
        self.image, self.rect = pyspy.utilities.load_png(name)
        self.name = name.replace('_', ' ')
        self.font = pygame.font.Font(os.path.join(FONT_DIR, TEXT_FONT),
                                        BONUS_SIZE)
        self.active = True
        if can_disable:
            self.greyed, self.greyed_rect = \
                    pyspy.utilities.load_png('grey_' + name)
            self.greyed_rect = self.rect
        self.callback = callback
        self.dirty = False

    def __call__(self):
        if self.callback:
            if self.active:
                #FIXME: This is BAD, very, very BAD
                val = self.callback()
                if not val:
                    self.active = False
                self.dirty = True

    def reset(self):
        # FIXME: This is a hack to fix this there should be different types
        # of buttons.
        if hasattr(self.callback, 'reset'):
            self.callback.reset()
        self.active = True

    def set_callback(self, func):
        self.callback = func

    def toggle_active(self):
        self.active = not self.active
        self.dirty = True

    def draw(self, background, screen):
        screen.blit(background, self.rect, self.rect)
        if not self.active:
            screen.blit(self.greyed, self.rect)
        else:
            screen.blit(self.image, self.rect)
        #FIXME: Again the different types of buttons should be seperated out
        # into different classes.
        if hasattr(self.callback, 'counts'):
            text = self.font.render("%d" %(self.callback.counts), 1,
                                            BONUS_COUNT_COLOUR)
            screen.blit(text, (self.rect.x + 15, self.rect.bottom - 30))

class ProgressBar(pygame.Surface):
    def __init__(self, width, height, color=(211,255,200)):
        pygame.Surface.__init__(self, (width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.percent = 0
        self.color = color
        self.rect = self.get_rect()

    def update(self, percent):
        self.percent = percent
        self.fill((0,0,0,0))
        pygame.draw.rect(self, self.color, 
                pygame.Rect(0,0,self.percent/100*self.width, self.height))
        pygame.draw.rect(self, pygame.Color('black'),
                pygame.Rect(0,0,self.width,self.height),3)

