#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import game_engine


def main():
    engine = game_engine.GameEngine()
    engine.LoadWorld(20, 10, 'world')
    engine.add_player('DeLich', 0)
    engine.add_player('DeGodz', 1)
    engine.StartWorld()


if __name__ == '__main__':
    main()