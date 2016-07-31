# -*- coding: utf-8 -*-

# kivy/Python modules
from kivy.app import App
from kivy.lang import Builder

#my own modules
from tetris import *

Builder.load_string("""
<MainScreen>:
    name: 'main'
    Button:
        size_hint: None, .10
        width: self.height * 2
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: root.manager.start_tetris()
        text: 'Start'

<TetrisScreen>:
    name: 'tetris'
    tetris: tetris
    canvas.before:
        Color:
            rgba: .2, .2, .2, .5 # your color here
        Rectangle:
            size: root.size
    Tetris:
        id: tetris
        shape: 20, 10
        size_hint: .40, 1
        pos_hint: {'x': .10, 'y': 0}
        on_game_over: root.manager.current = 'main'
    Label:
        id: points
        size_hint: .20, .10
        pos_hint: {'top': .97, 'right': .97}
        canvas.before:
            Color:
                rgba: .0, .0, .0, .5 # your color here
            Rectangle:
                size: root.size
        text: 'score: ' + str(tetris.points)

<Tetris>:
    canvas.before:
        Color:
            rgba: .0, .0, .0, .5 # your color here
        Rectangle:
            size: root.size

<Brick>:
    source: 'block.png'

<Piece>:
    row: 19
    column: 5
    brick_0: brick_0
    Brick:
        id: brick_0
        pos_hint: {'x': 0, 'y': 0}
        color: root.color

<IPiece>:
    color: .5, .5, .5, 1
    brick_a: brick_a
    brick_b: brick_b
    brick_c: brick_c
    Brick:
        id: brick_a
        pos_hint: {'x': -1, 'y': 0}
        color: root.color
    Brick:
        id: brick_b
        pos_hint: {'x': 1, 'y': 0}
        color: root.color
    Brick:
        id: brick_c
        pos_hint: {'x': 2, 'y': 0}
        color: root.color

<LPiece>:
    color: .5, .5, 1, 1
    brick_a: brick_a
    brick_b: brick_b
    brick_c: brick_c
    Brick:
        id: brick_a
        pos_hint: {'x': -1, 'y': 0}
        color: root.color
    Brick:
        id: brick_b
        pos_hint: {'x': 1, 'y': 0}
        color: root.color
    Brick:
        id: brick_c
        pos_hint: {'x': -1, 'y': -1}
        color: root.color

<JPiece>:
    color: .5, 1, .5, 1
    brick_a: brick_a
    brick_b: brick_b
    brick_c: brick_c
    Brick:
        id: brick_a
        pos_hint: {'x': -1, 'y': 0}
        color: root.color
    Brick:
        id: brick_b
        pos_hint: {'x': 1, 'y': 0}
        color: root.color
    Brick:
        id: brick_c
        pos_hint: {'x': 1, 'y': -1}
        color: root.color

<TPiece>:
    color: .5, 1, 1, 1
    brick_a: brick_a
    brick_b: brick_b
    brick_c: brick_c
    Brick:
        id: brick_a
        pos_hint: {'x': -1, 'y': 0}
        color: root.color
    Brick:
        id: brick_b
        pos_hint: {'x': 1, 'y': 0}
        color: root.color
    Brick:
        id: brick_c
        pos_hint: {'x': 0, 'y': -1}
        color: root.color

<SPiece>:
    color: 1, .5, .5, 1
    brick_a: brick_a
    brick_b: brick_b
    brick_c: brick_c
    Brick:
        id: brick_a
        pos_hint: {'x': 1, 'y': 0}
        color: root.color
    Brick:
        id: brick_b
        pos_hint: {'x': 0, 'y': -1}
        color: root.color
    Brick:
        id: brick_c
        pos_hint: {'x': -1, 'y': -1}
        color: root.color

<ZPiece>:
    color: 1, .5, 1, 1
    brick_a: brick_a
    brick_b: brick_b
    brick_c: brick_c
    Brick:
        id: brick_a
        pos_hint: {'x': -1, 'y': 0}
        color: root.color
    Brick:
        id: brick_b
        pos_hint: {'x': 0, 'y': -1}
        color: root.color
    Brick:
        id: brick_c
        pos_hint: {'x': 1, 'y': -1}
        color: root.color

<OPiece>:
    color: 1, 1, .5, 1
    brick_a: brick_a
    brick_b: brick_b
    brick_c: brick_c
    Brick:
        id: brick_a
        pos_hint: {'x': -1, 'y': 0}
        color: root.color
    Brick:
        id: brick_b
        pos_hint: {'x': 0, 'y': -1}
        color: root.color
    Brick:
        id: brick_c
        pos_hint: {'x': -1, 'y': -1}
        color: root.color

""")


class MyApp(App):

    def build(self):
        return TetrisManager()


if __name__ == '__main__':
    MyApp().run()