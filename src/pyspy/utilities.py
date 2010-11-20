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

def load_png(name, rootpath=IMAGE_DIR):
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
            print message
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

def check_version():
    """Check that compatible versions of pygame and python are being used"""
    pygame_ver = pygame.version.vernum
    if pygame_ver[0] < 1 or (pygame_ver[0] < 2 and pygame_ver[1] < 9):
        print "Requires pygame 1.9.0 or greater"
        sys.exit(0)
    python_ver = sys.version_info
    if python_ver[0] < 2 or (python_ver[0] > 1 and python_ver[1] < 6):
        print "Requires python 2.6 or greater"
        sys.exit(0)
    if python_ver[0] > 2:
        print "This is not yet compatible with python 3.0 or greater"
        sys.exit(0)

