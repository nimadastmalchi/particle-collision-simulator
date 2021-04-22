class Vector:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def setvals(self, tup : tuple):
        if len(tup) != 2:
            raise ValueError(f"unsupported tuple size of {len(tup)} for Vector 2D")
        self.x, self.y = tup[0], tup[1]
        return self

    def getx(self) -> float:
        return self.x

    def gety(self) -> float:
        return self.y

    def dot(self, other) -> float:
        if isinstance(other, self.__class__):
            return self.x * other.x + self.y * other.y
        else:
            raise TypeError(f"unsupported operand type(s) for dot product: {self.__class__} and {type(other)}")

    def distance(self, other) -> float:
        if isinstance(other, self.__class__):
            return abs(abs(self) - abs(other))
        else:
            raise TypeError(f"unsupported operand type(s) for distance: {self.__class__} and {type(other)}")

    def __add__(self, other):
        if isinstance(other, self.__class__):
            x = self.x + other.x
            y = self.y + other.y
        else:
            raise TypeError(f"unsupported operand type(s) for +: {self.__class__} and {type(other)}")
        return Vector(x, y)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            x = self.x - other.x
            y = self.y - other.y
        else:
            raise TypeError(f"unsupported operand type(s) for +: {self.__class__} and {type(other)}")
        return Vector(x, y)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            x = self.x * other.x
            y = self.y * other.y
        elif isinstance(other, int) or isinstance(other, float):
            x = self.x * other
            y = self.y * other
        else:
            TypeError(f"unsupported operand type(s) for *: {self.__class__} and {type(other)}")
        return Vector(x, y)

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            x = self.x / other.x
            y = self.y / other.y
        elif isinstance(other, int) or isinstance(other, float):
            x = self.x / other
            y = self.y / other
        else:
            TypeError(f"unsupported operand type(s) for /: {self.__class__} and {type(other)}")
        return Vector(x, y)

    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5

    def __repr__(self):
        return f"Vector[x={self.x}, y={self.y}]"

    def __str__(self):
        return self.__repr__()


def reflect(v : Vector, n : Vector) -> Vector:
    '''Assuming v is pointed at a surface with normal n, the reflection vector is returned'''
    n = n / abs(n)
    return v - n * v.dot(n) * 2

class Rocket:
    VEL_LOSS_ON_BOUNCE_RATIO = 0.75 # velocity becomes 75% at each bounce
    def __init__(self, init_pos: Vector, init_vel : Vector, WIDTH : int, HEIGHT : int):
        self.pos = init_pos
        self.vel = init_vel
        self.t = 0
        self.fuel = False
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT

    def add_vel(self, delta_vel : Vector) -> None:
        self.vel = self.vel + delta_vel

    def update_vel(self, vel : Vector) -> None:
        self.vel = vel

    def update_loc(self, dt : float) -> None:
        self.t += dt
        self.pos = self.pos + self.vel * dt

        # account for bounce on edge of screen
        newx, newy = self.pos.getx(), self.pos.gety()
        n = None
        if newx <= 0:
            newx = 0
            n = Vector(1, 0)
        elif newx >= self.WIDTH:
            newx = self.WIDTH
            n = Vector(-1, 0)
        if newy <= 0:
            newy = 0
            n = Vector(0, 1)
        elif newy >= self.HEIGHT:
            newy = self.HEIGHT
            n = Vector(0, -1)

        if n is not None:
            self.vel = reflect(self.vel * Rocket.VEL_LOSS_ON_BOUNCE_RATIO, n)

        self.pos.setvals((newx, newy))
 
    def get_loc_tuple(self) -> (float, float):
        return (self.pos.getx(), self.pos.gety())

    def get_loc_vector(self) -> Vector:
        return self.pos

    def __str__(self):
        return f"Rocket[pos={self.pos}, vel={self.vel}, t={self.t}]"

def collision_check(this : Rocket, rockets : [], radius : int):
    for other in rockets:
        if this is other:
            continue
        this_loc, other_loc = this.get_loc_vector(), other.get_loc_vector()
        if this.get_loc_vector().distance(other.get_loc_vector()) < radius: #TODO: change to distancesquared to optimize
            this_dir = this_loc / abs(this_loc)
            other_dir = other_loc / abs(other_loc)
            new_this = other_dir * abs(this_loc)
            new_other = this_dir * abs(other_loc)
            this.update_vel(new_this)
            other.update_vel(new_other)
 
if __name__ == "__main__":
    print(Vector(1, 1).distance(Vector(2, 2)))