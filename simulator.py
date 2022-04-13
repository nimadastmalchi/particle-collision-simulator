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
            return abs(self - other)
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
    VEL_LOSS_ON_BOUNCE_RATIO = 0.85 # velocity becomes 75% at each bounce
    def __init__(self, init_pos: Vector, init_vel : Vector, radius : float, SCREEN_WIDTH : int, SCREEN_HEIGHT : int, color : tuple):
        self.pos = init_pos
        self.vel = init_vel
        self.radius = radius
        self.t = 0
        self.fuel = False
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
        self.color = color

    def get_color(self) -> tuple:
        return self.color

    def get_loc_tuple(self) -> (float, float):
        return (self.pos.getx(), self.pos.gety())

    def get_loc_vector(self) -> Vector:
        return self.pos

    def get_vel(self) -> Vector:
        return self.vel

    def get_rad(self) -> float:
        return self.radius

    def get_mass(self) -> float:
        return self.radius**2 # m = p * A = p * pi * r**2 = r**2, assume p = 1/pi

    def add_time(self, amount : float) -> None:
        self.t += amount

    def add_vel(self, delta_vel : Vector) -> None:
        self.vel = self.vel + delta_vel

    def update_vel(self, vel : Vector) -> None:
        self.vel = vel

    def apply_friction(self) -> None:
        self.vel = self.vel * 0.99

    def surrounds(self, point : Vector) -> bool:
        return self.pos.distance(point) < self.radius

    def add_loc(self, delta_pos : Vector) -> None:
        self.pos = self.pos + delta_pos

    def update_loc(self, dt : float) -> None:
        self.t += dt
        self.pos = self.pos + self.vel * dt

        # account for bounce on edge of screen
        newx, newy = self.pos.getx(), self.pos.gety()
        n = None
        if newx - self.radius <= 0:
            newx = self.radius
            n = Vector(1, 0)
        elif newx + self.radius >= self.SCREEN_WIDTH:
            newx = self.SCREEN_WIDTH - self.radius
            n = Vector(-1, 0)
        if newy - self.radius <= 0:
            newy = self.radius
            n = Vector(0, 1)
        elif newy + self.radius >= self.SCREEN_HEIGHT:
            newy = self.SCREEN_HEIGHT - self.radius
            n = Vector(0, -1)

        if n is not None:
            self.vel = reflect(self.vel * Rocket.VEL_LOSS_ON_BOUNCE_RATIO, n)

        self.pos.setvals((newx, newy))
 
    def __str__(self):
        return f"Rocket[pos={self.pos}, vel={self.vel}, t={self.t}]"

# @depreciated
def collision_check2(this : Rocket, rockets : [], dt : float) -> None:
    for other in rockets:
        if this is other:
            continue
        grav_check(this, other, dt)
        x10 = this.get_loc_vector()
        x20 = other.get_loc_vector()
        if x10.distance(x20) <= this.get_rad() + other.get_rad() and abs(x20 - x10) != 0: #TODO: change to distancesquared to optimize
            v10 = this.get_vel()
            v20 = other.get_vel()
            m1 = this.get_mass()
            m2 = other.get_mass()
            v1n = v10 - ( (x10 - x20) * ((v10 - v20).dot(x10 - x20) / abs(x10 - x20)**2) ) * ( 2*m2 / (m1 + m2) )
            v2n = v20 - ( (x20 - x10) * ((v20 - v10).dot(x20 - x10) / abs(x20 - x10)**2) ) * ( 2*m1 / (m1 + m2) )

            this.update_vel(v1n)
            other.update_vel(v2n)

            # update locations so same collision is not detected between same objects again
            for _ in range(10):
                this.update_loc(dt)
                other.update_loc(dt)

def collision_check(r1 : Rocket, r2 : Rocket, dt : float) -> bool:
    if r1 is r2:
        return

    x10 = r1.get_loc_vector()
    x20 = r2.get_loc_vector()
    if x10.distance(x20) <= r1.get_rad() + r2.get_rad(): #TODO: change to distancesquared to optimize
        v10 = r1.get_vel()
        v20 = r2.get_vel()
        m1 = r1.get_mass()
        m2 = r2.get_mass()
        v1n = v10 - ( (x10 - x20) * ((v10 - v20).dot(x10 - x20) / abs(x10 - x20)**2) ) * ( 2*m2 / (m1 + m2) )
        v2n = v20 - ( (x20 - x10) * ((v20 - v10).dot(x20 - x10) / abs(x20 - x10)**2) ) * ( 2*m1 / (m1 + m2) )

        r1.update_vel(v1n)
        r2.update_vel(v2n)

        # update locations so same collision is not detected between same objects again
        for _ in range(2):
            r1.update_loc(dt)
            r2.update_loc(dt)
    
        return True

    return False

def grav_check(r1 : Rocket, r2 : Rocket, dt : float) -> None:
    if r1 is r2:
        return
    dir_vec = r2.get_loc_vector() - r1.get_loc_vector() # dir vector from r1 to r2
    dir_vec = dir_vec / abs(dir_vec)
    d = abs(r1.get_loc_vector() - r2.get_loc_vector())
    delta_v = dir_vec * r2.get_mass() * dt / d**2
    r1.add_vel(delta_v * 10000)
    r1.update_loc(dt)

if __name__ == "__main__":
    v = Vector(1, 2)
    print(v / abs(v))
