#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import game_world
import unit
import atributes
import textures
import event as ev
import player


STANDART_LANDSHAFTS = ['.', '~', '^', 'T']


class GameEngine():
    def __init__(self):
        self.world = None

        self.cur_creature_selected = None
        self.cur_building_selected = None
        self.cur_landshaft_selected = None

        self.players = []
        self.current_player = None
        self.current_player_index = 0

    def CreateWorld(self,
                  width, height,
                  tyle_type=game_world.GameWorldTyle,
                  side_px=game_world.tk_world.SIDE_PX,
                  landshafts=STANDART_LANDSHAFTS,
                  window=None,
                  textures=None):
        self.world = game_world.GameWorld(self, width, height, 
                                      tyle_type,
                                      side_px,
                                      False,
                                      window,
                                      textures)
        self.world.landshafts = landshafts

    def GenerateWorld(self,
                      lands_to_generate=100, 
                      defined_land_square = 0,
                      landshafts=None,
                      to_update=False, delay_between_updates=0):
        if landshafts is None:
            landshafts = self.world.landshafts
        self.world.GenerateWorld(lands_to_generate, 
                                 defined_land_square,
                                 landshafts,
                                 to_update, delay_between_updates)

    def StartWorld(self):
        self.world.update()
        self.world.root_window.mainloop()

    def SaveWorld(self, file_name):
        self.world.SaveTheWorld(file_name)
        self.world.update()

    def LoadWorld(self, width, height, file_name):
        if self.world is None:
            self.CreateWorld(width, height)

        self.world.LoadTheWorld(file_name)
        self.world.update()

    def add_player(self, name, flag_index):
        self.players.append(player.Player(self.world, name, flag_index))
        if self.current_player is None:
            self.current_player = self.players[0]

    def end_turn(self):
        self.current_player.update(end_of_turn=True)
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_player = self.players[self.current_player_index]
        print('End of Turn. Now player is:', self.current_player.name)

    def cancel_selection(self):
        creature = self.cur_creature_selected
        building = self.cur_building_selected
        landshaft = self.cur_landshaft_selected
        if creature:
            creature.cancel_selection()
            self.cur_creature_selected = None
        if building:
            building.cancel_selection()
            self.cur_building_selected = None
        if building:
            landshaft.cancel_selection()
            self.cur_landshaft_selected = None


    def click_handler(self, event):
        if event.type == ev.TYLE_CLICKED:
            tyle = event.tyle
            if tyle.coating_func:
                tyle.coating_func(tyle)
                return

            self.cancel_selection()

            if tyle.creature:
                event.creature = tyle.creature
                event.type = ev.CREATURE_CLICKED
                self.click_handler(event)
            elif tyle.building:
                event.building = tyle.building
                event.type = ev.BUILDING_CLICKED
                self.click_handler(event)
            elif tyle.landshaft:
                event.landshaft = tyle.landshaft
                event.type = ev.LANDSHAFT_CLICKED
                self.click_handler(event)
            else:
                # testing unit
                atrs = atributes.Atributes(10, 5, 5, 0, 0, 1)
                unit.spawn_unit(self.world, tyle.x, tyle.y, unit.TYPE_BUILDING, 'cr', '@', atrs, -1, self.current_player, textures.castle, self.current_player.flag)

        elif event.type == ev.CREATURE_CLICKED:
            if self.cur_creature_selected:
                cr = self.cur_creature_selected
                cr.close_selection()
                self.cur_creature_selected = None
            else:
                cr = event.creature
                if cr.owner != self.current_player:
                    return
                else:
                    self.cur_creature_selected = cr
                    cr.clicked(event)


def main():
    world = game_world.GameWorld(10, 10, pre_generated=True)
    world.root_window.mainloop()


if __name__ == '__main__':
    main()