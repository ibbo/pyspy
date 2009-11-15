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
import os
import random
import pygame
import pyspy
from pyspy.constants import *

class SoundEffect(pygame.mixer.Sound):
    def __init__(self, path):
        pygame.mixer.Sound.__init__(self, path)

    def play(self):
        if SOUND:
            pygame.mixer.Sound.play(self)

class MusicControl:
    def __init__(self):
        self.music_dir = 'music'
        self.filenames = self.get_filenames()
        self.filenames = [i for i in self.filenames if i.endswith('.mid')\
                                                    or i.endswith('.ogg')]
        self.current_track = 0
        self.On = MUSIC
        self.paused = 0

    def get_filenames(self):
        return os.listdir(self.music_dir)

    def play_track(self, randomize = 1):
        if self.On:
            if len(self.filenames)-1 > 0:
                if randomize:
                    self.current_track = \
                            random.randint(0, len(self.filenames)-1)
                track = self.filenames[self.current_track]
                pygame.mixer.music.load(os.path.join(self.music_dir,track))
                pygame.mixer.music.play()
            return True
        return False

    def unpause_track(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = 0
        return True

    def pause_track(self):
        pygame.mixer.music.pause()
        self.paused = 1
        return True

    def next_track(self, randomize = 1):
        pygame.mixer.music.stop()
        if self.current_track < len(self.filenames)-2:
            if not randomize:
                self.current_track += 1
        else:
            return False
        self.play_track(randomize)
        return True

    def update(self):
        if self.On:
            if not pygame.mixer.music.get_busy():
                self.play_track()
 
