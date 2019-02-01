#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PIL import Image, ImageTk


def load_texture(path):
    return ImageTk.PhotoImage(Image.open(path))


def load_texture_by_name(name):
    return load_texture('./textures/' + name + '.png')


grass =  load_texture_by_name('grass')
water =  load_texture_by_name('water')
mountains =  load_texture_by_name('mountains')
tree =  load_texture_by_name('tree')

swordman =  load_texture_by_name('swordman')
horseman =  load_texture_by_name('horseman')

building_plan = load_texture_by_name('building_plan')
castle =  load_texture_by_name('castle')

transparent =  load_texture_by_name('transparent')

chosen_corner = load_texture_by_name('chosen_corner_red')
chosen_corner_red =  load_texture_by_name('chosen_corner_red')
chosen_corner_blue =  load_texture_by_name('chosen_corner_blue')
chosen_corner_green =  load_texture_by_name('chosen_corner_green')
chosen_corner_golden =  load_texture_by_name('chosen_corner_golden')
chosen_corner_brown =  load_texture_by_name('chosen_corner_brown')

error = load_texture_by_name('error')

TEXTURES = {
    'grass' : grass,
    'water' : water,
    'mountains' : mountains,
    'tree' : tree,
    'swordman' : swordman,
    'transparent' : transparent,
    'chosen_corner_red' : chosen_corner_red,
    'chosen_corner_blue' : chosen_corner_blue,
    'chosen_corner_green' : chosen_corner_green,
    'chosen_corner_golden' : chosen_corner_golden,
    'chosen_corner_brown' : chosen_corner_brown
}

CORNERS_TEXTURES = {
    'chosen_corner_red' : TEXTURES['chosen_corner_red'],
    'chosen_corner_blue' : TEXTURES['chosen_corner_blue'],
    'chosen_corner_green' : TEXTURES['chosen_corner_green'],
    'chosen_corner_golden' : TEXTURES['chosen_corner_golden'],
    'chosen_corner_brown' : TEXTURES['chosen_corner_brown']
}

FLAGS = [load_texture_by_name('flag1'),
         load_texture_by_name('flag2')]