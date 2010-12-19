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
import math
import pygame
import pyspy
from pygame.locals import *
from pyspy.constants import *

class Error(pyspy.states.GameState):
    def __init__(self, gameScreen):
        pyspy.states.GameState.__init__(self, gameScreen)
        self.font = pygame.font.Font(os.path.join(FONT_DIR,MONO_FONT), 20)

    def set_error_message(self, message):
        self.text = self.font.render('Error: '+message,
                      1, pygame.Color('black'), pygame.Color('white'))

    def enter(self):
        self.delay = 250

    def update(self):
        if self.delay > 0:
            self.delay -= 1
        else:
            self.gameControl.music.unpause_track()
            self.gameScreen.quit()

    def eventHandle(self):
        # Don't allow escaping to main menu from here.
        pyspy.states.GameState.eventHandle(self)

    def draw(self, background, screen):
        screen.blit(background, (0,0))
        rect = self.text.get_rect()
        screen_rect = screen.get_rect()
        rect.center = screen_rect.center
        screen.blit(self.text, rect)


class Correct(pyspy.states.GameState):
    def __init__(self, gameScreen):
        pyspy.states.GameState.__init__(self,gameScreen)

    def enter(self):
        self.time_left = 100
        pygame.mouse.set_visible(False)
        self.gameScreen.image.clue.show_all()
        self.image = self.gameScreen.image
        self.image.set_alpha(127)
        self.drawn = 0

    def leave(self):
        self.image.set_alpha(255)
        pygame.mouse.set_visible(True)

    def update(self):
        if self.time_left > 0:
            self.time_left -= 1
        elif self.time_left == 0:
            self.gameScreen.state = self.gameScreen.states['NextLevel']
            self.gameScreen.state.enter()
            self.leave()
        else:
            raise ValueError('time_left cannot be negative')

    def eventHandle(self):
        pyspy.states.GameState.eventHandle(self)

    def draw(self, background, screen):
        if not self.drawn:
            screen.blit(background, self.image.rect, self.image.rect)
            screen.blit(self.image, (X_OFFSET, Y_OFFSET))
            old_text_rect = self.gameScreen.text_rect
            self.text_rect = self.image.clue.image.get_rect()
            self.text_rect.topleft = old_text_rect.topleft
            self.text_rect.width = self.image.rect.width
            screen.blit(background, self.text_rect, self.text_rect)
            screen.blit(self.image.clue.image, self.gameScreen.text_rect)
            # All this code is to convert the binary mask into an area of
            # the image rect and blit it to the screen.
            self.image.set_alpha(255)
            new = pygame.Surface((self.image.rect.width,
                                  self.image.rect.height), pygame.SRCALPHA)
            new.blit(self.image, (0,0))
            #screen.blit(self.image.mask.image, (X_OFFSET, Y_OFFSET))
            brects = self.image.mask.mask.get_bounding_rects()
            self.image.mask.mask.invert()
            for brect in brects:
                for i in range(brect.width):
                    for j in range(brect.height):
                        x = i+brect.left
                        y = j+brect.top
                        if self.image.mask.mask.get_at((x, y)):
                            new.set_at((x, y), (0,0,0,0))
                posrect = Rect(brect)
                posrect.top += Y_OFFSET
                posrect.left += X_OFFSET
                screen.blit(new, posrect, brect)
            self.image.mask.mask.invert()
            self.drawn = 1
            if DEBUG and DEBUG_DRAW_OUTLINE:
                for i in brects:
                    i.left = i.left + X_OFFSET
                    i.top = i.top + Y_OFFSET
                    pygame.draw.rect(screen, (255,255,255),i,2)

class GameOver(pyspy.states.GameState):
    def __init__(self, gameScreen):
        pyspy.states.GameState.__init__(self,gameScreen)
        self.font = pygame.font.Font(os.path.join(FONT_DIR,TEXT_FONT), 50)
        self.delay = 250
        self.buttons = gameScreen.buttons
        self.won_sound = pyspy.sound.SoundEffect(os.path.join(SOUND_DIR,
            'brass_fanfare_4.wav'))

    def enter(self, won):
        self.delay = 250
        if won:
            text = 'You have won!'
            self.gameControl.music.pause_track()
            self.won_sound.play()
        else:
            text = 'Game Over'

        self.won = won
        self.text = self.font.render(text, 1, (255,255,255),(0,0,80))
        self.text.set_colorkey([0,0,80])

        # Reset buttons TODO(need a way to separate bonus buttons and music
        # control buttons)
        self.buttons['unshuffle'].reset()
        self.buttons['reveal'].reset()
        self.buttons['more_letters'].reset()

    def update(self):
        if self.delay > 0:
            self.delay -= 1
        else:
            self.gameControl.music.unpause_track()
            self.gameScreen.score.reset()
            self.gameScreen.quit()

    def eventHandle(self):
        # Don't allow escaping to main menu from here.
        #pyspy.states.GameState.eventHandle(self)
        pass

    def draw(self, background, screen):
        screen.blit(background, (0,0))
        rect = self.text.get_rect()
        screen_rect = screen.get_rect()
        rect.bottomleft = (screen_rect.width/2 - rect.width/2,
                           screen_rect.height/2-rect.height/2)
        if self.won:
            rect.top += int(100*math.sin(self.delay*2*math.pi/40))
        screen.blit(self.text, rect.bottomleft)
        self.gameScreen.score.changed = True
        self.gameScreen.score.draw(background, screen)

#TODO: Implement cool transition effect
class NextLevel(pyspy.states.GameState):
    def __init__(self, gameScreen):
        pyspy.states.GameState.__init__(self,gameScreen)
        self.buttons = self.gameScreen.buttons
        self.buttons['unshuffle'] = pyspy.gui.Button('unshuffle')
        self.buttons['more_letters'] = pyspy.gui.Button('more_letters')
        self.buttons['reveal'] = pyspy.gui.Button('reveal')
        self.gameScreen.buttons = self.buttons
        self.static_font = pygame.font.Font(
                os.path.join(FONT_DIR,TEXT_FONT), 28)
        self.gameScreen.static_text = self.static_font.render(
                'I spy with my little eye, something beginning with:',\
                        1,(221,255,33))
        self.static_text = self.gameScreen.static_text
        self.gameScreen.static_text_rect = self.static_text.get_rect()
        self.static_text_rect = self.gameScreen.static_text_rect
        self.drawn_once = False

    def enter(self):
        self.gameScreen.level += 1
        self.level_exists = self.gameScreen.set_level(self.gameScreen.level)
        self.gameScreen.image.load_image()
        self.image = self.gameScreen.image
        self.delay = 1
        pygame.mouse.set_visible(True)
        self.init_layout()
        

    def update(self):
        if self.gameScreen.level > 10:
            self.gameScreen.state = self.gameScreen.states['GameOver']
            self.gameScreen.state.enter(1)
            return
        if self.delay == 0:
            self.updateParent()
            self.gameScreen.state = self.gameScreen.states['Playing']
            self.gameScreen.state.enter()
        else:
            self.delay -= 1

    def updateParent(self):
        self.gameScreen.buttons = self.buttons
        self.gameScreen.image = self.image
        self.gameScreen.text_rect = self.text_rect
        self.gameScreen.static_text_rect = self.static_text_rect

    def eventHandle(self):
        pyspy.states.GameState.eventHandle(self)

    def init_layout(self):
        # Set the image position
        self.image = self.gameScreen.image
        self.image.rect.topleft = (X_OFFSET, Y_OFFSET)
        self.image.mask.rect.topleft = self.image.rect.topleft
        self.gameScreen.score.rect.topright = \
                self.gameScreen.screenRect.topright
        self.gameScreen.score.rect.move_ip(-20, 210)
        if not self.drawn_once:
            self.static_text_rect.topleft = self.image.rect.bottomleft
            self.static_text_rect.centery += 5
            self.text_rect = self.image.clue.image.get_rect()
            self.text_rect.topleft = self.static_text_rect.bottomleft
            self.buttons['unshuffle'].rect.topleft = \
                self.image.rect.bottomleft
            self.buttons['unshuffle'].rect.move_ip(0, 100)
            self.buttons['more_letters'].rect.bottomleft = \
                self.buttons['unshuffle'].rect.bottomright
            self.buttons['more_letters'].rect.move_ip(20, 0)
            self.buttons['reveal'].rect.bottomleft = \
                self.buttons['more_letters'].rect.bottomright
            self.buttons['reveal'].rect.move_ip(20, 0)
            self.buttons['play'].rect.topleft = \
                self.buttons['unshuffle'].rect.bottomleft
            self.buttons['play'].rect.move_ip(0, 10)
            self.buttons['pause'].rect.topleft = \
                self.buttons['play'].rect.topright
            self.buttons['pause'].rect.move_ip(5, 0)
            self.buttons['next'].rect.topleft = \
                self.buttons['pause'].rect.topright
            self.buttons['next'].rect.move_ip(5, 0)
            self.drawn_once = True

    def draw(self, background, screen):
        screen.blit(background, (0, 0))
        screen.blit(self.image, self.image.rect)
        screen.blit(self.static_text, self.static_text_rect)
        screen.blit(self.image.clue.image, self.text_rect)
        self.gameScreen.indicator.draw(self.gameScreen.level)
        screen.blit(self.gameScreen.indicator,
                self.gameScreen.indicator.rect)

        for button in self.buttons.values():
            button.draw(background, screen)
        self.gameScreen.score.draw(background, screen)

class Playing(pyspy.states.GameState):
    def __init__(self, gameScreen):
        pyspy.states.GameState.__init__(self,gameScreen)
        timer_delay = TIMER_DELAY['slow']
        self.timer = pyspy.timer.Timer(timer_delay[0], timer_delay[1])
        self.buttons = self.gameScreen.buttons
        self.buttons['unshuffle'].set_callback(
                pyspy.bonus.Bonus(self.unshuffle_bonus, SHUFFLE_TIMES))
        self.buttons['reveal'].set_callback(
                pyspy.bonus.Bonus(self.reveal_bonus, REVEALS))
        self.buttons['more_letters'].set_callback(
                pyspy.bonus.Bonus(self.more_letters_bonus, ADD_TIMES))
        self.yipee_sound = pyspy.sound.SoundEffect(
                os.path.join(SOUND_DIR, 'yipee.wav'))
        self.indicator = pyspy.effects.DistanceIndicator()

    def enter(self):
        self.image = self.gameScreen.image
        self.text_rect = self.gameScreen.text_rect
        self.timer.reset()
        self.reset()
        level = self.gameScreen.level
        if level <= 1:
            self.timer.set_delay(*TIMER_DELAY['slow'])
        if level > 1 and level <= 3:
            self.timer.set_delay(*TIMER_DELAY['medium'])
        elif level > 3 and level <= 7:
            self.timer.set_delay(*TIMER_DELAY['fast'])
        elif level > 7 and level <= 9:
            self.timer.set_delay(*TIMER_DELAY['very fast'])
        elif level > 9:
            self.timer.set_delay(*TIMER_DELAY['impossible'])
            
        pygame.mouse.set_cursor(*pygame.cursors.load_xbm(
            os.path.join(CURSOR_DIR, 'mag.xbm'),
            os.path.join(CURSOR_DIR, 'mag-mask.xbm')))
        
    def update(self):
        self.indicator.update()
        game_over = self.timer.update()
        if game_over:
            self.gameScreen.state = self.gameScreen.states['GameOver']
            self.gameScreen.state.enter(0)

    def eventHandle(self):
        pyspy.states.GameState.eventHandle(self)
        if self.gameControl.gameEvent.newkeys[K_u]:
            self.buttons['unshuffle']()
        if self.gameControl.gameEvent.newkeys[K_m]:
            self.buttons['more_letters']()
        if self.gameControl.gameEvent.newkeys[K_r]:
            self.buttons['reveal']()
        mousepos = self.gameControl.gameEvent.mousePos
        if self.gameControl.gameEvent.mouseButtons[0]:
            if self.image.rect.collidepoint(mousepos):
                x = mousepos[0]-self.image.rect.left
                y = mousepos[1]-self.image.rect.top
                if self.image.mask.mask.get_at((x,y)):
                    self.yipee_sound.play()
                    self.gameScreen.score += self.timer.time_bar.width
                    self.gameScreen.state = self.gameScreen.states['Correct']
                    self.gameScreen.state.enter()
                else:
                    self.image.clue.add_letter()
                    if self.image.clue.allShown:
                        if self.buttons['more_letters'].active:
                            self.buttons['more_letters'].toggle_active()
                        if self.image.clue.unshuffled:
                            if self.buttons['reveal'].active:
                                self.buttons['reveal'].toggle_active()
                    self.timer.remove_time()
                    self.indicator.set_pos(mousepos[0], mousepos[1])
                    # Need to set the colour of the indicator based on the
                    # distance away from the object to find. 
                    distance = self.image.mask.get_distance((x,y))
                    self.indicator.set_colour(distance)
                    self.indicator.show = True
                    self.gameScreen.score -= distance
            else:
                for button in self.buttons.values():
                    if button.rect.collidepoint(mousepos) and button.active:
                        button()
                        
    def draw(self, background, screen):
        self.indicator.draw(background, screen, self.image)
        timer_rect = self.timer.get_rect()
        timer_rect.topleft = (X_OFFSET,10)
        screen.blit(background, timer_rect, timer_rect)
        screen.blit(self.timer, timer_rect)
        old_text_rect = self.text_rect
        self.text_rect = self.image.clue.image.get_rect()
        self.text_rect.topleft = old_text_rect.topleft
        self.text_rect.width = self.image.rect.width
        screen.blit(background, self.text_rect, self.text_rect)
        screen.blit(self.image.clue.image, self.text_rect)
        #FIXME: Shouldn't need to blit this every time.
        screen.blit(background, self.gameScreen.static_text_rect,
                self.gameScreen.static_text_rect)
        screen.blit(self.gameScreen.static_text,
                    self.gameScreen.static_text_rect)
        #FIXME: Shouldn't have to manually let the score know to redraw
        self.gameScreen.score.changed = True
        self.gameScreen.score.draw(background, screen)
        # Re-draw dirty rects
        for button in self.buttons.values():
            if button.dirty:
                button.draw(background, screen)

    def reset(self):
        self.indicator.reset()
        for i in self.buttons.values():
            #FIXME: Need different class for bonus buttons
            if hasattr(i.callback, 'counts'):
                if i.callback.counts > 0 and i.active == False:
                    i.toggle_active()
        
    def unshuffle_bonus(self):
        if not self.image.clue.unshuffled:
            self.image.clue.unshuffle()
            if self.timer.time_bar.width > WARNING_TIME:
                self.timer.remove_time(SHUFFLE_PENALTY)
            self.buttons['unshuffle'].toggle_active()
            if self.image.clue.allShown and self.buttons['reveal'].active:
                self.buttons['reveal'].toggle_active()
            return True
        return False

    def more_letters_bonus(self):
        if not self.image.clue.allShown:
            extra_letters = random.randint(2,4)
            self.image.clue.add_letter(extra_letters)
            if self.image.clue.allShown:
                self.buttons['more_letters'].toggle_active()
                if self.image.clue.unshuffled and \
                        self.buttons['reveal'].active:
                            self.buttons['reveal'].toggle_active()
            if self.timer.time_bar.width > WARNING_TIME:
                self.timer.remove_time(ADD_LETTER_PENALTY)
            return True
        return False

    def reveal_bonus(self):
        if not (self.image.clue.allShown and self.image.clue.unshuffled):
            self.image.clue.show_all()
            if self.timer.time_bar.width > WARNING_TIME:
                self.timer.remove_time(REVEAL_PENALTY)
            if self.buttons['unshuffle'].active:
                self.buttons['unshuffle'].toggle_active()
            if self.buttons['more_letters'].active:
                self.buttons['more_letters'].toggle_active()
            return True
        return False
 
