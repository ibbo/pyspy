#!/usr/bin/python
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
