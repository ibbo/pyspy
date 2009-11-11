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


import os, pygame
from pygame.locals import *
from main import MusicControl

def music_test():
    music_object = MusicControl()
    tracks_left = 1
    while tracks_left:
        try:
            tracks_left = music_object.next_track(0)
            print tracks_left
        except pygame.error, message:
            print "Error playing: %s" %(music_object.filenames[music_object.current_track])
            print "Here's what pygame says: %s" %(message)
        pygame.time.wait(1000)

if __name__ == "__main__":
    pygame.init()
    music_test()
    print "Music test complete, all files playable"
