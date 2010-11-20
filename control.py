import pyspy
from pyspy.constants import *

class QuitMode:
    def __init__(self):
        pass

    def eventHandle(self):
        pass

    def update(self):
        pass

    def reset(self, type):
        pass

    def draw(self, background, screen):
        pass

class GameControl:
    def __init__(self):
        self.gameEvent = pyspy.events.GameEvent()
        self.currentMode = 0
        self.modes = {}
        self.players = []
        self.playerCur = 0
        self.updated = False
        self.music = pyspy.sound.MusicControl()
		
    def addModes(self, newModes):
        """Insert the new mode into the modes list"""
        for k,v in newModes.items():
            self.modes[k] = v
        
    def setMode(self, newMode, type = 0):
        """Set the new mode, and reset it"""
        self.currentMode = self.modes[newMode]
        
        self.currentMode.reset(type)

    def update(self):
        """Update the current mode and events"""
        self.gameEvent.update()
        self.music.update()
        
        self.currentMode.eventHandle()
        self.currentMode.update()

    def draw(self, background, screen):
        self.currentMode.draw(background, screen)

