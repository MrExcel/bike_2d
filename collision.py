#!/usr/bin/env python2

from copy import deepcopy

from math import sqrt
from vec2d import Vec2d
from basecomponent import *

__all__ = ['CollisionResolver']

def collides(this, other):
    try: bound = this.hitbox.getBoundingPoly(this)
    except (KeyError, AttributeError): pass
    try: bound = this.hitbox.getBoundingBox(this)
    except (KeyError, AttributeError): pass
    try: bound = this.hitbox.getBoundingCircle(this)
    except (KeyError, AttributeError): return False
    return bound.intersects(other)

class Bounds(object):
    def intersects(self, other):
        try: ohb = other.hitbox
        except KeyError: return False
        try: return self.intersectsPoly(ohb.getBoundingPoly(other))
        except AttributeError: pass
        try: return self.intersectsCirc(ohb.getBoundingCircle(other))
        except AttributeError: return False

class BoundingBox(Bounds):
    def __init__(self, x, y, w, h):
        self.pos = Vec2d(x, y)
        self.dim = Vec2d(w, h)

    def __getitem__(self, key):
        key = key % 4
        if key  == 0:
            return self.pos
        elif key == 1:
            return self.pos + Vec2d(0, self.dim.y)
        elif key == 2:
            return self.pos + self.dim
        else:
            return self.pos + Vec2d(self.dim.x, 0)

    def intersectsBB(self, other):
        minResVec = Vec2d(0, 0)
        if self.pos.x > other.pos.x + other.dim.x: 
            minResVec += Vec2d(self.pos.x - other.pos.x + other.dim.x, 0)
        if self.pos.y > other.pos.y + other.dim.y:
            minResVec += Vec2d(0, self.pos.y - other.pos.y + other.dim.y)
        if other.pos.x > self.pos.x + self.dim.x:
            minResVec += Vec2d(self.pos.x + self.dim.x - other.pos.x, 0)
        if other.pos.y > self.pos.y + self.dim.y:
            minResVec += Vec2d(0, self.pos.y + self.dim.y - other.pos.y)
        return minResolVec if minResolVec != Vec2d(0, 0) else False

    def intersectsCirc(self, other):
        return other.intersectsBB(self)

class BoundingPolygon(Bounds):
    def __init__(self, points):
        self.points = points

    def __getitem__(self, key):
        key = key % len(self.points)
        return self.points[key]

    def intersectsCirc(self, other):
        return other.intersectsPoly(self)
        

class BoundingCircle(Bounds):
    def __init__(self, x, y, r):
        self.pos = Vec2d(x, y)
        self.r = r

    def intersectsCirc(self, other):
        # minResVec = other.pos - self.pos
        # if minResVec.get_length_sqrd() - (self.r + other.r)**2 < 0:
        #     return minResVec - (self.r + other.r)
        return False

    def intersectsBB(self, other):
        minResVec = Vec2d(0, 0)
        for i in range(4):
            minResVec += self.intersectsLine(other[i], other[i+1])
        return minResVec if minResVec != Vec2d(0, 0) else False

    def intersectsPoly(self, other):
        minResVec = Vec2d(0, 0)
        for i in range(len(other.points)):
            minResVec += self.intersectsLine(other[i], other[i+1])
        return minResVec if minResVec != Vec2d(0, 0) else False        

    # using the image on 2nd answer: 
    # http://stackoverflow.com/questions/1073336/circle-line-collision-detection
    # returns a minimal resolution vector or False
    def intersectsLine(self, point1, point2):
        ac = self.pos - point1
        ab = (point2 - point1)
        ablen = ab.normalize_return_length()
        adlen = ac.dot(ab)
        if adlen < 0:
            aclen = ac.length
            if aclen < self.r: return ac/aclen * self.r - ac
            else: return False
        if adlen > ablen:
            return False
        dcsqrd = ac.get_length_sqrd() - adlen**2
        if dcsqrd < self.r**2:
            return ab.perpendicular() * (self.r - sqrt(dcsqrd))

        return False

class Contact(object):
    def __init__(self, this, other, minResVec):
        self.this = this
        self.other = other
        self.minResVec = minResVec

class Collider(Component):
    def __init__(self, other, minResVec):
        self.other = other
        self.resVec = minResVec
        self.length = minResVec.normalize_return_length()

class CollisionResolver(object):
    @staticmethod
    def resolveCollisions(this, others=None):
        if(others):
            contacts = CollisionResolver.getCollisionsOneToMany(this, others)
        else:
            contacts = CollisionResolver.getCollisionsAll(this)

        CollisionResolver.addColliders(contacts)

    @staticmethod
    def addColliders(contacts):
        for contact in contacts:
            this, other, minResVec = contact.this, contact.other, contact.minResVec
            try: 
                this.contacts.add(Collider(deepcopy(other), minResVec))
            except: pass

            try: 
                other.contacts.add(Collider(deepcopy(this), -minResVec))
            except: pass

    @staticmethod
    def getCollisionsAll(entities):
        contacts = []
        for i, this in enumerate(entities):
            contacts.extend(CollisionResolver.getCollisionsOneToMany(this, 
                entities[i+1:]))
        return contacts

    @staticmethod
    def getCollisionsOneToMany(this, others):
        contacts = []
        for other in others:
                if this != other:
                    minResVec = collides(this, other)
                    if(minResVec):
                        contacts.append(Contact(this, other, minResVec))
        return contacts



        
