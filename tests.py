#!/usr/bin/python

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
