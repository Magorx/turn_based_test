#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import game_world
import unit
import atributes
import textures
import event as ev
import player
import log_window


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

    def to_log(self, string):
        self.log.write(string)

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

        self.log = log_window.LogWindow(self.world, 40, 20)
        self.log.activate()

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
        self.to_log('Epoch of epicness begins!')
        self.to_log('Lord {}, your turn.'.format(self.current_player))
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

    def end_turn(self, *trash):
        self.to_log("End of {}'s turn".format(self.current_player))
        for pl in self.players:
            pl.update(end_of_turn=True)
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_player = self.players[self.current_player_index]
        self.to_log("Lord {}, your turn.".format(self.current_player))

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
        if landshaft:
            landshaft.cancel_selection()
            self.cur_landshaft_selected = None

    def update_players(self):
        for player in self.players:
            player.update()

    def click_handler(self, event):
        self.update_players()
        if event.type == ev.TYLE_CLICKED:
            tyle = event.tyle
            if tyle.coating_func:
                tyle.coating_func(tyle)
                self.update_players()
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
                #testing unit
                # atrs = atributes.Atributes(10, 5, 5, 0, 0, 4, 3)
                # cr = unit.Creature(self.world, tyle.x, tyle.y, unit.TYPE_BUILDING, 'cr', '@', atrs, self.current_player_index, self.current_player, textures.footman, self.current_player.flag)
                # unit.spawn_cr(cr, self.current_player)

                #testing buildings
                atrs1 = atributes.Atributes(10, 5, 5, 1, 0, 0, 4, 4)
                atrs2 = atributes.Atributes(15, 7, 6, 2, 0, 0, 2, 6)
                cr1 = unit.Creature(self.world, tyle.x, tyle.y, unit.TYPE_CREATURE, 'Rider', '@', atrs1, self.current_player_index, self.current_player, textures.horseman, self.current_player.flag)
                cr2 = unit.Creature(self.world, tyle.x, tyle.y, unit.TYPE_CREATURE, 'Knight', '@', atrs2, self.current_player_index, self.current_player, textures.footman, self.current_player.flag)
                crs = [cr1, cr2]
                bld = unit.Building(self.world, tyle.x, tyle.y, unit.TYPE_BUILDING, 'cr', '@', atrs1, self.current_player_index, self.current_player, textures.castle, self.current_player.flag,
                                    produced_units=crs, spawn_points=10)
                unit.spawn_bld(bld, self.current_player)

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
        elif  event.type == ev.BUILDING_CLICKED:
            if self.cur_building_selected:
                bld = self.cur_building_selected
                bld.close_selection()
                self.cur_building_selected = None
            else:
                bld = event.building
                if bld.owner != self.current_player:
                    return
                else:
                    self.cur_building_selected = bld
                    bld.clicked(event)
        self.update_players()


def main():
    world = game_world.GameWorld(10, 10, pre_generated=True)
    world.root_window.mainloop()


if __name__ == '__main__':
    main()