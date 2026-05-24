import math
from vector import vector

pi = 3.1415926535897932384626433832795
north = 0
northeast = 45
east = 90
southeast = 135
south = 180
southwest = 225
west = 270
northwest = 315
half_up = 45
streight_up = 90
half_down = 135
streight_down = 180

import math
def move(x, y, z=0, deg=0, dir=0):
    if dir != 0:
        d2 = deg + dir
        if d2 >= 360:
            d2 -= 360
        deg = d2
    theta = calculate_theta(deg)
    r = vector()
    r.x = x + math.sin(theta)
    r.y = y + math.cos(theta)
    r.z = round(z + math.sin(calculate_theta(0)))
    return r


def calculate_theta(deg):
    return deg * pi / 180


def getdir(facing):
    if facing >= north and facing < northeast:
        return north
    if facing >= northeast and facing < east:
        return northeast
    if facing >= east and facing < southeast:
        return east
    if facing >= southeast and facing < south:
        return southeast
    if facing >= south and facing < southwest:
        return south
    if facing >= southwest and facing < west:
        return southwest
    if facing >= west and facing < northwest:
        return west
    if facing >= northwest:
        return northwest
    return -1


def snapleft(deg, direction, inc=45):
    d = direction - inc
    if d < 0:
        d += 360
    return d


def snapright(deg, direction, inc=45):
    d = direction + inc
    if d >= 360:
        d -= 360
    return d


def turnleft(deg, inc=45):
    deg -= inc
    if deg < 0:
        deg += 360
    return deg


def turnright(deg, inc=45):
    deg += inc
    if deg >= 360:
        deg -= 360
    return deg


def dir_to_string(direction):
    r = str(direction)
    r = r.replace(str(northwest), "northwest")
    r = r.replace(str(west), "west")
    r = r.replace(str(southwest), "southwest")

    r = r.replace(str(south), "south")
    r = r.replace(str(southeast), "southeast")
    r = r.replace(str(east), "east")
    r = r.replace(str(northeast), "northeast")
    r = r.replace(str(north), "north")
    return r


def get_1d_distance(x1, x2):
    return abs(x1 - x2)


def get_2d_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_3d_distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
def calculate_x_y_angle(x1, y1, x2, y2, deg):
    x = round(x2) - round(x1)
    y = round(y2) - round(y1)
    if x == 0 and y == 0:
        return 0
    if x == 0:
        x += 0.0000001
    if y == 0:
        y += 0.0000001

    rad = math.atan(y / x)
    arctan = rad / pi * 180
    fdeg = 0
    if x > 0:
        fdeg = 90 - arctan
    elif x < 0:
        fdeg = 270 - arctan
    if x == 0:
        if y > 0:
            fdeg = 0
        elif y < 0:
            fdeg = 180
    fdeg -= deg
    if fdeg < 0:
        fdeg += 360

    return round(fdeg)

def calculate_x_y_string(deg):
    if deg == 0:
        return "streight in front"
    elif deg > 0 and deg < 10:
        return "in front and very slightly to the right"
    elif deg > 9 and deg < 20:
        return "in front and slightly off to the right"
    elif deg > 19 and deg < 40:
        return "in front a little ways off to the right"
    elif deg > 39 and deg < 90:
        return "slightly in front and a fair distance off to the right"
    elif deg == 90:
        return "streight off to the right"
    elif deg > 90 and deg < 120:
        return "slightly behind and far off to the right"
    elif deg > 119 and deg < 150:
        return "behind and a little ways off to the right"
    elif deg > 149 and deg < 170:
        return "behind and slightly to the right"
    elif deg > 169 and deg < 180:
        return "behind and very slightly to the right"
    elif deg == 180:
        return "streight behind"
    elif deg > 180 and deg < 190:
        return "behind and very slightly to the left"
    elif deg > 189 and deg < 200:
        return "behind and slightly to the left"
    elif deg > 199 and deg < 220:
        return "behind and a little ways off to the left"
    elif deg > 219 and deg < 240:
        return "behind and a fair distance off to the left"
    elif deg > 239 and deg < 270:
        return "slightly behind and far off to the left"
    elif deg == 270:
        return "streight off to the left"
    elif deg > 270 and deg < 300:
        return "streight off to the left"
    elif deg > 299 and deg < 320:
        return "in front and a ways off to the left"
    elif deg > 319 and deg < 340:
        return "in front and a little ways off to the left"
    elif deg > 339 and deg < 350:
        return "in front and slightly off to the left"
    elif deg > 349 and deg <= 360:
        return "in front and very slightly off to the left"
    return ""


