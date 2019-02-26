#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
hp - hp
mp - mp
These atrs were making sence to me one day
Attack - clear damage output, without any buffs
Defence - clear damage reduction, without any buffs
Hardness - damage cutting after using all bonuses
Speed - you have [speed] move points (XD)
'''


class Atributes():
    def __init__(self, hp, mp, attack, attack_range, defence, hardness, speed, cost):
        self.hp = hp
        self.mp = mp
        self.attack = attack
        self.attack_range = attack_range
        self.defence = defence
        self.hardness = hardness
        self.speed = speed
        self.cost = cost

    def copy(self):
        atrs = type(self)(self.hp,
                          self.mp,
                          self.attack,
                          self.attack_range,
                          self.defence,
                          self.hardness,
                          self.speed,
                          self.cost)

        for key in self.__dict__:
            atrs.__dict__[key] = self.__dict__[key]

        return atrs
