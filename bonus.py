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

class Bonus:
    def __init__(self, bonus_function, counts):
        self.func = bonus_function
        self.counts = counts
        self.original_counts = counts

    def __call__(self):
        if self.counts > 0:
            applied = self.func()
            if applied:
                self.counts = self.counts - 1
        return self.counts

    def reset(self):
        self.counts = self.original_counts

