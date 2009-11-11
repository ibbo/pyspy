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


import pygame, os
from pyspy.constants import *
from pyspy.utilities import *

if DEBUG:
    import pdb

class MenuItem():
    def __init__(self, text, index):
        self.font = pygame.font.Font(os.path.join('fonts', TEXT_FONT), 
                                        MENU_SIZE_NORMAL)
        self.bigFont = pygame.font.Font(os.path.join('fonts', TEXT_FONT), 
                                        MENU_SIZE_BIG)
        self.selected = 0
        self.text = text
        self.index = index
        self.renderedText = {}
        self.renderText()

    def select(self):
        self.selected = 1
        self.renderText()

    def deselect(self):
        self.selected = 0
        self.renderText()

    def renderText(self):
        if self.selected:
            if not self.renderedText.has_key('big'):
                self.renderedText['big'] = self.bigFont.render(self.text, 1, 
                                                MENU_SELECTED_COLOUR)
            self.textImage = self.renderedText['big']
        else:
            if not self.renderedText.has_key('normal'):
                self.renderedText['normal'] = self.font.render(self.text, 1, 
                                                MENU_COLOUR)
            self.textImage = self.renderedText['normal']
        self.rect = self.textImage.get_rect()

    def draw(self, background, screen):
        screen.blit(self.textImage, self.rect)
        return self.rect

class Menu:
    def __init__(self, items, move_sound=[]):
        self.items = [MenuItem(i,j) for i,j in zip(items, range(len(items)))]
        self.move_sound = move_sound
        self.selectedItem = []
        self.pointer, self.pointerRect = load_png('mag')
        self.dirty_rects = []
        self.reset()

    def setPositions(self, backgroundRect):
        totalHeight = 0
        for i in self.items:
            totalHeight = totalHeight + i.rect.height
        totalHeight = totalHeight + MENU_PADDING*(len(self.items) - 1)
        startPos = backgroundRect.centery - totalHeight/2
        for i in self.items:
            i.rect.centerx = backgroundRect.centerx
            i.rect.centery = startPos
            startPos = startPos + i.rect.height/2 + MENU_PADDING

    def reset(self):
        if self.selectedItem:
            self.selectedItem.deselect()
        self.selectedItem = self.items[0]
        self.selectedItem.select()

    def draw(self, background, screen):
        for rect in self.dirty_rects:
            screen.blit(background, rect, rect)
            self.dirty_rects = []
        for i in self.items:
            self.dirty_rects.append(i.draw(background, screen))
            if i.selected:
                self.pointerRect.centerx = i.rect.left - 50
                self.pointerRect.centery = i.rect.centery
                screen.blit(self.pointer, self.pointerRect)
                self.dirty_rects.append(self.pointerRect)
    
    def collide(self, point):
        for i in self.items:
            if i.rect.collidepoint(point):
                if i.selected == 0:
                    self.move_sound.play()
                    for j in self.items:
                        j.deselect()
                    i.select()
                    self.selectedItem = i
                return
        
    def selectNext(self, direction="down"):
        if direction == "down":
            nextItem = 1
        elif direction == "up":
            nextItem = -1
        else:
            raise ValueError, "Direction must be either 'up' or 'down'"
        if self.selectedItem.index + nextItem < len(self.items) and \
                self.selectedItem.index + nextItem >= 0:
            self.move_sound.play()
            self.selectedItem.deselect()
            self.selectedItem = self.items[self.selectedItem.index + nextItem]
            self.selectedItem.select()
