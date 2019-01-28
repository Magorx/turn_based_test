#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import tk_world
import textures
import info_window
import unit
import event

LANDSHAFT_PASSABILITY = {'!' : 0, '.' : 1, 'T' : 2, '^' : 3, '~' : -1}

class GameWorldTyle(tk_world.TkWorldTyle):
    def __init__(self, world, canvas, x=0, y=0, symb='.'):
        super(GameWorldTyle, self).__init__(world, canvas, x, y, symb=symb)
        self.coating_func = None
        self.points_left = 0 # here we store how many points (of movement, for example) left. [for last action of any type]
        self.a_value = 0 # here we store some number, that has to be stored by outer funcs (spawning unit index)

    def clicked(self, tk_event):
        self.world.clicked(event.Event(tk_event, event.TYLE_CLICKED, tyle=self))

    def update(self, **kwargs):
        super(GameWorldTyle, self).update(kwargs)
        self.passability = LANDSHAFT_PASSABILITY[self.symb]

    def is_full(self):
        if self.creature or self.building:
            return True
        else:
            return False

    def get_team(self):
        obj = self.get_intaractable()
        if obj:
            return obj.team
        else:
            return -1
    
    def get_intaractable(self):
        if self.creature:
            return self.creature
        elif self.building:
            return self.building
        else:
            return None

class GameWorld(tk_world.TkWorld):
    def __init__(self,
                 engine,
                 width, height, 
                 tyle_type=GameWorldTyle,
                 side_px=tk_world.SIDE_PX,
                 pre_generated=False,
                 window=None,
                 textures=None):
        super(GameWorld, self).__init__(width, height, 
                                        tyle_type,
                                        None,
                                        side_px,
                                        pre_generated,
                                        window,
                                        textures)
        self.engine = engine

    def clicked(self, event):
        self.engine.click_handler(event)

    def check_coords(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return  False
        else:
            return True

    def update(self):
        super(GameWorld, self).full_update()
        for x in range(self.width):
            for y in range(self.height):
                self.map[x][y].update()
    
    def to_log(self, string):
        self.engine.to_log(string)


def main():
    world = GameWorld(10, 10, pre_generated=True)
    world.root_window.mainloop()


if __name__ == '__main__':
    main()