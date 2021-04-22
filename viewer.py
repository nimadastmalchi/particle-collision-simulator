# TODO: implement collision detection and handling ... FIX sim.check_collisions

import pygame
import simulator as sim
import random 

# constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH = 1000
HEIGHT = 700

GRAV_DELTA_V = 0.1

REFRESH_RATE = 60

ROCKET_RADIUS = 10

INIT_NUM_ROCKETS = 1000

dt = 1

def draw_rocket(screen, r : sim.Rocket):
    loc_tuple = r.get_loc_tuple()
    pygame.draw.circle(screen, BLACK, tuple(map(round, loc_tuple)), ROCKET_RADIUS, 0)
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

    rockets = [sim.Rocket(sim.Vector(random.randint(0, WIDTH), random.randint(0, HEIGHT)), sim.Vector(0, 0), WIDTH, HEIGHT) for _ in range(INIT_NUM_ROCKETS)]

    mouse_pos = None

    fuel = False

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
                fuel = True
            elif event.type == pygame.MOUSEBUTTONUP: # once mouse is back up, fueling stops
                fuel = False
            elif event.type == pygame.KEYDOWN:
                print("Adding rocket")
                rocket = sim.Rocket(sim.Vector(WIDTH / 2, HEIGHT / 2), sim.Vector(0, 0), WIDTH, HEIGHT)
                rockets.append(rocket)
 
        # background color
        screen.fill(WHITE)

        # putting text on the screen
        textsurface = myfont.render(f"paricles generated: {len(rockets)}", False, BLACK)
        screen.blit(textsurface, (0, 0))

        for rocket in rockets:
            #sim.collision_check(rocket, rockets, ROCKET_RADIUS)

            rocket.add_vel(sim.Vector(0, GRAV_DELTA_V)) # gravity

            if fuel:
                mouse_pos = pygame.mouse.get_pos()
                delta_vel = sim.Vector().setvals(mouse_pos) - rocket.get_loc_vector()
                delta_vel = delta_vel / abs(delta_vel) * 10
                rocket.add_vel(delta_vel) # adding velocity; hence, accelerating (dv/dt =/= 0)

            rocket.update_loc(dt)
            draw_rocket(screen, rocket)
 
        # update screen
        pygame.display.flip()
        
        # limit to refresh rate
        clock.tick(REFRESH_RATE)
    
    pygame.quit()