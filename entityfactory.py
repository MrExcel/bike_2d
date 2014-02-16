#!/usr/bin/env python2

from entity import *
from math import radians

class EntityFactory(object):
    def __init__(self, entityList, evtMngr):
        self.target = entityList
        self.evtMngr = evtMngr
    
    def CreatePlayer(self, x=0, y=0, w=10, h=10):
        e = Entity(self.target)
        e.type = PLAYER
        e.addComp(Input(self.evtMngr))
        fw = self.CreateWheel(x - 50, y)
        bw = self.CreateWheel(x + 50, y)
        e.addComp(Spring(fw, bw))
        e.addComp(Chassis(fw, bw))
        return e

    def CreateLevelBlock(self,x=0, y=0, width=10, heigth=10, angle=0):
        e = self.CreateBox(x, y, width, heigth, angle)
        e.type = LEVEL_BLOCK
        return e

    def CreateWheel(self, x=0, y=0, r=20):
        e = self.CreateCircle(x, y, r)
        e.type = WHEEL
        e.addComp(Velocity())
        e.addComp(Gravity())
        e.addComp(Contacts())
        e.addComp(Engine())
        e.addComp(Breaks())
        e.physprops.mass = 7
        e.physprops.grip = 1
        e.physprops.rotFriction = .01
        e.physprops.restitution = .4
        e.updateFirst = ['velocity', 'engine', 'breaks']
        e.updateLast = ['contacts']
        return e

    def CreateCircle(self,x=0, y=0, r=10):
        e = Entity(self.target)
        e.type = CIRCLE
        e.addComp(PhysicalProperties())
        e.addComp(Position(x, y))
        e.addComp(CircleModel(e.position, r))
        e.addComp(CircleHitbox(r))
        return e

    def CreateBox(self,x=0, y=0, width=10, heigth=10, angle=0):
        e = Entity(self.target)
        e.type = BOX
        e.addComp(PhysicalProperties())
        e.addComp(Position(x, y, radians(angle)))
        e.addComp(BoxModel(e.position, width, heigth))
        e.addComp(Hitbox(width, heigth))
        return e

    def CreateFPSMeter(self, x=10, y=0, fontSize=32):
        e = Entity(self.target)
        e.type = HUD_ELEM
        e.addComp(FPSCounter())
        e.addComp(
            FPSModel(self.evtMngr, Position(x, y), e.fpscounter, fontSize)
            )
        return e

    def CreateParameterMonitor(self, fn, x=10, y=550, fontSize=32):
        e = Entity(self.target)
        e.type = HUD_ELEM
        e.addComp(TextModel(self.evtMngr, Position(x, y), fontSize, fn))
        return e
