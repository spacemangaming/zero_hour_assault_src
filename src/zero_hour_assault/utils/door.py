from sound import sound
from rotation import *
from timer import timer
import globals as g




class door:
    def __init__(
        self,
        doorx,
        doormx,
        doory,
        doormy,
        doorz,
        doormz,
        doorfinishx,
        doorfinishy,
        doorfinishz,
        speed,
        doorsnd3,
        doorsnd4, exitdoor
    ):
        self.exitdoor=exitdoor
        self.ds3 = sound()
        self.ds4 = sound()
        self.dx = 0
        self.dmx = 0
        self.dy = 0
        self.dmy = 0
        self.dz = 0
        self.dmz = 0
        self.finishx = 0
        self.finishy = 0
        self.finishz = 0
        self.movetime = 150
        self.moving = False
        self.aimoving = False
        self.movetimer = timer()



        self.ds3 = doorsnd3
        self.ds4 = doorsnd4
        self.dx = doorx
        self.dmx = doormx
        self.dy = doory
        self.dmy = doormy
        self.dz = doorz
        self.dmz = doormz
        self.finishx = doorfinishx
        self.finishy = doorfinishy
        self.finishz = doorfinishz
        self.movetime = speed


def doorcheckloop():
    for i in range(len(g.doors)):
        if (
            g.doors[i].finishx == round(g.me.x)
            and g.doors[i].finishy == round(g.me.y)
            and g.doors[i].finishz == round(g.me.z)
            and g.doors[i].moving == True
        ):
            g.p.play_extended_3d(g.doors[i].ds4, g.me.x, g.me.y, g.me.z, g.doors[i].dx, g.doors[i].dy, g.doors[i].dz, calculate_theta(g.facing), 0, 0, 0, 0, 0, 0, False, 0.0, 0.0, 0.0, 100.0, False)

            g.n.send_reliable(0, "playonmap " + g.doors[i].ds4, 0)

#            g.p.play_stationary(g.doors[i].ds4, False)
            g.n.send_reliable(0, "playonmap g.doors[i].ds4", 0)
            g.doors[i].moving = False
            g.can_move = True
            g.dmoving = False
            g.n.send_reliable(0, "iamnotdmoving", 0)



        if (
            g.doors[i].moving == True
            and g.doors[i].movetimer.elapsed >= g.doors[i].movetime
        ):
            g.doors[i].movetimer.restart()
            if round(g.me.x) > g.doors[i].finishx:
                g.me.x -= 1
                g.n.send_reliable(
                    0,
                    "move_to " + str(round(g.me.x)) + " " + str(round(g.me.y)) + " " + str(round(g.me.z)),
                    0,
                )

            elif round(g.me.x) < g.doors[i].finishx:
                g.me.x += 1
                g.n.send_reliable(
                    0,
                    "move_to " + str(round(g.me.x)) + " " + str(round(g.me.y)) + " " + str(round(g.me.z)),
                    0,
                )

            if round(g.me.y) > g.doors[i].finishy:
                g.me.y -= 1
                g.n.send_reliable(
                    0,
                    "move_to " + str(round(g.me.x)) + " " + str(round(g.me.y)) + " " + str(round(g.me.z)),
                    0,
                )

            elif round(g.me.y) < g.doors[i].finishy:
                g.me.y += 1
                g.n.send_reliable(
                    0,
                    "move_to " + str(round(g.me.x)) + " " + str(round(g.me.y)) + " " + str(round(g.me.z)),
                    0,
                )

            if round(g.me.z) > g.doors[i].finishz:
                g.me.z -= 1
                g.n.send_reliable(
                    0,
                    "move_to " + str(round(g.me.x)) + " " + str(round(g.me.y)) + " " + str(round(g.me.z)),
                    0,
                )

            elif round(g.me.z) < g.doors[i].finishz:
                g.me.z += 1
                g.n.send_reliable(
                    0,
                    "move_to " + str(round(g.me.x)) + " " + str(round(g.me.y)) + " " + str(round(g.me.z)),
                    0,
                )

def destroy_door(d):
    g.doors.remove(g.doors[d])


def destroy_all_doors():


    g.doors = []


def spawn_door(
    doorx,
    doormx,
    doory,
    doormy,
    doorz,
    doormz,
    finishx,
    finishy,
    finishz,
    speed,
    doorsnd3,
    doorsnd4,exitdoor

):
    door1 = door(
        doorx,
        doormx,
        doory,
        doormy,
        doorz,
        doormz,
        finishx,
        finishy,
        finishz,
        speed,
        doorsnd3,
        doorsnd4, exitdoor

    )
    g.doors.append(door1)
