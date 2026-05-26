# python version of the bgt vector written by lucia development team
class vector:
    """an object representing what bgt calls a vector

    This represents a point in 3-space, where positive x is right, positive y is forward, and positive z is up.
    The property coords can be used to get and set a tuple of the coordinates represented by this vector with no rounding applied.

    args:
        x (float, optional): The starting x coordinate of this vector
        y (float, optional): The starting y coordinate of this vector
        z (float, optional): The starting z coordinate of this vector.
    """

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def get_coords(self):
        return (self.x, self.y, self.z)

    def set_coords(self, coords):
        self.x, self.y, self.z = coords

    coords = property(get_coords, set_coords)

    @property
    def get_tuple(self):
        return tuple([round(self.x), round(self.y), round(self.z)])
