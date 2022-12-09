import pygame
import math

WIDTH, HEIGHT = 800, 800

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Inner Planets")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,40,50)
ORANGE = (100,0,100)
YELLOW = (200,200,0)
GREEN = (0,200,0)
BLUE = (50,50,200)
PURPLE = (200,0,200)
DARK_GRAY = (80,80,80)

FONT = pygame.font.SysFont("TerminessTTF NF", 20)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU # 1au = 100px
    TIMESTEP = 3600 * 12 # 0.5day

    def __init__(self, name, x, y, radius, color, mass) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.isSun = False
        self.distance_to_sun = 0
        self.orbit = []

        self.x_velocity = 0
        self.y_velocity = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH/2
                y = y * self.SCALE + WIDTH/2
                updated_points.append((x,y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)
        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.isSun:
            distance_text = FONT.render(f"{self.name}: {round(self.distance_to_sun/1000)}km", 1, WHITE)
            WIN.blit(distance_text, ((x - distance_text.get_width()/2), (y - distance_text.get_height()/2)))
        
        return 0

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt( distance_x**2 + distance_y**2)

        if other.isSun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_velocity += total_fx / self.mass * self.TIMESTEP
        self.y_velocity += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_velocity * self.TIMESTEP
        self.y += self.y_velocity * self.TIMESTEP

        self.orbit.append((self.x, self.y))
        return 0

def main():

    run = True
    clock = pygame.time.Clock()

    sun = Planet('Sun', 0, 0, 30, YELLOW, 1.98892*10**30)
    sun.isSun = True

    mercury = Planet('Mercury', 0.387*Planet.AU, 0, 8, DARK_GRAY, 3.30*10**23)
    mercury.y_velocity = -47.4 * 1000

    venus = Planet('Venus', -0.723*Planet.AU, 0, 14, ORANGE, 4.8685*10*24)
    venus.y_velocity = 35.02 * 1000

    earth = Planet('Earth', 1*Planet.AU, 0, 16, BLUE, 5.9742*10**24)
    earth.y_velocity = -29.783 * 1000

    mars = Planet('Mars', -1.524*Planet.AU, 0, 12, RED, 6.39*10**23)
    mars.y_velocity = 24.077 * 1000

    planets = [sun, mercury, venus, earth, mars]

    while run:
        clock.tick(60)
        WIN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
            
        pygame.display.update()

    pygame.quit()
    return 0

if __name__ == "__main__":
    # main()
    EXIT_CODE = main()
    if EXIT_CODE == 0:
        print('Program exited successfully')
    else:
        print(f'ERROR EXIT CODE: {EXIT_CODE}')