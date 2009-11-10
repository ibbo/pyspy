#!/usr/bin/python

import sys, os, random, math, getopt
sys.path.append(os.path.split(os.getcwd())[0])
import pygame
from pygame.locals import *
import pyspy
from pyspy.utilities import *
import pyspy.clue as clue
from pyspy.constants import *
from pyspy.timer import Timer
from pyspy.menu import *
import pyspy.images as ims

if DEBUG:
    import pdb

class SpyImage(pygame.Surface):
    def __init__(self,size,name):
        pygame.Surface.__init__(self,size)
        self.image, self.rect = load_png(name, rootpath='levels')
        self.blit(self.image, (0,0))
        self.info = ims.ImageInfo(name + '.png')
        self.mask = []
        self.levels = self.load_levels()
        self.font = pygame.font.Font(os.path.join('fonts','FreeMono.ttf'), 36)
        self.clue = clue.ClueImage()
       
    def load_levels(self):
        levels = []
        for i in self.info.masks:
            levels.append(i.level)
        return levels

    def set_mask(self, level=1):
        # Take a random mask
        masks = [i for i in self.info.masks if i.level == level]
        if len(masks) > 0:
            self.mask = masks[random.randint(0,len(masks)-1)]
        else:
            self.mask = []
            print "No levels found"
            return self.mask
        self.clue.reset(self.mask.clue)
        # Replace this with a method of the clue class
        
class StartScreen:
    def __init__(self, gameControlObj, screenRect):
        self.gameControl = gameControlObj
        self.menuMax = 3
        move_sound = SoundEffect(os.path.join('sounds','menu_move.wav'))
        self.menu = Menu(["Play Game", "Instructions", "Quit"], move_sound)
        self.firstDraw = 1

    def reset(self, type):
        self.menu.reset()
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        self.firstDraw = 1
        return

    def eventHandle(self):
        if self.gameControl.gameEvent.mouseMoved:
            mousepos = self.gameControl.gameEvent.mousePos
            self.menu.collide(mousepos)
        # Check for quit
        if self.gameControl.gameEvent.newkeys[K_ESCAPE]:
            self.gameControl.setMode(QUIT)

        # Move selection up and down
        if self.gameControl.gameEvent.newkeys[K_DOWN]:
            self.menu.selectNext("down")
            
        if self.gameControl.gameEvent.newkeys[K_UP]:
            self.menu.selectNext("up")

        # Process current selection
        if self.gameControl.gameEvent.newkeys[K_RETURN] or \
            self.gameControl.gameEvent.newkeys[K_KP_ENTER] or \
                self.gameControl.gameEvent.mouseButtons[0]:
            if self.menu.selectedItem.text == "Play Game":
                self.gameControl.setMode(GAME)
            if self.menu.selectedItem.text == "Instructions":
                self.gameControl.setMode(INSTRUCTIONS)
            if self.menu.selectedItem.text == "Quit":
                self.gameControl.setMode(QUIT)

    def update(self):
        return

    def draw(self, background, screen):
        if self.firstDraw:
            screen.blit(background, (0, 0))
            self.firstDraw = 0
        # The size of the menu items changes when they are selected so we
        # have to set the positions before we draw them.
        self.menu.setPositions(background.get_rect())
        #Draw Everything
        self.menu.draw(background, screen)
        
  
class InstructionsScreen:
    def __init__(self, gameControlObj, screenRect):
        self.gameControl = gameControlObj
        self.text_font = pygame.font.Font(os.path.join('fonts',TEXT_FONT), 30)
        self.filename = 'Instructions.txt'
        self.lines = self.get_instructions()
        self.drawn = 0

    def get_instructions(self):
        f = file(self.filename, 'r')
        raw_lines = f.readlines()
        f.close()
        lines = [i.strip() for i in raw_lines]
        rendered_lines = []
        for i in lines:
            rendered_lines.append(self.text_font.render(i,1,(255,255,255), (0,0,0)))
        return rendered_lines

    def update(self):
        pass

    def reset(self, type=0):
        self.drawn = 0
        pass

    def eventHandle(self):
        if self.gameControl.gameEvent.newkeys[K_ESCAPE]:
            self.gameControl.setMode(MAIN_MENU)

    def draw(self, background, screen):
        if not self.drawn:
            screen.blit(background, (0,0))
            count = 0
            for i in self.lines:
                screen.blit(i, (50, 50 + count*30))
                count += 1
        self.drawn = 1

class Button:
    def __init__(self, name, callback=None):
        self.image, self.rect = load_png(name)
        self.name = name.replace('_', ' ')
        self.active = True
        self.greyed, self.greyed_rect = load_png('grey_' + name)
        self.greyed_rect = self.rect
        self.callback = callback
        self.dirty = False

    def __call__(self):
        if self.callback:
            val = self.callback()
            if not val:
                self.active = False
                self.dirty = True

    def reset(self):
        # FIXME: This is a hack to fix this there should be different types
        # of buttons.
        if hasattr(self.callback, 'reset'):
            self.callback.reset()
        self.active = True

    def set_callback(self, func):
        self.callback = func

    def toggle_active(self):
        self.active = not self.active

    def draw(self, background, screen):
        if not self.active:
            screen.blit(self.greyed, self.rect)
        else:
            screen.blit(self.image, self.rect)

class LevelNumber:
    def __init__(self, level, font, font_big):
        self.colour = (0,0,0)
        self.image = font.render(str(level), 1, self.colour)
        self.image_big = font_big.render(str(level), 1, self.colour)
        self.rect = self.image.get_rect()
        self.rect_big = self.image_big.get_rect()

class LevelIndicator(pygame.Surface):
    def __init__(self, size):
        self.font_big = pygame.font.Font(
                os.path.join('fonts',TEXT_FONT), 44)
        self.font = pygame.font.Font(
                os.path.join('fonts',TEXT_FONT), 36)

        self.mag_image, self.mag_rect = load_png('level_mag')
        self.levels = range(1, MAX_LEVEL+1)
        self.level_images = []
        for i in reversed(self.levels):
            self.level_images.append(LevelNumber(i, self.font, self.font_big))

        maxWidth = max([i.rect_big.width for i in self.level_images])
        maxWidth = max([maxWidth, self.mag_rect.width])
        height = sum([i.rect.height for i in self.level_images])
        height += self.mag_rect.height
        size = (maxWidth, height)
        pygame.Surface.__init__(self, size, SRCALPHA)
        self.rect = self.get_rect()
        self.fill([0,0,0,0])
        for i in self.level_images:
            i.rect.centerx = self.rect.centerx
            i.rect_big.centerx = self.rect.centerx
        self.rect.left = X_OFFSET + 650
        self.rect.top = Y_OFFSET

    def draw(self, level):
        self.fill([0,0,0,0])
        for l,j,i in zip(self.level_images, self.levels, reversed(self.levels)):
            if i == level:
                l.rect.top = (j-1)*41 - 5 + 20
                self.blit(l.image_big, l.rect)
                self.mag_rect.center = l.rect.center
                self.mag_rect.centery += 5
                self.blit(self.mag_image, self.mag_rect)
            else:
                l.rect.top = (j-1)*41 + 20
                self.blit(l.image, l.rect)
 
class GameState:
    def __init__(self, gameScreen):
        self.gameScreen = gameScreen
        self.gameControl = gameScreen.gameControl

    def enter(self):
        pass

    def update(self):
        pass

    def eventHandle(self):
        if self.gameControl.gameEvent.newkeys[K_ESCAPE]:
            self.gameControl.setMode(MAIN_MENU)

    def draw(self, background, screen):
        pass

    def reset(self):
        pass

class Correct(GameState):
    def __init__(self, gameScreen):
        GameState.__init__(self,gameScreen)

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
        GameState.eventHandle(self)

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
            screen.blit(self.image.mask.image, (X_OFFSET, Y_OFFSET))
            self.drawn = 1
            if DEBUG and DEBUG_DRAW_OUTLINE:
                for i in self.image.mask.mask.get_bounding_rects():
                    i.left = i.left + X_OFFSET
                    i.top = i.top + Y_OFFSET
                    pygame.draw.rect(screen, (255,255,255),i,2)

class CloseIndicator(pygame.Surface):
    def __init__(self):
        pygame.Surface.__init__(self, (100,100), pygame.SRCALPHA)
        self.rect = self.get_rect()
        self.colours = pyspy.utilities.fireRGB()
        self.colour = pygame.Color(*self.colours[0])
        self.colour.a = 127
        self.fill(self.colour)
        self.anim_length = 20
        self.anim_tick = self.anim_length
        self.show = False
        self.dirty = False
        self.set_alpha(127)

    def set_pos(self, left, top):
        self.rect.top = top - self.rect.height/2
        self.rect.left = left - self.rect.width/2

    def set_colour(self, distance):
        temp = int(distance/300*255)
        if temp > 254:
            temp = 254
        self.colour = pygame.Color(*self.colours[temp])
        self.colour.a = 127
        self.fill(self.colour)

    def reset(self):
        self.anim_tick = self.anim_length
        self.show = False
        self.dirty = False

    def update(self):
        if self.show and self.anim_tick > 0:
            self.anim_tick -= 1
        elif self.anim_tick == 0:
            self.show = False
            self.anim_tick = self.anim_length
            self.dirty = True

    def draw(self, background, screen, image):
        pos = Rect(self.rect)
        pos.top -= image.rect.top
        pos.left -= image.rect.left
        if self.show and self.anim_tick > 0:
            screen.blit(background, self.rect, self.rect)
            screen.blit(image, self.rect, pos)
            screen.blit(self, self.rect)
        elif self.dirty:
            screen.blit(background, self.rect, self.rect)
            screen.blit(image, image.rect)
            self.dirty = False

class Playing(GameState):
    def __init__(self, gameScreen):
        GameState.__init__(self,gameScreen)
        timer_delay = TIMER_DELAY['slow']
        self.timer = Timer(timer_delay[0], timer_delay[1])
        self.buttons = self.gameScreen.buttons
        self.buttons['unshuffle'].set_callback(
                Bonus(self.unshuffle_bonus, SHUFFLE_TIMES))
        self.buttons['reveal'].set_callback(
                Bonus(self.reveal_bonus, REVEALS))
        self.buttons['more_letters'].set_callback(
                Bonus(self.more_letters_bonus, ADD_TIMES))
        self.yipee_sound = SoundEffect(os.path.join('sounds', 'yipee.wav'))
        self.indicator = CloseIndicator()

    def enter(self):
        self.image = self.gameScreen.image
        self.text_rect = self.gameScreen.text_rect
        self.timer.reset()
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
            os.path.join('cursors', 'mag.xbm'),
            os.path.join('cursors', 'mag-mask.xbm')))
        
    def update(self):
        self.indicator.update()
        game_over = self.timer.update()
        if game_over:
            self.gameScreen.state = self.gameScreen.states['GameOver']
            self.gameScreen.state.enter(0)

    def eventHandle(self):
        GameState.eventHandle(self)
        if self.gameControl.gameEvent.newkeys[K_u]:
            self.unshuffle_bonus()
        if self.gameControl.gameEvent.newkeys[K_m]:
            self.more_letters_bonus()
        mousepos = self.gameControl.gameEvent.mousePos
        if self.gameControl.gameEvent.mouseButtons[0]:
            if self.image.rect.collidepoint(mousepos):
                x = mousepos[0]-self.image.rect.left
                y = mousepos[1]-self.image.rect.top
                if self.image.mask.mask.get_at((x,y)):
                    self.yipee_sound.play()
                    # Transition to Correct state
                    self.gameScreen.state = self.gameScreen.states['Correct']
                    self.gameScreen.state.enter()
                else:
                    self.image.clue.add_letter()
                    self.timer.remove_time()
                    self.indicator.set_pos(mousepos[0], mousepos[1])
                    # Need to set the colour of the indicator based on the
                    # distance away from the object to find. TODO: Need to
                    # find a way to get a measure of that distance.
                    distance = self.image.mask.get_distance((x,y))
                    self.indicator.set_colour(distance)
                    self.indicator.show = True
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
        # Re-draw dirty rects
        for button in self.buttons.values():
            if button.dirty:
                button.draw(background, screen)

    def reset(self):
        self.indicator.reset()

    def unshuffle_bonus(self):
        if not self.image.clue.unshuffled:
            self.image.clue.unshuffle()
            if self.timer.time_bar.width > WARNING_TIME:
                self.timer.remove_time(SHUFFLE_PENALTY)

    def more_letters_bonus(self):
        extra_letters = random.randint(2,4)
        self.image.clue.add_letter(extra_letters)
        if self.timer.time_bar.width > WARNING_TIME:
            self.timer.remove_time(ADD_LETTER_PENALTY)

    def reveal_bonus(self):
        self.image.clue.show_all()
        if self.timer.time_bar.width > WARNING_TIME:
            self.timer.remove_time(REVEAL_PENALTY)
    
class Bonus:
    def __init__(self, bonus_function, counts):
        self.func = bonus_function
        self.counts = counts
        self.original_counts = counts

    def __call__(self):
        if self.counts > 0:
            self.func()
        self.counts = self.counts - 1
        return self.counts

    def reset(self):
        self.counts = self.original_counts

#TODO: Implement cool transition effect
class NextLevel(GameState):
    def __init__(self, gameScreen):
        GameState.__init__(self,gameScreen)
        self.buttons = self.gameScreen.buttons
        self.static_font = pygame.font.Font(
                os.path.join('fonts',TEXT_FONT), 28)
        self.static_text = self.static_font.render(
                'I spy with my little eye, something beginning with:',\
                        1,(221,255,33))
        self.static_text_rect = self.static_text.get_rect()
        self.drawn_once = False

    def enter(self):
        self.gameScreen.level += 1
        self.level_exists = self.gameScreen.set_level(self.gameScreen.level)
        self.image = self.gameScreen.image
        self.delay = 1
        pygame.mouse.set_visible(True)
        self.init_layout()

    def update(self):
        if not self.level_exists:
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
        GameState.eventHandle(self)

    def init_layout(self):
        # Set the image position
        self.image = self.gameScreen.image
        self.image.rect.topleft = (X_OFFSET, Y_OFFSET)
        self.image.mask.rect.topleft = self.image.rect.topleft
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

class GameOver(GameState):
    def __init__(self, gameScreen):
        GameState.__init__(self,gameScreen)
        self.font = pygame.font.Font(os.path.join('fonts',TEXT_FONT), 50)
        self.delay = 200
        self.buttons = gameScreen.buttons

    def enter(self, won):
        self.delay = 200
        if won:
            text = 'You have won!'
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
            self.gameControl.setMode(MAIN_MENU)

    def eventHandle(self):
        # Don't allow escaping to main menu from here.
        #GameState.eventHandle(self)
        pass

    def draw(self, background, screen):
        screen.blit(background, (0,0))
        rect = self.text.get_rect()
        screen_rect = screen.get_rect()
        rect.bottomleft = (screen_rect.width/2 - rect.width/2,screen_rect.height/2-rect.height/2)
        if self.won:
            rect.top += int(100*math.sin(self.delay*2*math.pi/40))
        screen.blit(self.text, rect.bottomleft)

#FIXME: These functions need a proper home
def getLevels(path='levels'):
    levels = [pyspy.utilities.strip_ext(i) \
        for i in os.listdir(path) if i.endswith('xcf')]
    return levels

def checkLevel(level, path='levels'):
    return level+'.png' in os.listdir(path)
    
class GameScreen:
    def __init__(self, gameControlObj, screenRect):
        self.gameControl = gameControlObj
        self.level = 0
        self.indicator = LevelIndicator((screenRect.width, screenRect.height))
        self.images = []
        levels = getLevels()
        if not levels:
            #FIXME: Need to create custom Exception classes
            raise Exception, "No levels found"
        for i in levels:
            if checkLevel(i):
                self.images.append(SpyImage((640,480), i))
            else:
                print "Generating level: %s" %(i)
                pyspy.levels.generateLevel(i)
        self.images = [SpyImage((640,480), i) for i in levels \
                            if checkLevel(i)]
        self.buttons = {'unshuffle': Button('unshuffle'), 
                'more_letters': Button('more_letters'),
                'reveal': Button('reveal'),
                'play': Button('play', callback=self.gameControl.music.unpause_track),
                'pause': Button('pause', callback=self.button_pause),
                'next': Button('next', callback=self.gameControl.music.next_track)}
        self.states = {'NextLevel': NextLevel(self), 'Playing': Playing(self),
            'GameOver': GameOver(self), 'Correct': Correct(self)}

    def button_pause(self):
        if gameControl.music.paused:
            gameControl.music.unpause_track()
        else:
            gameControl.music.pause_track()

    def set_image(self, imageObj):
        self.image = imageObj
        self.image.set_mask(self.level)
    
    def update(self):
        self.state.update()

    def set_level(self, level):
        valid_images = []
        for i in self.images:
            if level in i.levels:
                valid_images.append(i)

        if valid_images:
            self.set_image(valid_images[random.randint(0,len(valid_images)-1)])
        else:
            return False
        return True

    def eventHandle(self):
        self.state.eventHandle()
        return

    def reset(self, type = 0):
        self.level = 0
        for button in self.buttons.values():
            button.reset()
        self.state = self.states['NextLevel']
        self.state.enter()

    def draw(self, background, screen):
        self.state.draw(background, screen)



# Deals with events in the Game

class GameEvent:
    """Event system wrapped so that it is based on time things were pressed.  
            Otherwise repeats occur that we dont desire."""
            
    def __init__(self):
            # Run update to init all the variables
            self.keystate = pygame.key.get_pressed()
            self.keystate = [k for k in self.keystate]
            self.mousestate = pygame.mouse.get_pressed()
            self.mousestate = [b for b in self.mousestate]
            self.mouseMoved = 0
            self.mousePos = (0,0)
            self.update()

    def update(self):
            # See if the user wants to quit
            if pygame.event.peek(12):
                pygame.quit()
                exit(0)
            pygame.event.pump() #keep messages alive

            events = pygame.event.get()
            self.keystate = [False for k in self.keystate]
            self.mousestate = [False for b in self.mousestate]
            for e in events:
                if e.type == KEYUP:
                    #pdb.set_trace()
                    self.keystate[e.key] = True
                if e.type == MOUSEBUTTONUP:
                    if e.button in range(0,3):
                    # Sometimes there are mouse buttons that are outside
                    # this range which mouse.get_pressed() doesn't know about
                    # We only care about left-clicking really...
                        self.mousestate[e.button-1] = True
            
            self.newkeys = self.keystate
            self.mouseButtons = self.mousestate

            pygame.event.clear()

            # Get the mouse data
            self.oldMousePos = self.mousePos
            self.mousePos = pygame.mouse.get_pos()
            if self.oldMousePos == self.mousePos:
                self.mouseMoved = 0
            else:
                self.mouseMoved = 1
            
            
            # Get the time
            self.ticks = pygame.time.get_ticks()

class SoundEffect(pygame.mixer.Sound):
    def __init__(self, path):
        pygame.mixer.Sound.__init__(self, path)

    def play(self):
        if SOUND:
            pygame.mixer.Sound.play(self)

class MusicControl:
    def __init__(self):
        self.music_dir = 'midi'
        self.filenames = self.get_filenames()
        self.filenames = [i for i in self.filenames if i.endswith('.ogg')]
        self.current_track = 0
        self.On = MUSIC
        self.paused = 0

    def get_filenames(self):
        return os.listdir(self.music_dir)

    def play_track(self, randomize = 1):
        if self.On:
            if len(self.filenames)-1 > 0:
                if randomize:
                    self.current_track = random.randint(0, len(self.filenames)-1)
                track = self.filenames[self.current_track]
                #track = 'chpn_op10_e05.ogg'
                pygame.mixer.music.load(os.path.join(self.music_dir,track))
                pygame.mixer.music.play()

    def unpause_track(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = 0

    def pause_track(self):
        pygame.mixer.music.pause()
        self.paused = 1

    def next_track(self, randomize = 1):
        pygame.mixer.music.stop()
        if self.current_track < len(self.filenames)-2 and not randomize:
            self.current_track += 1
        else:
            return 0
        self.play_track(randomize)
        return 1

    def update(self):
        if self.On:
            if not pygame.mixer.music.get_busy():
                self.play_track()
        

class GameControl:
    def __init__(self):
        self.gameEvent = GameEvent()
        self.modeCur = 0
        self.modes = []
        self.players = []
        self.playerCur = 0
        self.music = MusicControl()
        return
		
    def addMode(self, newMode):
        """Insert the new mode into the modes list"""
        self.modes.append(newMode)
        
    def setMode(self, newMode, type = 0):
        """Set the new mode, and reset it"""
        self.modeCur = newMode
        
        # If we didn't set the mode to exit
        if self.modeCur != -1:
            self.modes[self.modeCur].reset(type)		

    def update(self):
        """Update the current mode and events"""
        self.gameEvent.update()
        self.music.update()
        
        if self.modeCur != -1:
            self.modes[self.modeCur].eventHandle()
                
        if self.modeCur != -1:
            self.modes[self.modeCur].update()

    def draw(self, background, screen):
        if self.modeCur != -1:
            self.modes[self.modeCur].draw(background, screen)

def usage():
    usage_string = """
    main.py - Play pySpy!
    Options: -q, --quiet: play pySpy quietly
             -d, --debug: Run in debug mode
             -h, --help: show this usage message
    """
    print usage_string

def main(argv):
    FULL = False
    # Command-line argument handling
    try:
        opts, args = getopt.getopt(argv, "hdqfu",
                ["help","debug","quiet","fullscreen","update"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-q", "--quiet"):
            print "Running in quiet mode"
            global MUSIC, SOUND
            MUSIC = 0
            SOUND = 0
        elif opt in ("-d", "--debug"):
            print "Debug mode"
            global DEBUG
            DEBUG = 1
        elif opt in ("-f", "--fullscreen"):
            print "Running in fullscreen mode"
            FULL = True
        elif opt in ("-u", "--update"):
            print "Checking for updates..."
            updates = pyspy.update.update()
            if not updates:
                print "No updates available"
            sys.exit()

    # Initialise the screen
    pygame.init()
    modes = pygame.display.list_modes()
    #mode = modes[1]
    mode = (1024, 768)
    if FULL:
        screen = pygame.display.set_mode(mode, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(mode)
    pygame.display.set_caption('pySpy')

    background = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    #background.convert_alpha()
    background.fill((255,255,255))
    try:
        bkg_name = 'background_'+str(mode[0])+'x'+str(mode[1])
        bkg_image, bkg_rect = load_png(bkg_name)
    except:
        print "Rescaling default background image"
        bkg_image, bkg_rect = load_png('background')
        bkg_image = pygame.transform.scale(bkg_image, mode)
    background.blit(bkg_image, (0,0))
    logo, logo_rect = load_png('logo')
    logo_rect.right = bkg_rect.right - 20
    logo_rect.top = bkg_rect.top + 20
    background.blit(logo, logo_rect)
    background = background.convert_alpha()
    #background.fill((0,0,160))
    

    bigFont = pygame.font.Font(os.path.join('fonts', TEXT_FONT), 
                                    MENU_SIZE_BIG)
    loadingText = bigFont.render('Loading...', 1, (255,255,255))
    loadingRect = loadingText.get_rect()
    loadingRect.center = screen.get_rect().center

    # Show the background while we're loading, with a loading symbol
    screen.blit(background, (0,0))
    screen.blit(loadingText, loadingRect)
    
    pygame.display.flip()

    clock = pygame.time.Clock()
    random.seed()

    gameControl = GameControl()
    gameControl.addMode(StartScreen(gameControl, screen.get_rect()))
    gameControl.addMode(GameScreen(gameControl, screen.get_rect()))
    gameControl.addMode(InstructionsScreen(gameControl, screen.get_rect()))

    while 1:
        # Lock the framerate
        clock.tick(60)

        # Handle the modes
        gameControl.update()
        gameControl.draw(background, screen)

        # Handle game exit
        if gameControl.modeCur == -1:
            return

        #Flip to front
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__": main(sys.argv[1:])
