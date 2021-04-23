# TODO: implement collision detection and handling ... FIX sim.check_collisions

import pygame
import simulator as sim
import random 

# constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (204, 0, 102)
ORANGE = (255, 128, 0)
GREY = (64, 64, 64)
ZERESHKI = (102, 0, 0)
CYAN = (0, 255, 255)

BALL_COLORS = [BLACK, GREEN, RED, BLUE, PINK, ORANGE, GREY, ZERESHKI, CYAN]

WIDTH = 1000
HEIGHT = 800

GRAV_DELTA_V = 1

REFRESH_RATE = 60

RADIUS_MIN = 10
RADIUS_MAX = 60

INIT_NUM_ROCKETS = 3

dt = 1 / 60

def draw_rocket(screen, r : sim.Rocket):
    loc_tuple = r.get_loc_tuple()
    pygame.draw.circle(screen, r.get_color(), tuple(map(round, loc_tuple)), r.get_rad(), 0)
    # random colors
    #pygame.draw.circle(screen, tuple(random.randint(0, 255) for _ in range(3)), tuple(map(round, loc_tuple)), ROCKET_RADIUS, 0)

if __name__ == "__main__":
    # Open a new window
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Rocket Game")

    carryOn = True
    
    # used to control refresh rate
    clock = pygame.time.Clock()

    rockets = [sim.Rocket(sim.Vector(random.randint(0, WIDTH), random.randint(0, HEIGHT)), sim.Vector(0, 0), random.randint(RADIUS_MIN, RADIUS_MAX+1), WIDTH, HEIGHT, BALL_COLORS[random.randrange(len(BALL_COLORS))]) for _ in range(INIT_NUM_ROCKETS)]

    mouse_pos = None

    fuel = False
    attract = None

    # init font for putting down text
    pygame.font.init()
    myfont = pygame.font.SysFont("Comic Sans MS", 11)

    # -------- Main Program Loop -----------
    while carryOn:
        # --- Main event loop ---
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                carryOn = False
            elif event.type == pygame.MOUSEBUTTONDOWN: # once mouse is down, fueling starts (rocket accelerates toward mouse)
                mouse_state = pygame.mouse.get_pressed() # tuple
                fuel = not mouse_state[1] # fuel up if either left or right button is pressed (not middle mouse button)
                attract = mouse_state[0] # attract if left button is pressed
            elif event.type == pygame.MOUSEBUTTONUP: # once mouse is back up, fueling stops
                fuel = False
            elif event.type == pygame.KEYDOWN:
                print("Adding rocket...")
                mouse_pos = pygame.mouse.get_pos()
                init_loc = sim.Vector(WIDTH / 2, HEIGHT / 2)
                init_vel = sim.Vector(0, 0).setvals(mouse_pos) - init_loc
                init_vel = init_vel
                rocket = sim.Rocket(init_loc, init_vel, random.randint(RADIUS_MIN, RADIUS_MAX+1), WIDTH, HEIGHT, BALL_COLORS[random.randrange(len(BALL_COLORS))])
                rockets.append(rocket)

        # background color
        screen.fill(WHITE)

        # putting text on the screen
        textsurface = myfont.render(f"paricles generated: {len(rockets)}", False, BLACK)
        screen.blit(textsurface, (0, 0))

        for rocket in rockets:
            for other_rocket in rockets:
                if rocket is other_rocket:
                    continue

                if not sim.collision_check(rocket, other_rocket, dt): # apply collision
                    sim.grav_check(rocket, other_rocket, dt) # apply gravity if these two objects did not collide so that the objects are not forced into each other
                

            #rocket.add_vel(sim.Vector(0, GRAV_DELTA_V)) # gravity
            #rocket.apply_friction()

            if fuel:
                # calculate vector from mouse_pos to rocket:
                mouse_pos = pygame.mouse.get_pos()
                delta_vel = sim.Vector().setvals(mouse_pos) - rocket.get_loc_vector()
                delta_vel = delta_vel / abs(delta_vel) * 100
                delta_vel = delta_vel * (1 if attract else -1)
                rocket.add_vel(delta_vel) # adding velocity; hence, accelerating (dv/dt =/= 0)

            rocket.update_loc(dt)
            draw_rocket(screen, rocket)
 
        # update screen
        pygame.display.flip()
        
        # limit to refresh rate
        clock.tick(REFRESH_RATE)
    
    pygame.quit()