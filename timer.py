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
from pygame.locals import *
from pyspy.constants import *

class Timer(pygame.Surface):
    def __init__(self, delay, step):
        pygame.Surface.__init__(self, (600,30))
        # TODO: All colours should be variables which can be changed
        self.fill((100,100,100))
        self.set_colorkey((100,100,100))
        self.font = pygame.font.Font(os.path.join('fonts',TEXT_FONT), 30)
        self.text = self.font.render('Time: ', 1, (211,255,33), (100,100,100))
        self.blit(self.text,(0,0))
        # TODO: The drawing rectangle should be passed as an argument
        self.time_bar = pygame.draw.rect(self, (211,255,200), pygame.Rect(100,0,500,30))
        self.counter = 0
        self._delay = delay
        self.step = step

    def set_delay(self, delay, step):
        self._delay = delay
        self.step = step

    def remove_time(self, amount = 50):
        if DEBUG:
            amount = 0
        if self.time_bar.width > 0:
            # TODO: The timer width should be a percentage
            # (This could also make it work like a waitbar...)
            if self.time_bar.width > amount:
                self.time_bar.width -= amount
            else:
                self.time_bar.width = 0
            self.fill((100,100,100))
            self.blit(self.text,(0,0))
            if self.time_bar.width < WARNING_TIME:
                pygame.draw.rect(self, (211,0,0), self.time_bar)
            else:
                pygame.draw.rect(self, (211,255,200), self.time_bar)

    def update(self):
        if self.time_bar.width > 0:
            if self.counter == self._delay:
                self.time_bar.width -= self.step
                self.counter = 0
            elif self.counter < self._delay:
                self.counter += 1
            else:
                raise ValueError('Counter cannot be greater than delay')
            self.fill((100,100,100))
            self.blit(self.text,(0,0))
            if self.time_bar.width < WARNING_TIME:
                pygame.draw.rect(self, (211,0,0), self.time_bar)
            else:
                pygame.draw.rect(self, (211,255,200), self.time_bar)
            return 0
        else:
            return 1

    def reset(self):
        self.time_bar.width = 500
        self.fill((100,100,100))
        self.blit(self.text,(0,0))
        self.counter = 0
        pygame.draw.rect(self, (211,255,200), self.time_bar)
