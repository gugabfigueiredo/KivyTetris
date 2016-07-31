# -*- coding: utf-8 -*-
# kivy/Python modules
from kivy.properties import ObjectProperty, NumericProperty,\
    ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.audio import SoundLoader
import random

#from the internet modules
from tetriscore import SparseGridLayout

# my own modules
from pieces import *


class TetrisManager(ScreenManager):

    def __init__(self, *args, **kwargs):
        super(TetrisManager, self).__init__(*args, **kwargs)
        self.add_widget(MainScreen())

    def start_tetris(self):
        if self.has_screen('tetris'):
            self.remove_widget(self.get_screen('tetris'))
        self.add_widget(TetrisScreen())
        self.current = 'tetris'


class MainScreen(Screen):
    pass


class TetrisScreen(Screen):

    tetris = ObjectProperty()


class Tetris(SparseGridLayout):

    pieces = ListProperty(['I', 'J', 'L', 'O', 'S', 'T', 'Z'])
    next_piece = ObjectProperty(None)
    falling_piece = ObjectProperty(None)
    level = NumericProperty(1.0)
    lines = NumericProperty(0)
    points = NumericProperty(0)
    game_over = BooleanProperty(False)
    brick_wall = ListProperty([[]] * 22)
    sound = SoundLoader.load('tetris.mp3')

    def __init__(self, **kwargs):
        super(Tetris, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.sound.loop = True
        self.sound.play()
        self.set_next()
        self.set_falling()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left' and not self.collide_falling_left():
            self.falling_piece.strifel()
        elif keycode[1] == 'right' and not self.collide_falling_right():
            self.falling_piece.strifer()
        elif keycode[1] == 'up':
            if self.collide_shift():
                return True
            self.falling_piece.shift_right()
        elif keycode[1] == 'down':
            self.drop_falling()
        elif keycode[1] == 'spacebar':
            Clock.schedule_interval(self.drop_falling, .005)
        return True

    def set_falling(self):
        # sets the falling piece
        if self.falling_piece:
            # if falling piece exists, get its bricks
            self.get_bricks()
        self.falling_piece = self.next_piece
        self.falling_piece.row = 19
        self.falling_piece.column = 5
        self.add_widget(self.falling_piece)
        # if piece is started on top of bricks in pile
        # i.e., brick wall reached max height
        if self.collide_on_start():
            self.game_over = True
        else:
            Clock.schedule_interval(self.drop_falling, (1 - (self.level / 100)))
            self.set_next()

    def clear_falling(self):
        # releases falling piece so bricks can be taken
        self.remove_widget(self.falling_piece)
        self.falling_piece.release_bricks()

    def drop_falling(self, *args, **kwargs):
        # moves falling piece down 1 position if no colisions happen
        if self.collide_falling():
            # if colision happens, halts piece, sets new falling
            Clock.unschedule(self.drop_falling)
            self.set_falling()
        else:
            self.falling_piece.fall()

    def collide_falling(self):
        # checks if falling piece has collided with bottom
        # or fallen over any brick on the wall
        for brick in self.falling_piece.bricks:
            pos = brick.pos_hint
            if self.falling_piece.row + pos['y'] <= 0:
                return True
            anchor_pos = self.falling_piece.grid_pos
            fall_pos = [anchor_pos[0] + pos['y'] - 1,
                        anchor_pos[1] + pos['x']]
            if self.brick_wall[fall_pos[0]]:
                if self.brick_wall[fall_pos[0]][fall_pos[1]]:
                    return True

    def collide_falling_right(self):
        # checks if falling piece is touching any piece to its right
        for brick in self.falling_piece.bricks:
            pos = brick.pos_hint
            pos_x = pos['x'] + self.falling_piece.column
            if (pos_x >= 9):
                return True
            anchor_pos = self.falling_piece.grid_pos
            fall_pos = [anchor_pos[0] + pos['y'],
                        anchor_pos[1] + pos['x'] + 1]
            if self.brick_wall[fall_pos[0]]:
                if self.brick_wall[fall_pos[0]][fall_pos[1]]:
                    return True

    def collide_falling_left(self):
        # checks if falling piece is touching any piece to its left
        for brick in self.falling_piece.bricks:
            pos = brick.pos_hint
            pos_x = pos['x'] + self.falling_piece.column
            if (pos_x <= 0):
                return True
            anchor_pos = self.falling_piece.grid_pos
            fall_pos = [anchor_pos[0] + pos['y'],
                        anchor_pos[1] + pos['x'] - 1]
            if self.brick_wall[fall_pos[0]]:
                if self.brick_wall[fall_pos[0]][fall_pos[1]]:
                    return True

    def collide_shift(self):
        # checks if falling piece will collide if shifted
        for brick in self.falling_piece.bricks:
            pos = brick.pos_hint
            anchor_pos = self.falling_piece.grid_pos
            shift_pos = [anchor_pos[0] + pos['x'],
                         anchor_pos[1] + pos['y']]
            if shift_pos[1] < 0 or shift_pos[1] >= 10:
                return True
            if self.brick_wall[shift_pos[0]]:
                if self.brick_wall[shift_pos[0]][shift_pos[1]]:
                    return True

    def set_next(self):
        # generates random next piece to fall
        random_name = self.pieces[random.randint(0, 6)]
        self.next_piece = Piece.factory(random_name)

    def get_bricks(self):
        # take bricks from falling piece and add to the field
        self.clear_falling()
        for brick in self.falling_piece.bricks:
            # set positioning of brick to align to grid
            pos = brick.pos_hint
            brick.row = self.falling_piece.row + pos['y']
            brick.column = self.falling_piece.column + pos['x']
            self.another_brick_in_the_wall(brick)
            self.add_widget(brick)
        # collapses any line in the wall if necessary
        self.collapse_wall()

    def another_brick_in_the_wall(self, brick):
        # adds a brick to the wall
        if not self.brick_wall[brick.grid_pos[0]]:
            self.brick_wall[brick.grid_pos[0]] = [None] * 10
        self.brick_wall[brick.grid_pos[0]][brick.grid_pos[1]] = brick

    def collapse_wall(self, *args, **kwargs):
        # checks if any lines in the wall are full
        lines = 0
        for line in reversed(self.brick_wall):
            if line and None not in line:
                for brick in line:
                    self.remove_widget(brick)
                # remove full lines
                self.brick_wall.remove(line)
                self.brick_wall.append([])
                # update score
                lines = lines + 1
                self.points = self.points + 100 * lines * self.level
            self.lines = self.lines + lines
        # updates positioning of blocks in flield (move unfilled lines down)
        for i, line in enumerate(self.brick_wall):
            for brick in line:
                if hasattr(brick, 'row'):
                    brick.row = i
        pass

    def on_lines(self, *args, **kwargs):
        if self.lines % 5 == 0:
            self.level = self.level + 1

    def collide_on_start(self):
        for brick in self.falling_piece.bricks:
            pos = brick.pos_hint
            anchor_pos = self.falling_piece.grid_pos
            fall_pos = [anchor_pos[0] + pos['y'],
                        anchor_pos[1] + pos['x']]
            if self.brick_wall[fall_pos[0]]:
                if self.brick_wall[fall_pos[0]][fall_pos[1]]:
                    return True