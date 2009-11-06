#!/usr/bin/python
# Just defines a dictionary with all the relevant information for building
# image info classes.
#TODO: Make the naming include the level, and then this can be loaded automatically
import cPickle as pickle
import os

def addClue(imageName, clue, level, path=''):
    levelList = getLevelList(path)
    if levelList.has_key(imageName):
        levelList[imageName][clue] = level
    else:
        levelList[imageName] = {clue:level}
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

    f = file(imageListPath, "r")
    levelList = pickle.load(f)
    f.close()
    print levelList
    return levelList
