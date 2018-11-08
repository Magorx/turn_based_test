#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import textures


class Player():
    def __init__(self, world, name, flag_index):
        self.world = world
        self.name = name
        self.flag = textures.FLAGS[flag_index]

        self.creatures = []
        self.buildings = []

    def add_creature(self, creature):
        self.creatures.append(creature)

    def del_creature(self, creature):
        for i in range(len(creatures)):
            if creatures[i] == creature:
                del creature[i]

    def update(self, end_of_turn=False):
        self.update_creatures(end_of_turn=end_of_turn)

    def update_creatures(self, end_of_turn=False):
        for cr in self.creatures:
            cr.update(end_of_turn=end_of_turn)
