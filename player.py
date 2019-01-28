#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import textures


class Player():
    def __init__(self, world, name, flag_index, action_points=2):
        self.world = world
        self.name = name
        self.flag = textures.FLAGS[flag_index]

        self.creatures = []
        self.buildings = []

        self.action_points = action_points
        self.cur_action_points = action_points

    def add_creature(self, creature):
        self.creatures.append(creature)

    def add_building(self, building):
        self.buildings.append(building)

    def del_creature(self, creature):
        for i in range(len(creatures)):
            if creatures[i] == creature:
                del creature[i]

    def update(self, end_of_turn=False):
        if end_of_turn:
            self.cur_action_points = self.action_points

        self.update_creatures(end_of_turn=end_of_turn)
        self.update_buildings(end_of_turn=end_of_turn)

    def update_creatures(self, end_of_turn=False):
        for cr in self.creatures:
            cr.update(end_of_turn=end_of_turn)

    def update_buildings(self, end_of_turn=False):
        for bld in self.buildings:
            bld.update(end_of_turn=end_of_turn)

    def __repr__(self):
        return self.name