#! /bin/env python

import os, sys
sys.path.append('src')

import game
import mode


g = game.Game((1280, 720), os.path.join(sys.path[0], 'res'))
g.run(mode.PlayMode())
