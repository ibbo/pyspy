#!/usr/bin/python
# pySpy_utilities - utility functions used in pySpy
import pygame, os
from pygame.locals import *
from constants import *
import pySpy.images as ims

if DEBUG:
    import pdb

def strip_ext(filename):
    #FIXME: This assumes all file extensions are 3 characters long
    return filename[0:-4]

def load_png(name, rootpath='images'):
    """ Load image and return image object"""
    if name.endswith('.png'):    
	    fullname = os.path.join(rootpath, name)
    else:
	    fullname = os.path.join(rootpath, name+'.png')
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
            print 'Cannot load image:', fullname
            raise SystemExit, message
    return image, image.get_rect()

