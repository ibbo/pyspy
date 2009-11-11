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

# Just defines a dictionary with all the relevant information for building
# image info classes.
#TODO: Make the naming include the level, and then this can be loaded automatically
import cPickle as pickle
import os

def addClue(imageName, clue, level, levelList=None):
    if not levelList:
        levelList = dict()
    if levelList.has_key(imageName):
        levelList[imageName][clue] = level
    else:
        levelList[imageName] = {clue:level}
    return levelList

def clearImage(imageName, levelList):
    if levelList:
        if levelList.has_key(imageName):
            del levelList[imageName]
    return levelList

def saveLevelList(levelList, path=''):
    if path != '':
        imageListPath = os.path.join(path, "imageList.dat")
    else:
        imageListPath = "imageList.dat"
    f = file(imageListPath, "w")
    pickle.dump(levelList, f)
    f.close()

def getLevelList(path=''):
    if path != '':
        imageListPath = os.path.join(path, "imageList.dat")
    else:
        imageListPath = "imageList.dat"
    
    try:
        f = file(imageListPath, "r")
    except IOError:
        return None

    levelList = pickle.load(f)
    f.close()
    return levelList
