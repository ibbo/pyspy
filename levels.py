#!/usr/bin/python
import sys
sys.path.append(os.path.split(os.getcwd())[0])
import os
import re
import shutil
import hashlib
import urllib
from pyspy.constants import *

def checkForUpdates(url='http://pyspy.game-host.org/levels/', path='levels'):
    updatesAvailable = False
    opener = urllib.FancyURLopener({})
    f = opener.open(url+'levelList.txt')
    levels = f.readlines()
    f.close()
    for i in levels:
        m = hashlib.md5()
        f = opener.open(url+i)
        remoteHash = f.read().split()
        f.close()
        localFile = open(os.path.join(path,remoteHash[1]), 'r')
        m.update(localFile.read())
        localFile.close()
        sum = m.hexdigest()
        if DEBUG:
            print i
            print remoteHash[0]
            print sum
            print '\n'
        if sum != remoteHash[0]:
            print "Updates available for: %s" %(i)
            updatesAvailable = True
    return updatesAvailable


def generateLevel(level, path='levels'):
    #TODO: Make this check for other versions of the Gimp
    if not os.path.exists(os.path.join(os.environ['HOME'], '.gimp-2.6')):
        #FIXME: This should be more than just an "Exception"
        raise Exception, "Gimp installation not found"
    
    layerScriptPath = os.path.join(os.environ['HOME'], '.gimp-2.6', \
                                    'plug-ins', 'gimpSaveLayers.py')
    if not os.path.exists(layerScriptPath):
        shutil.copy(os.path.join(path,'gimpSaveLayers.py'), layerScriptPath)
    
    generateScriptPath = os.path.join(os.environ['HOME'], '.gimp-2.6', \
                                    'scripts', 'generate_levels.scm')
    if not os.path.exists(generateScriptPath):
        shutil.copy(os.path.join(path,'generate_levels.scm'), generateScriptPath)
    
    os.system("gimp -i -b '(generate-levels \"%s.xcf\")' -b '(gimp-quit 0)'"
                %(os.path.join(path,level)))

if __name__ == '__main__':
    generateLevel('*')
