#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import random
import time


class LogWindow(object):
    def __init__(self, world, width, height, font=('Comic Sans MS', 12, 'bold')):
        self.world = world
        self.width = width
        self.height = height
        self.font = font

        self.active = False
        self.window = None

    def write(self, string, end='\n'):
        self.text.insert(tkinter.END, string + end)

    def activate(self):
        if self.window is not None:
            return 0
        self.active = True

        window = tkinter.Toplevel()
        window.title('log')
        self.text = tkinter.Text(window, width=self.width, height=self.height,
                                 wrap=tkinter.WORD,
                                 font=self.font)
        self.text.pack()
        self.x = max(self.world.window_standard_x - 420, 0)
        self.y = self.world.window_standard_y
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