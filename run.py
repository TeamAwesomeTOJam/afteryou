#! /bin/env python

import os, sys
import game
import mode


g = game.Game((1280, 720), os.path.join(sys.path[0], 'res'))
g.run(mode.PlayMode())