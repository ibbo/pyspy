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

"""A generic image class for storing info about the images"""
import os
import random
import pygame
import math
import re
import pyspy
from pygame.locals import *
from pyspy.constants import *

# All images in the game are set to this value
IMAGE_SIZE = (640,480)

class SpyImage(pygame.Surface):
    def __init__(self,size,name):
        pygame.Surface.__init__(self,size)
        self.name = name
        self.image = None
        self.rect = None
        self.info = pyspy.images.ImageInfo(name + '.png')
        self.mask = []
        self.levels = self.load_levels()
        self.font = pygame.font.Font(
                os.path.join(FONT_DIR,'FreeMono.ttf'), 36)
        self.clue = pyspy.clue.ClueImage()
       
    def load_image(self):
        self.image, self.rect = pyspy.utilities.load_png(self.name,
                rootpath=LEVEL_DIR)
        self.blit(self.image, (0,0))

    def load_levels(self):
        levels = {'ispy':[], 'spythis':[]}
        for i in self.info.masks:
            if i.spythis:
                levels['spythis'].append(i.level)
            else:
                levels['ispy'].append(i.level)
        return levels

    def set_mask(self, level=1):
        difficulty = pyspy.levels.convertLevelToDifficulty(level)
        # Take a random mask
        masks = [i for i in self.info.masks 
                    if i.level == difficulty and not i.used]
        if len(masks) > 0:
            self.mask = masks[random.randint(0,len(masks)-1)]
        else:
            self.mask = []
            print "No levels found"
            return None
        self.clue.reset(self.mask.clue)
        self.mask.load_mask()
        self.mask.used = True

    def set_spythis_masks(self):
        # Take 5 random masks
        random.shuffle(self.info.masks)
        if len(self.info.masks) > 0:
            self.masks = self.info.masks[:5]
            [i.load_mask() for i in self.masks]
            return True
        else:
            self.mask = []
            print "No levels found"
            return False

class ImageInfo:
    def __init__(self, filename, path=LEVEL_DIR):
        self.basefile = filename
        self.has_spythis = False
        self.masks = self.initMasks(path)
        
    def initMasks(self, path):
        base_name = pyspy.utilities.strip_ext(self.basefile)
        masks, self.has_spythis = pyspy.levels.getMasksForLevel(base_name)
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
    def __init__(self, filename, level, clue):
        self.filename = filename
        self.level = level
        self.clue = clue
        self.found = False
        self.dirty = False
        self.used = False
        if '#' in self.clue:
            self.spythis = True
        else:
            self.spythis = False
        #TODO: Implement a bounding box calculator
        #self.boundingBox = self.calculateBoundingBox()

    def __str__(self):
        return self.clue + ' level: ' + str(self.level)

    def load_mask(self):
        self.image, self.rect = \
                pyspy.utilities.load_png(self.filename, rootpath=LEVEL_DIR)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_rect = self.image.get_bounding_rect()
        self.spythis_rect = Rect(self.mask_rect)

    def get_distance(self, pos):
        masks = self.mask.connected_components()
        outlines = [i for j in masks for i in j.outline(10)]
        dist = [math.sqrt((pos[0]-i[0])**2 +(pos[1]-i[1])**2) for i in outlines]
        return min(dist)

    def reset(self):
        self.found = False
        self.dirty = False

if __name__ == '__main__':
    i = ImageInfo('bookcase.png')
    print i
