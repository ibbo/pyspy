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
import pyspy
from pygame.locals import *
from pyspy.constants import *

class DistanceIndicator(pygame.Surface):
    def __init__(self):
        pygame.Surface.__init__(self, (100,100), pygame.SRCALPHA)
        self.anim_image, self.anim_rect = pyspy.utilities.load_png('hot.png')
        self.rect = self.get_rect()
        self.colours = pyspy.utilities.fireRGB()
        self.colour = pygame.Color(*self.colours[0])
        #self.colour.a = 0
        #self.fill(self.colour)
        self.anim_length = 10
        self.anim_pause = 2
        self.anim_tick = self.anim_length*self.anim_pause
        self.show = False
        self.dirty = False
        #self.set_alpha(127)

    def set_pos(self, left, top):
        self.rect.top = top - self.rect.height/2
        self.rect.left = left - self.rect.width/2

    def set_colour(self, distance):
        if distance < 0:
            distance = 0
        self.temp = 255 - int(distance/300*255)
        if self.temp < 0:
            self.temp = 0
        elif self.temp > 254:
            self.temp = 254
        self.colour = pygame.Color(*self.colours[self.temp])
        #self.colour.a = 127
        #self.fill(self.colour)

    def reset(self):
        self.anim_tick = self.anim_length*self.anim_pause
        self.show = False
        self.dirty = False

    def update(self):
        if self.show and self.anim_tick > 0:
            self.fill((0,0,0,0))
            x = self.rect.width/2
            y = self.rect.height/2
            frame = (self.anim_length*self.anim_pause -\
                            self.anim_tick)/self.anim_pause
            if self.temp > 220:
                frame_rect = Rect(frame*50, 0, 50, 50)
                self.blit(self.anim_image, (25, 20), frame_rect)
            else:
                radius = (frame+1)*2
                if radius > 13:
                    radius = 13
                pygame.draw.circle(self, self.colour, (x,y), radius, 2)
            self.anim_tick -= 1
        elif self.anim_tick == 0:
            self.show = False
            self.anim_tick = self.anim_length*self.anim_pause
            self.dirty = True

    def draw(self, background, screen, image):
        pos = Rect(self.rect)
        pos.top -= image.rect.top
        pos.left -= image.rect.left
        if self.show and self.anim_tick > 0:
            screen.blit(background, self.rect, self.rect)
            screen.blit(image, self.rect, pos)
            screen.blit(self, self.rect)
        elif self.dirty:
            screen.blit(background, self.rect, self.rect)
            screen.blit(image, image.rect)
            self.dirty = False


