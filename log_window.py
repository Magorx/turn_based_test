#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import random
import time


def do_nothing():
    pass


class LogWindow(object):
    def __init__(self, engine, width, height, font=('Comic Sans MS', 12, 'bold')):
        self.engine = engine
        self.width = width
        self.height = height
        self.font = font

        self.active = False
        self.window = None

    def write(self, string, end='\n'):
        self.text.insert(tkinter.END, string + end)

    def activate(self):
        if self.window is not None:
            return
        self.active = True

        window = tkinter.Toplevel()
        window.title('log')
        self.text = tkinter.Text(window, width=self.width, height=self.height,
                                 wrap=tkinter.WORD,
                                 font=self.font)
        window.protocol("WM_DELETE_WINDOW", do_nothing)
        self.text.pack()
        self.x = max(self.engine.world.window_standard_x - window.winfo_reqwidth()*2 - 7, 0) # some magic numbers, TODO
        self.y = self.engine.world.window_standard_y

        status_bar = tkinter.Canvas(window, width=window.winfo_reqwidth()*2 + 2, height=self.engine.world.side_px, bg='green') # idk why width is so wierd, TODO
        button_end_turn = tkinter.Button(status_bar, width=self.engine.world.side_px, height=self.engine.world.side_px, text='End Turn', command=self.engine.end_turn)
        print(self.engine.world.side_px)
        button_end_turn.pack()
        status_bar.pack()

        window.geometry('+{}+{}'.format(self.x, self.y))
        self.window = window

    def deactivate(self, tk_event=None):
        self.active = False
        self.window.destroy()
        self.window = None

    def return_by_index(self, i):
        print('returned ', self.i)
        self.deactivate()
        return self.commands[i]


def main():
    world = tk_worlds.TkWorld(15, 15)
    world.GenerateWorld(lands_to_generate=100, defined_land_square=20)
    world.full_update(to_set_texture_by_symb=True)
    world.root_window.mainloop()


if __name__ == "__main__":
    main()