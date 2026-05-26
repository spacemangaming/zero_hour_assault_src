from sound import *
import globals as g
from rotation import *


class msound:
    def __init__(self, i, l, c1, c2, c3, cm, pi):
        self.id = 0
        self.soundloop = ""
        self.map = ""
        self.x = 0
        self.y = 0
        self.z = 0
        self.loopint = -5
        self.pitch = 0

        self.id = i
        self.soundloop = l
        self.x = c1
        self.y = c2
        self.z = c3
        self.pitch = pi
        if cm == g.mapname:
            self.loopint = g.p.play_extended_3d(
                self.soundloop,
                g.me.x,
                g.me.y,
                g.me.z,
                self.x,
                self.y,
                self.z,
                calculate_theta(g.facing),
                0,
                0,
                0,
                0,
                0,
                0,
                self.soundloop.startswith("motor") or self.soundloop.startswith("electric"),
                0,
                0,
                0,
                self.pitch,
                False, True
            )
        else:
            self.loopint = -5
        self.map = cm

    def updateme(self, c1, c2, c3, pi):
        self.x = c1
        self.y = c2
        self.z = c3
        #try:
            #if self.soundloop.startswith("motor") and not self.loopint.handle.player.playing(): self.loopint.handle.play()
        #except: pass
        if g.mapname == self.map and self.loopint == -5:
            self.loopint = g.p.play_extended_3d(
                self.soundloop,
                g.me.x,
                g.me.y,
                g.me.z,
                self.x,
                self.y,
                self.z,
                calculate_theta(g.facing),
                0,
                0,
                0,
                0,
                0,
                0,
                self.soundloop.startswith("motor") or self.soundloop.startswith("electric"),
                0,
                0,
                0,
                self.pitch,
                False, True
            )
            if "electric" in self.soundloop: g.p.update_sound_range_3d(self.loopint, 0, 0, 0, 0, 0, 10, calculate_theta(g.facing))
        if g.mapname != self.map and self.loopint != -5:
            g.p.destroy_sound(self.loopint)
            self.loopint = -5
        if g.mapname == self.map and self.loopint != -5:
            g.p.update_sound_3d(self.loopint, self.x, self.y, self.z)
            if "electric" in self.soundloop: g.p.update_sound_range_3d(self.loopint, 0, 0, 0, 0, 0, 10, calculate_theta(g.facing))
            if pi != self.pitch:
                self.pitch = pi
                g.p.update_sound_start_values(self.loopint, 0, 0, self.pitch)
def createmsound(id, loop, x, y, z, map, pitch):
    m1 = msound(id, loop, x, y, z, map, pitch)
    g.msounds.append(m1)


def updatemsound(id, x, y, z, pitch):
    for i in range(len(g.msounds)):
        if g.msounds[i].id == id:
            g.msounds[i].updateme(x, y, z, pitch)


def destroymsound(id):
    for i in g.msounds:
        if i.id == id:
            g.p.destroy_sound(i.loopint)
            g.msounds.remove(i)


def destroy_all_msounds():
    for i in g.msounds:
        destroymsound(i.id)
def msoundloop():
    for msound in g.msounds:
        msound.updateme(msound.x,msound.y,msound.z,msound.pitch)