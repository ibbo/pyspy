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

import sys
import os
sys.path.append(os.path.split(os.getcwd())[0])
import re
import shutil
import hashlib
import urllib
import curses
import pyspy
from pyspy.constants import *

def checkForUpdates(url=SERVER_URL, path='levels'):
    opener = urllib.FancyURLopener({})
    f = opener.open(url+'levelList.txt')
    levels = f.readlines()
    f.close()
    updateList = []
    for i in levels:
        updateFile = pyspy.utilities.strip_ext(i) + '.xcf'
        m = hashlib.md5()
        f = opener.open(url+i)
        remoteHash = f.read().split()
        f.close()
        try:
            localFile = open(os.path.join(path,remoteHash[1]), 'r')
        except IOError:
            # If there's an IOError we assume the file doesn't exist and
            # that there's a new level on the server. So add it to the list
            # of updates to be downloaded.
            print "New level available: %s" %(updateFile)
            updateList.append(updateFile)
            continue
        m.update(localFile.read())
        localFile.close()
        sum = m.hexdigest()
        if DEBUG:
            print i
            print remoteHash[0]
            print sum
            print '\n'
        if sum != remoteHash[0]:
            print "Updates available for: %s" %(updateFile)
            updateList.append(updateFile)
    return updateList

class DownloadStatus:
    def __init__(self):
        self.stdscr = curses.initscr()

    def __call__(self, blockCount, blockSize, totalSize):
        percent = float(blockCount)*float(blockSize)/float(totalSize)*100
        self.update(percent)

    def set_file(self, filename):
        self.filename = filename

    def update(self, percent):
        self.stdscr.addstr(0,0, "Downloading %s: %.1f percent complete"
                % (self.filename, percent))
        self.stdscr.refresh()

    def quit(self):
        curses.endwin()

def downloadUpdates(updateList, url=SERVER_URL, path='levels'):
    status = DownloadStatus()
    for i in updateList:
        status.set_file(i)
        try:
            urllib.urlretrieve(url+i, os.path.join(path,i), status)
        finally:
            status.quit()
    status.quit()

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
    print "Running Gimp in batch mode to generate level: %s" %(level)
    sys.stdout.flush()
    os.system("gimp -i -b '(generate-levels \"%s.xcf\")' -b '(gimp-quit 0)'"
                %(os.path.join(path,level)))

if __name__ == '__main__':
    generateLevel('*')
