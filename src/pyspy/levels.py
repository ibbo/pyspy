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
if os.name != 'nt':
    import curses
import pyspy
from pyspy.constants import *
import pygame
from pygame.locals import *

EASY = 0
MEDIUM = 1
HARD = 2
FIENDISH = 3
IMPOSSIBLE = 4

def parseLevelName(levelName):
    p = re.compile('^([a-zA-Z]+)_((?:[a-zA-Z]+|#[0-9]*)_+)([0-9]+)')
    m = p.match(levelName)
    if m:
        parsedName = {'base_name': m.group(1), 'clue': m.group(2),
                'level': m.group(3), 'filename': m.group(0)}
        return parsedName
    else:
        return None

def getLevels(path=LEVEL_DIR):
    p = re.compile('^[a-zA-Z]+\.png')
    levels = [pyspy.utilities.strip_ext(i) \
        for i in os.listdir(path) if p.match(i)]
    return levels

def checkLevel(level, path=LEVEL_DIR):
    return level+'.png' in os.listdir(path)

def checkForUpdates(url=SERVER_URL, localPath=LEVEL_DIR, remotePath=REMOTE_LEVEL_DIR):
    opener = urllib.FancyURLopener({})
    f = opener.open(url+'/'+remotePath+'/'+'levels.md5')
    levels = f.readlines()
    f.close()
    updateList = []
    updatedLevels = []
    for i in levels:
        m = hashlib.md5()
        remoteHash = i.split()
        try:
            localFile = open(os.path.join(localPath,remoteHash[1]), 'r')
        except IOError:
            # If there's an IOError we assume the file doesn't exist and
            # that there's a new level on the server. So add it to the list
            # of updates to be downloaded.
            parsedName = parseLevelName(remoteHash[1])
            if not parsedName:
                print "New image available: %s" %(remoteHash[1])
            elif parsedName['base_name'] not in updatedLevels:
                print "New levels available for: %s" %(parsedName['base_name'])
                updatedLevels.append(parsedName['base_name'])
            update = os.path.join(remotePath, remoteHash[1])
            updateList.append(update)
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
            print "Updates available for: %s" %(remoteHash[1])
            update = os.path.join(remotePath, remoteHash[1])
            updateList.append(update)
    return updateList

class DownloadStatus:
    def __init__(self):
        if os.name != 'nt':
            self.stdscr = curses.initscr()

    def __call__(self, blockCount, blockSize, totalSize):
        percent = float(blockCount)*float(blockSize)/float(totalSize)*100
        self.update(percent)

    def set_file(self, filename):
        self.filename = filename

    def update(self, percent):
        if os.name != 'nt':
            self.stdscr.erase()
            self.stdscr.addstr(0,0, "Downloading %s: %.1f percent complete"
                % (self.filename, percent))
            self.stdscr.refresh()
        else:
            print "Downloading %s: %.1f percent complete" % (self.filename, percent)

    def quit(self):
        if os.name != 'nt':
            curses.endwin()

class GUIDownloadStatus(DownloadStatus):
    def __init__(self):
        self.text_font = pygame.font.Font(os.path.join(FONT_DIR, MONO_FONT), 16)
        self.set_text('Checking for updates')
        self.width = 400
        self.height = 30
        self.progress_bar = pyspy.gui.ProgressBar(400, 30)
        self.rect = Rect(0,0,400,60)
        self.background = []
        self.screen = []

    def update(self, percent):
        self.progress_bar.update(percent)
        self.percent = percent
        self.draw()

    def set_drawables(self, background, screen):
        self.background = background
        self.screen = screen

    def set_text(self, text):
        self.text = self.text_font.render(text, 1, pygame.Color('black'))
    
    def set_file(self, filename):
        split_path = os.path.split(filename)
        if len(split_path) > 1:
            name = split_path[1]
        else:
            name = split_path[0]
        levelName = pyspy.utilities.strip_ext(name)
        parsed = parseLevelName(levelName)
        if parsed:
            self.set_text('Downloading levels for: "%s"' %(parsed['base_name']))
        else:
            self.set_text('Downloading image: "%s"' %levelName)

    def quit(self):
        pass

    def reset(self):
        self.percent = 0

    def draw(self):
        if self.background and self.screen:
            self.screen.blit(self.background, self.rect, self.rect)
            pygame.draw.rect(self.screen, pygame.Color('white'), self.rect)
            pygame.draw.rect(self.screen, pygame.Color('black'), self.rect, 3)
            self.text_rect = Rect(self.rect)
            self.text_rect.move_ip(5,7)
            self.screen.blit(self.text, self.text_rect)
            progress_rect = Rect(self.rect)
            progress_rect.top += 30
            self.screen.blit(self.progress_bar, progress_rect)
            pygame.display.flip()


def downloadUpdates(updateList, url=SERVER_URL,
                        localPath=LEVEL_DIR, statusObj=None):
    status = statusObj
    for i in updateList:
        status.set_file(i)
        try:
            urllib.urlretrieve(url+urllib.pathname2url(i),
                    os.path.join(localPath,os.path.split(i)[1]), status)
        finally:
            status.quit()
    status.quit()

def generateLevel(level, path=LEVEL_DIR):
    if os.name == 'nt':
        rootPath = os.environ['USERPROFILE']
    else:
        rootPath = os.environ['HOME']
    
    p = re.compile('\.gimp-2\.[0-9]')
    gimpFolder = [i for i in os.listdir(rootPath) if p.match(i)]
    if not gimpFolder:
        #FIXME: This should be more than just an "Exception"
        raise Exception, "Gimp installation not found"
    else:
        # Any Gimp will do so tae the first one found TODO: but we should
        # really use the latest available version.
        gimpFolder = gimpFolder[0]
    
    layerScriptPath = os.path.join(rootPath, gimpFolder, \
                                    'plug-ins', 'gimpSaveLayers.py')
    if not os.path.exists(layerScriptPath):
        shutil.copy(os.path.join(path,'gimpSaveLayers.py'), layerScriptPath)
    
    generateScriptPath = os.path.join(rootPath, gimpFolder, \
                                    'scripts', 'generate_levels.scm')
    if not os.path.exists(generateScriptPath):
        shutil.copy(os.path.join(path,'generate_levels.scm'), generateScriptPath)
    print "Running Gimp in batch mode to generate level: %s" %(level)
    sys.stdout.flush()
    if os.name == 'nt':
        gimpCommand = "gimp-2.6.exe"
    else:
        gimpCommand = "gimp"
    os.system(gimpCommand +
              " -i -b '(generate-levels \"%s.xcf\")' -b '(gimp-quit 0)'"
              %(os.path.join(path,level)))

if __name__ == '__main__':
    generateLevel('*')
