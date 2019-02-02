#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import random
import time


class InfoWindow(object):
    def __init__(self, world, choices, commands, args, imgs=[], button_height=2, button_width=10):
        if len(choices) != len(commands) or len(choices) < 1:
            raise IndexError
        if imgs and len(imgs) != len(choice):
            raise IndexError

        self.world = world

        self.choices = ['Cancel'] + choices
        self.commands = [self.die] + commands
        self.args = [[]] + args
        self.imgs = [None] + imgs
        self.side_px = world.side_px
        self.button_height = button_height
        self.button_width = button_width
        self.window = None
        self.to_return = None

        self.active = False

    def check_xy(self, x, y):
        if x < 0 or y < 0 or x > self.world.root_window.winfo_width() or y > self.world.root_window.winfo_height():
            return False
        else:
            return True

    def die(self, event):
        self.deactivate()

    def activate(self, init_x, init_y):
        if self.window is not None:
            return 0
        self.active = True

        window = tkinter.Canvas(self.world.root_window)
        side_px = self.side_px
        window_width = 0
        window_height = 0

        for i in range(len(self.choices)):
            canvas = tkinter.Canvas(window, width=side_px, height=side_px)
            if len(self.imgs) > 1:
                canvas.create_image(i * side_px, i * side_px, image=self.imgs[i])
            button = tkinter.Button(canvas, 
                                    text=str(self.choices[i]),
                                    command=lambda i=i: self.commands[i](self.args[i]), # kostili v dele, inache nikak
                                    width=self.button_width, height=self.button_height)
            button.pack()
            canvas.pack()
            window_width = max(window_width, canvas.winfo_reqwidth())
            window_height += canvas.winfo_reqheight()
        self.window = window

        x = (init_x + 1) * self.world.side_px
        y = (init_y + 1) * self.world.side_px
        anchor = tkinter.NW
        print(1)

        if not self.check_xy(x + window_width, y + window_height):
            x = init_x * self.world.side_px
            y = init_y * self.world.side_px
            anchor = tkinter.SE
            if not self.check_xy(x - window_width, y - window_height):
                x = init_x * self.world.side_px
                y = (init_y + 1) * self.world.side_px
                anchor = tkinter.NE
                if not self.check_xy(x - window_width, y + window_height):
                    x = (init_x + 1) * self.world.side_px
                    y = init_y * self.world.side_px
                    anchor = tkinter.SW

        self.window.place(x=x, y=y, anchor=anchor)

    def deactivate(self, tk_event=None):
        self.active = False
        self.window.destroy()
        self.window = None

    def return_by_index(self, i):
        print('returned ', self.i)
        self.deactivate()
        return self.commands[i]


def main():
    pass


if __name__ == "__main__":
    main()