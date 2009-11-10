#!/usr/bin/python
# pySpy_utilities - utility functions used in pySpy
import pygame, os
from pygame.locals import *
from constants import *
import pyspy.images as ims
import re

if DEBUG:
    import pdb

def strip_ext(filename):
    p = re.compile('(.*)\.[a-zA-Z0-9]*\s?$')
    m = p.match(filename)
    if m:
        return m.group(1)
    else:
        return filename

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

def fireRGB():
    colours = [(255,255,255,255), (255,255,0,64), (255,128,0,48),
            (128,0,64,32), (0,0,128,16), (0,0,0,0)]
    currentEntry = 255
    fireRGB = []
    for i,j in zip(colours[:-1],colours[1:]):
        for k in range(i[3],j[3],-1):
            interpolantFactor = \
                float(i[3]-currentEntry)/float(i[3]-j[3])
            r = int(i[0]+(j[0]-i[0])*interpolantFactor)
            g = int(i[1]+(j[1]-i[1])*interpolantFactor)
            b = int(i[2]+(j[2]-i[2])*interpolantFactor)
            fireRGB.append((r,g,b))
            currentEntry -= 1

    return fireRGB

