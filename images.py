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

# A generic image class for storing info about the images
import os
import pygame
import math
import re
if __name__ != "__main__":
    import pyspy
else:
    import sys
    sys.path.append(os.path.split(os.getcwd())[0])
    import pyspy

class ImageInfo:
    def __init__(self, filename, path='levels'):
        self.basefile = filename
        self.masks = self.initMasks(path)
        
    def initMasks(self, path):
        #levelList = getLevelList('levels')
        base_name = pyspy.utilities.strip_ext(self.basefile)
        matches = [pyspy.levels.parseLevelName(i) for i in os.listdir(path) if base_name in i]
        matches = [i for i in matches if i]

        masks = []
        for match in matches:
            maskFile = match['filename'] + '.png'
            masks.append(ImageMask(maskFile, int(match['level']), \
                    match['clue'].replace('_', ' ').strip()))

        return masks


    def addMask(self, mask):
        self.masks.append(mask)

    def __str__(self):
        output = self.basefile + ': \n'
        output = output + '\tClues: \n'
        for i in self.masks:
            output = output + '\t\t' + str(i) + '\n'
        return output

class ImageMask:
    #TODO: Need to handle masks with more than one item in them
    def __init__(self, filename, level, clue):
        self.image, self.rect = \
                pyspy.utilities.load_png(filename, rootpath='levels')
        self.mask = pygame.mask.from_surface(self.image)
        self.level = level
        self.clue = clue
        #TODO: Implement a bounding box calculator
        #self.boundingBox = self.calculateBoundingBox()

    def __str__(self):
        return self.clue + str(self.level)

    def get_distance(self, pos):
        masks = self.mask.connected_components()
        outlines = [i for j in masks for i in j.outline(10)]
        dist = [math.sqrt((pos[0]-i[0])**2 +(pos[1]-i[1])**2) for i in outlines]
        return min(dist)

if __name__ == '__main__':
    i = ImageInfo('bookcase.png')
    print i
