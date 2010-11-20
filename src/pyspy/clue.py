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
#clue.py - code for handling the clues in pySpy
import pygame, os, random, sys
import copy
sys.path.append(os.path.split(os.getcwd())[0])
from pyspy.constants import *

if DEBUG:
    import pdb

class Word(object):
    def __init__(self, text):
        self.text = text
        self.randomShow = False
    
    @property
    def text(self):
        return str(self)

    @text.setter
    def text(self, value):
        self._text = [(i,Letter(j)) for i, j in enumerate(value)]

    @text.deleter
    def text(self):
        del self._text

    def shuffle(self):
        text = copy.copy(self._text)
        locked_list = [self._text.pop(i[0]) for i in text
                                                if i[1].locked]
        random.shuffle(self._text)
        [self._text.insert(i[0], i) for i in locked_list]

    def unshuffle(self):
        self._text.sort()

    def lock_letter(self, index):
        self._text[index][1].lock()

    def hideAll(self):
        [i[1].hide() for i in self._text]

    def showAll(self):
        [i[1].show() for i in self._text]

    def getHidden(self):
        return [i[1] for i in self._text if not i[1].visible]

    def showNext(self):
        hidden = self.getHidden()
        if hidden:
            if self.randomShow:
                chosen = random.choice(hidden)
            else:
                chosen = hidden[0]
            chosen.show()
        else:
            return None
        return str(self)

    def __str__(self):
        return ''.join([i[1][0] for i in self._text])

class Letter(list):
    def __init__(self, letter):
        self.append(letter)
        self._letter = letter
        self.locked = 0
        self.visible = 1

    def lock(self):
        self.locked = 1

    def unlock(self):
        self.locked = 0

    def hide(self):
        if not self.locked:
            self[0] = '_'
            self.visible = 0

    def show(self):
        if not self.locked:
            self[0] = self._letter
            self.visible = 1

class Clue(object):
    def __init__(self, text):
        self.text = text

    @property
    def text(self):
        return str(self)

    @text.setter
    def text(self, value):
        self._text = [Word(i) for i in value.split()]

    @text.deleter
    def text(self, value):
        del self._text

    def shuffle(self):
        [i.shuffle() for i in self._text]

    def unshuffle(self):
        [i.unshuffle() for i in self._text]

    def show_next(self, count=1):
        shown = False
        for i in range(count):
            for j in self._text:
                shown = j.showNext()
                if shown:
                    break
        hidden = [i for j in self._text for i in j.getHidden()]
        if not hidden:
            shown = False
        return shown

    def lock_letter(self, letter_index, word_index=0):
        self._text[word_index].lock_letter(letter_index)

    def show_all(self):
        for i in self._text:
            i.showAll()

    def hide_all(self):
        for i in self._text:
            i.hideAll()

    def __str__(self):
        return ' '.join([i.text for i in self._text])

class ClueImage:
    def __init__(self):
        self.text = ''
        #TODO: Set the font size more carefully
        self.font = pygame.font.Font(os.path.join(FONT_DIR, 'FreeMono.ttf'), 36)
        self.colour = CLUE_COLOUR
        self.image_base = []
        self.image = self.font.render('', 1, self.colour)
        self.unshuffled = False
        self.allShown = False

    def reset(self, text):
        self.unshuffled = False
        self.clue = Clue(text)
        self.text = str(text)
        self.allShown = False
        self.clue.lock_letter(0)
        self.clue.hide_all()
        self.clue.shuffle()
        #self.image_base = self.set_text_base(text.split())
        self.render()
    
    def shuffle(self):
        self.clue.shuffle()
    
    def unshuffle(self):
        self.unshuffled = True
        self.clue.unshuffle()
        self.render()

    def render(self):
        toRender = ' '.join(str(self.clue))
        self.image = self.font.render(toRender, 1, self.colour)

    def add_letter(self, letters = 1):
        shown = self.clue.show_next(count=letters)
        if not shown:
        #    self.show_all()
            self.allShown = True
        self.render()
        
    def show_all(self):
        self.clue.unshuffle()
        self.clue.show_all()
        self.unshuffled = True
        self.render()
        self.allShown = True
