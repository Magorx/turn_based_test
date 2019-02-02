#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import game_engine


def main():
    engine = game_engine.GameEngine()
    engine.LoadWorld(10, 10, 'world')
    engine.add_player('Shaitan', 0)
    engine.add_player('Quarzon', 1)
    engine.StartWorld()


if __name__ == '__main__':
    main()