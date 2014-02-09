#!/usr/bin/env python2

from sdl2 import timer

class View(object):
    def __init__(self, game):
        self.game = game
        self.time = timer.SDL_GetTicks()
        self.viewObjects = []

    def update(self, dt=None):
        if not dt: dt = self.getDt()

        for o in self.viewObjects:
            o.update(dt)

    def getDt(self):
        newTime = timer.SDL_GetTicks()
        dt = newTime - self.time
        self.time = newTime
        return dt