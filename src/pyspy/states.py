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
from pygame.locals import *
from pyspy.constants import *

class GameState:
    def __init__(self, gameScreen):
        self.gameScreen = gameScreen
        self.gameControl = gameScreen.gameControl

    def enter(self):
        pass

    def update(self):
        pass

    def eventHandle(self):
        if self.gameControl.gameEvent.newkeys[K_ESCAPE]:
            self.gameScreen.quit()

    def draw(self, background, screen):
        pass

    def reset(self):
        pass

