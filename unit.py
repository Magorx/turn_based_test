#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import atributes as atrs
import info_window
import textures

from collections import deque
import copy


TYPE_CREATURE = 101
TYPE_BUILDING = 102


STANDART_MOVE_MAP = [[0, 1], [1, 0], [-1, 0], [0, -1]]


class Unit():
    def __init__(self, world, x, y, 
                 type, name, char, atributes,
                 team=-1, owner=None, 
                 texture=None, flag=None, 
                 move_map=None):
        self.world = world
        self.x = x
        self.y = y
        self.type = type
        self.name = name
        self.char = char
        self.atributes = atributes
        self.team = team
        self.owner = owner
        self.texture = texture
        self.flag = flag

        if move_map is None:
            move_map = STANDART_MOVE_MAP
        self.move_map = move_map

        self.visible = True
        self.info_window = None

        self.last_filling_distance = 0
        self.move_points = self.atributes.speed

    def copy(self):
        unit = type(self)(self.world, self.x, self.y, 
                    self.type, self.name, self.char, self.atributes,
                    self.team, self.owner, 
                    self.texture, self.flag, 
                    self.move_map)
        for key in self.__dict__:
            unit.__dict__[key] = self.__dict__[key]

        return unit

    def delete(self, *trash):
        tyle = self.world.map[self.x][self.y]
        tyle.delete_texture_by_name(self.name + '_texture')
        tyle.delete_texture_by_name(self.name + '_flag')

        if self.type == TYPE_CREATURE:
            tyle.creature = None
        elif self.type == TYPE_BUILDING:
            tyle.building = None

        self.close_filling_module(self.last_filling_distance)

    def draw(self):
        self.world.map[self.x][self.y].add_texture(self.texture, self.name + '_texture')
        self.world.map[self.x][self.y].add_texture(self.flag, self.name + '_flag')

    def fill_zone_bfs(self, distance, 
                      coating_func, coating_value=-1,
                      init_x=None, init_y=None,
                      moveable_only=False, flying=False,
                      texture=None):
        if init_x is None or init_y is None:
            self.last_filling_distance = distance
            init_x = self.x
            init_y = self.y

        tyle = self.world.map[init_x][init_y]
        if moveable_only and not flying:
            distance += tyle.passability
        else:
            distance += 1

        q = deque()
        q.append([init_x, init_y, distance])
        while q:
            cur_x, cur_y, dist = q.popleft()
            if not self.world.check_coords(cur_x, cur_y):
                continue
            tyle = self.world.map[cur_x][cur_y]

            new_dist = dist
            if moveable_only and not flying:
                if tyle.is_full():
                    team = tyle.get_team()
                    if (self.team == -1 and team != -1) or (self.team != team and team != -1):
                        continue
                new_dist -= tyle.passability
            else:
                new_dist -= 1
            if new_dist < 0:
                continue

            if tyle.coating_func:
                continue
            if moveable_only and tyle.passability == -1:
                continue

            if not (moveable_only and tyle.is_full()):
                tyle.coating_func = coating_func
                tyle.a_value = coating_value
                tyle.points_left = new_dist
                if texture:
                    tyle.add_texture(texture, texture_name=str(self) + '_filled')

            for shift in self.move_map:
                new_x = cur_x + shift[0]
                new_y = cur_y + shift[1]
                q.append([new_x, new_y, new_dist])

    def close_filling_bfs(self, distance=0, 
                          cur_x=None, cur_y=None,
                          moveable_only=False,
                          texture_used=True):
        if cur_x is None or cur_y is None:
            cur_x = self.x
            cur_y = self.y
            distance = self.last_filling_distance
            self.last_filling_distance = 0
        if not self.world.check_coords(cur_x, cur_y):
            return
        tyle = self.world.map[cur_x][cur_y]
        if distance < 0:
            return
        if moveable_only and not tyle.moveable:
            return

        tyle.coating_func = None
        if texture_used:
            tyle.delete_texture_by_name(str(self) + '_filled')

        new_distance = distance
        if moveable_only:
            new_distance -= tyle.passability
        else:
            new_distance -= 1

        for shift in self.move_map:
            new_x = cur_x + shift[0]
            new_y = cur_y + shift[1]
            if self.world.check_coords(new_x, new_y):
                self.close_filling_bfs(new_distance, new_x, new_y, moveable_only)

    def fill_zone_module(self, distance, 
                         coating_func, coating_value=-1,
                         init_x=None, init_y=None,
                         moveable_only=False, flying=False,
                         texture=None):
        if init_x is None or init_y is None:
            self.last_filling_distance = distance
            init_x = self.x
            init_y = self.y

        for cur_x in range(init_x - distance, init_x + distance + 1):
            for cur_y in range(init_y - distance, init_y + distance + 1):
                if not self.world.check_coords(cur_x, cur_y):
                    continue
                else:
                    tyle = self.world.map[cur_x][cur_y]
                    if not (moveable_only and tyle.is_full()):
                        tyle.coating_func = coating_func
                        tyle.a_value = coating_value
                        if texture:
                            tyle.add_texture(texture, texture_name=str(self) + '_filled')

    def close_filling_module(self, distance=0, 
                             init_x=None, init_y=None, texture_used=True):
        if init_x is None or init_y is None or distance == 0:
            distance = self.last_filling_distance
            init_x = self.x
            init_y = self.y
            self.last_filling_distance = 0

        for cur_x in range(init_x - distance, init_x + distance + 1):
            for cur_y in range(init_y - distance, init_y + distance + 1):
                if not self.world.check_coords(cur_x, cur_y):
                    continue
                else:
                    tyle = self.world.map[cur_x][cur_y]
                    tyle.coating_func = None
                    if texture_used:
                        tyle.delete_texture_by_name(str(self) + '_filled')

    def cancel_selection(self):
        self.close_filling_module()
        if self.info_window:
            self.info_window.deactivate()
            self.info_window = None

    def update(self, end_of_turn=False):
        if end_of_turn:
            self.move_points = self.atributes.speed
            self.spawn_points

    def clicked(self, event):
        pass # make your own


class Creature(Unit):
    def prepare_move(self, *trash):
        self.fill_zone_bfs(self.move_points, self.move, moveable_only=True, texture=textures.chosen_corner_blue)

    def move(self, tyle):
        if tyle.creature:
            return
        else:
            self.delete()
            self.x = tyle.x
            self.y = tyle.y
            tyle.creature = self
            self.move_points = tyle.points_left
            self.draw()
    
    def clicked(self, event):
        if event.tk_event.num == 1:
            self.prepare_move()
        else:
            if self.info_window:
                if self.info_window.active:
                    return

            buttons = ['Delete', 'Move', 'End Turn']
            commands = [self.delete, self.prepare_move, self.owner.world.engine.end_turn]
            self.info_window = info_window.InfoWindow(buttons, commands, [None for i in range(3)])
            self.info_window.activate()   


class Building(Unit):
    def __init__(self, world, x, y, 
                 type, name, char, atributes, 
                 team=-1, owner=None, 
                 texture=None, flag=None, 
                 move_map=None,
                 produced_units=None, spawn_points=0, spawn_distance=1,
                 produced_resourses=None):
        super(Building, self).__init__(world, x, y,
                                       type, name, char, atributes,
                                       team, owner,
                                       texture, flag,
                                       move_map)
        self.produced_units = produced_units
        self.produced_resourses = produced_resourses
        self.spawn_points = spawn_points

    def prepare_spawn(self, unit_index):
        self.fill_zone_module(1, self.spawn_creature, coating_value=unit_index, 
                       moveable_only=True, flying=True,
                       texture=textures.chosen_corner_golden)

    def spawn_creature(self, tyle):
        cr_index = tyle.a_value
        cr = self.produced_units[cr_index].copy()
        self.close_filling_module()

        if cr.atributes.cost > self.spawn_points:
            return
        else:
            cr.x = tyle.x
            cr.y = tyle.y
            spawn_cr(cr, self.owner)
            self.spawn_points -= cr.atributes.cost

    def clicked(self, event):
        if event.tk_event.num == 1:
            self.prepare_spawn(0)
        else:
            if self.info_window:
                if self.info_window.active:
                    return

            buttons = ['Delete']
            commands = [self.delete]
            args = [[]]
            for i in range(len(self.produced_units)):
                buttons.append('Spawn ' + self.produced_units[i].name)
                commands.append(self.prepare_spawn)
                args.append(i)
            self.info_window = info_window.InfoWindow(buttons, commands, args)
            self.info_window.activate()

def spawn_creture(world, x, y, name, char, atributes, team, owner, texture, flag):
    unit = Creature(world, x, y, TYPE_CREATURE, name, char, atributes, team, owner, texture, flag, STANDART_MOVE_MAP)
    owner.creatures.append(unit)
    tyle = unit.world.map[x][y]
    tyle.creature = unit
    unit.draw()


def spawn_cr(cr, owner, world=None):
    if world:
        cr.world = world

    owner.add_creature(cr)
    tyle = cr.world.map[cr.x][cr.y]
    tyle.creature = cr
    cr.draw()


def spawn_bld(bld, owner):
    if not owner.cur_action_points:
        return
    else:
        owner.cur_action_points -= 1

    owner.add_building(bld)
    tyle = bld.world.map[bld.x][bld.y]
    tyle.building = bld
    bld.draw()