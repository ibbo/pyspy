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
from imageList import getLevelList
if __name__ != "__main__":
    import pyspy
else:
    import sys
    sys.path.append(os.path.split(os.getcwd())[0])
    import pyspy

class ImageInfo:
    def __init__(self, filename):
        self.basefile = filename
        self.masks = self.initMasks()
        
    def initMasks(self):
        levelList = getLevelList('levels')
        #try:
        clueList = levelList[pyspy.utilities.strip_ext(self.basefile)]
        #except:
        #    print "File: %s does not have any level data associated with it" \
        #            % (self.basefile)
        #    exit(-1)

        masks = []
        for clue in clueList:
            maskFile = pyspy.utilities.strip_ext(self.basefile) + \
                    '_' + clue + '.png'
            masks.append(ImageMask(maskFile, clueList[clue], \
                    clue.replace('_', ' ')))

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
        return self.clue

    def get_distance(self, pos):
        masks = self.mask.connected_components()
        outlines = [i for j in masks for i in j.outline(10)]
        dist = [math.sqrt((pos[0]-i[0])**2 +(pos[1]-i[1])**2) for i in outlines]
        return min(dist)

if __name__ == '__main__':
    i = ImageInfo('bookcase.png')
    print i
