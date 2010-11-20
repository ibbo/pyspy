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


