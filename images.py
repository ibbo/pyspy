#!/usr/bin/python
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
        centroid = self.mask.centroid()
        dist = math.sqrt((pos[0]-centroid[0])**2 + (pos[1]-centroid[1])**2)
        return dist

if __name__ == '__main__':
    i = ImageInfo('bookcase.png')
    print i
