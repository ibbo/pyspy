#!/usr/bin/python
# A generic image class for storing info about the images
import os, pygame
from imageList import getLevelList
if __name__ != "__main__":
    import pySpy
else:
    import sys
    sys.path.append(os.path.split(os.getcwd())[0])
    import pySpy

class ImageInfo:
    def __init__(self, filename):
        self.basefile = filename
        self.masks = self.initMasks()
        
    def initMasks(self):
        levelList = getLevelList('levels')
        #try:
        clueList = levelList[pySpy.utilities.strip_ext(self.basefile)]
        #except:
        #    print "File: %s does not have any level data associated with it" \
        #            % (self.basefile)
        #    exit(-1)

        masks = []
        for clue in clueList:
            maskFile = pySpy.utilities.strip_ext(self.basefile) + \
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
                pySpy.utilities.load_png(filename, rootpath='levels')
        self.mask = pygame.mask.from_surface(self.image)
        self.level = level
        self.clue = clue
        #TODO: Implement a bounding box calculator
        #self.boundingBox = self.calculateBoundingBox()

    def __str__(self):
        return self.clue

if __name__ == '__main__':
    i = ImageInfo('bookcase.png')
    print i
