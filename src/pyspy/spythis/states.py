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
import pygame.gfxdraw
import pyspy
from pygame.locals import *
from pyspy.constants import *
from pyspy.utilities import add_to_rect, add_2D_vectors

class Correct(pyspy.states.GameState):
    def __init__(self, gameScreen):
        pyspy.states.GameState.__init__(self,gameScreen)

    def enter(self):
        self.time_left = CORRECT_TIME
        pygame.mouse.set_visible(False)
        self.image = self.gameScreen.image
        #self.image.set_alpha(127)
        self.drawn = 0

    def leave(self, nextState):
        self.image.set_alpha(255)
        pygame.mouse.set_visible(True)
        self.gameScreen.state = nextState
        self.gameScreen.state.enter()

    def update(self):
        if self.time_left > 0:
            self.time_left -= 1
            new_alpha = int(255.0/CORRECT_TIME*self.time_left)
            self.image.set_alpha(new_alpha)
        elif self.time_left == 0:
            self.leave(self.gameScreen.states['NextLevel'])
        else:
            raise ValueError('time_left cannot be negative')

    def eventHandle(self):
        pyspy.states.GameState.eventHandle(self)

    def draw(self, background, screen):
        screen.blit(background, self.image.rect, self.image.rect)
        screen.blit(self.image, (X_OFFSET, Y_OFFSET))
        if not self.drawn:
            for mask in self.image.masks:
                bg_rect = pyspy.utilities.add_to_rect(
                        mask.spythis_rect, (-2, -2, 4, 4))
                screen.blit(background, bg_rect, bg_rect)
            self.drawn = 1

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
        self.buttons['reveal'].reset()

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
        self.buttons['reveal'] = pyspy.gui.Button('reveal')
        self.gameScreen.buttons = self.buttons
        self.drawn_once = False
        self.draw_last = False

    def enter(self):
        self.gameScreen.level += 1
        if self.gameScreen.level > 10:
            self.leave()
            self.gameScreen.state = self.gameScreen.states['GameOver']
            self.gameScreen.state.enter(1)
            return
        self.level_exists = self.gameScreen.set_level(self.gameScreen.level)
        self.gameScreen.image.load_image()
        self.image = self.gameScreen.image
        self.image.set_alpha(0)
        self.delay = FADE_IN_TIME
        pygame.mouse.set_visible(True)
        self.gameScreen.active_masks = self.image.masks
        self.init_layout()
        self.drawn_once = False
        self.draw_last = False

    def leave(self):
        self.image.set_alpha(255)
        self.drawn_once = False

    def update(self):
        if self.delay == 0:
            self.leave()
            self.updateParent()
            self.gameScreen.state = self.gameScreen.states['Playing']
            self.gameScreen.state.enter()
        elif self.delay == 1:
            # Only draw the clues after we have faded in
            self.draw_last = True
            self.delay -= 1
        else:
            self.delay -= 1
        self.image.set_alpha(int(255 - 255.0/FADE_IN_TIME*self.delay))

    def updateParent(self):
        self.gameScreen.buttons = self.buttons
        self.gameScreen.image = self.image

    def eventHandle(self):
        pyspy.states.GameState.eventHandle(self)

    def init_layout(self):
        # Set the image position
        self.image = self.gameScreen.image
        self.image.rect.topleft = (X_OFFSET, Y_OFFSET)
        self.gameScreen.score.rect.topright = \
                self.gameScreen.screenRect.topright
        self.gameScreen.score.rect.move_ip(-40, 210)
        self.arrange_masks()
        if not self.drawn_once:
            self.buttons['reveal'].rect.centerx = \
                self.gameScreen.score.rect.centerx
            self.buttons['reveal'].rect.top = \
                self.gameScreen.score.rect.bottom
            self.buttons['reveal'].rect.move_ip(0, 5)
            self.buttons['play'].rect.topleft = \
                self.buttons['reveal'].rect.bottomleft
            self.buttons['play'].rect.move_ip(-30, 10)
            self.buttons['pause'].rect.topleft = \
                self.buttons['play'].rect.topright
            self.buttons['pause'].rect.move_ip(5, 0)
            self.buttons['next'].rect.topleft = \
                self.buttons['pause'].rect.topright
            self.buttons['next'].rect.move_ip(5, 0)

    def arrange_masks(self):
        last = pygame.rect.Rect(self.image.rect)
        last.bottom += 5
        last = last.bottomleft
        bottoms = []
        for mask in self.gameScreen.active_masks:
            mask.rect.topleft = self.image.rect.topleft
            mask.spythis_rect.topleft = add_2D_vectors(last, [5, 0])
            bottoms.append(mask.spythis_rect.bottom)
            last = mask.spythis_rect.topright

    def draw(self, background, screen):
        screen.blit(background, self.image.rect, self.image.rect)
        screen.blit(self.image, self.image.rect)
        if not self.drawn_once:
            screen.blit(background, (0,0))
            screen.blit(self.image, self.image.rect)
            self.gameScreen.indicator.draw(self.gameScreen.level)
            screen.blit(self.gameScreen.indicator,
                self.gameScreen.indicator.rect)
            for button in self.buttons.values():
                button.draw(background, screen)
            self.gameScreen.score.draw(background, screen)
            self.drawn_once = True
        if self.draw_last:
            for mask in self.gameScreen.active_masks:
                new, brects = self.gameScreen.image_from_mask(mask)
                radius = math.floor(mask.spythis_rect.w/2.0)
                screen.blit(new, mask.spythis_rect, mask.mask_rect)
                pygame.gfxdraw.aacircle(screen,
                        mask.spythis_rect.x + radius,
                        mask.spythis_rect.y + radius,
                        radius,
                        pygame.Color('white'))
            self.draw_last = False

class Playing(pyspy.states.GameState):
    def __init__(self, gameScreen):
        pyspy.states.GameState.__init__(self,gameScreen)
        timer_delay = TIMER_DELAY['slow']
        self.timer = pyspy.timer.Timer(timer_delay[0], timer_delay[1])
        self.buttons = self.gameScreen.buttons
        self.buttons['reveal'].set_callback(
                pyspy.bonus.Bonus(self.reveal_bonus, REVEALS))
        self.yipee_sound = pyspy.sound.SoundEffect(
                os.path.join(SOUND_DIR, 'yipee.wav'))
        self.indicator = pyspy.effects.DistanceIndicator()
        self.draw_tick = False
        self.tick_timer = TICK_TIME
        self.tick, self.tick_rect = pyspy.utilities.load_png('tick')
        self.clear_tick = False

    def enter(self):
        self.image = self.gameScreen.image
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
        if self.draw_tick:
            if self.tick_timer > 0:
                self.tick_timer -= 1
            else:
                self.draw_tick = False
                self.tick_timer = TICK_TIME
                self.tick.set_alpha(255)
                self.clear_tick = True
        game_over = self.timer.update()
        if game_over:
            self.gameScreen.state = self.gameScreen.states['GameOver']
            self.gameScreen.state.enter(0)
        masks_left = False
        for i in self.image.masks:
            if not i.found:
                masks_left = True
        if not masks_left:
            self.yipee_sound.play()
            self.gameScreen.score += self.timer.time_bar.width
            self.gameScreen.state = self.gameScreen.states['Correct']
            self.gameScreen.state.enter()

    def eventHandle(self):
        pyspy.states.GameState.eventHandle(self)
        if self.gameControl.gameEvent.newkeys[K_r]:
            self.buttons['reveal']()
        mousepos = self.gameControl.gameEvent.mousePos
        if self.gameControl.gameEvent.mouseButtons[0]:
            if self.image.rect.collidepoint(mousepos):
                x = mousepos[0]-self.image.rect.left
                y = mousepos[1]-self.image.rect.top
                distances = []
                found_mask = False
                for curMask in self.gameScreen.active_masks:
                    if curMask.mask.get_at((x,y)):
                        if not curMask.found:
                            curMask.found = True
                            curMask.dirty = True
                            found_mask = True
                    else:
                        if not curMask.found:
                            distances.append(curMask.get_distance((x,y)))
                if not found_mask:
                    self.timer.remove_time()
                    self.indicator.set_pos(mousepos[0], mousepos[1])
                    # Need to set the colour of the indicator based on the
                    # distance away from the object to find.
                    self.indicator.set_colour(min(distances))
                    self.indicator.show = True
                else:
                    self.draw_tick = True
                    self.tick_rect.center = \
                            (mousepos[0]+TICK_X_OFFSET,
                                    mousepos[1]+TICK_Y_OFFSET)
            else:
                for button in self.buttons.values():
                    if button.rect.collidepoint(mousepos) and button.active:
                        button()
    
    def arrange_masks(self):
        last = pygame.rect.Rect(self.image.rect)
        last.bottom += 5
        last = last.bottomleft
        bottoms = []
        for mask in self.gameScreen.active_masks:
            mask.rect.topleft = self.image.rect.topleft
            mask.spythis_rect.topleft = add_2D_vectors(last, [5, 0])
            bottoms.append(mask.spythis_rect.bottom)
            last = mask.spythis_rect.topright

    def redraw_masks(self, background, screen):
        for mask in self.gameScreen.active_masks:
            new, brects = self.gameScreen.image_from_mask(mask)
            radius = math.floor(mask.spythis_rect.w/2.0)
            screen.blit(new, mask.spythis_rect, mask.mask_rect)
            pygame.gfxdraw.aacircle(screen,
                    mask.spythis_rect.x + radius,
                    mask.spythis_rect.y + radius,
                    radius,
                    (255,255,255))

    def clear_masks(self, background, screen):
        for mask in self.gameScreen.active_masks:
            bg_rect = pyspy.utilities.add_to_rect(
                    mask.spythis_rect, (-2, -2, 4, 4))
            screen.blit(background, bg_rect, bg_rect)

    def draw(self, background, screen):
        timer_rect = self.timer.get_rect()
        timer_rect.topleft = (X_OFFSET,10)
        pos_rect = Rect(self.tick_rect)
        pos_rect.left += X_OFFSET
        pos_rect.top += Y_OFFSET
        blit_rect = Rect(self.tick_rect)
        blit_rect.left -= X_OFFSET
        blit_rect.top -= Y_OFFSET
        if self.draw_tick:
            screen.blit(background, self.tick_rect, self.tick_rect)
            screen.blit(self.image, self.tick_rect, blit_rect)
            # TODO: try using surfarrays to do this
            # This will require numpy, but if numpy isn't available
            # do the current thing instead.
            #new_alpha = 255/TICK_TIME*self.tick_timer
            #self.tick.set_alpha(new_alpha)
            screen.blit(self.tick, self.tick_rect)
        elif self.clear_tick:
            screen.blit(background, self.tick_rect, self.tick_rect)
            screen.blit(self.image, self.tick_rect, blit_rect)

        # Re-draw dirty rects
        for button in self.buttons.values():
            if button.dirty:
                button.draw(background, screen)
        
        # Flag if the masks need to be redrawn
        dirty = False
        toRemove = []
        for mask in self.gameScreen.active_masks:
            if mask.dirty:
                mask.dirty = False
                toRemove.append(mask)
                dirty = True
        if dirty:
            self.clear_masks(background, screen)
            for mask in toRemove:
                self.gameScreen.active_masks.remove(mask)
            self.arrange_masks()
            self.redraw_masks(background, screen)

        # Draw the distance indicator
        self.indicator.draw(background, screen, self.image)
        #FIXME: Shouldn't have to manually let the score know to redraw
        self.gameScreen.score.changed = True
        self.gameScreen.score.draw(background, screen)
        # The timer is drawn last to fix LP:681909
        screen.blit(background, timer_rect, timer_rect)
        screen.blit(self.timer, timer_rect)

    def reset(self):
        self.indicator.reset()
        self.masks_left = False
        self.draw_tick = False
        if self.image:
            for mask in self.image.masks:
                mask.reset()
        for i in self.buttons.values():
            #FIXME: Need different class for bonus buttons
            if hasattr(i.callback, 'counts'):
                if i.callback.counts > 0 and i.active == False:
                    i.toggle_active()
        
    def reveal_bonus(self):
        for i in self.image.masks:
            if not i.found:
                i.found = True
                i.dirty = True
                break
        if self.timer.time_bar.width > WARNING_TIME:
            self.timer.remove_time(REVEAL_PENALTY)
        return True
 
