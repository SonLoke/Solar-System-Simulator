import pygame #2D graphics library
import math
pygame.init()

#variables & other values
width, height = 800, 650 #dimensions of the window in pixels
win = pygame.display.set_mode((width, height)) #window, or surface, where the simulation will be displayed
pygame.display.set_caption("Solar System Simulator") #window title

#colors
white = (255, 255, 255)
yellow = (255, 255, 0)
blue = (100, 149, 237)
red = (188, 39, 50)
dark_grey = (80, 78, 81)

#font
font = pygame.font.SysFont("roboto", 18)

#celestial bodies
class Celestial_Body:
    au = 149.6e6 * 1000 #1 au (astronomical unit) = 149.600.000.000 Meters
    g = 6.67428e-11 #gravitational constant
    scale = 200 / au #scale space of the simulation in relation to reality; 1 au = 100 pixels
    timestep = 3600*24 #scale of time in the simulation in relation to reality; 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.star = False
        self.distance_to_star = 0

        self.x_vel = 0 #these are the speed the bodies will travel in each direction
        self.y_vel = 0
    
    def draw (self, win): #traces each planet's orbit around & shows their distance to the sun
        x = self.x * self.scale + width / 2
        y = self.y *self.scale + height / 2 

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.scale + width / 2
                y = y * self.scale + height / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.star:
            distance_text = font.render(f"{round(self.distance_to_star/1000, 1)}km", 1, white)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_width()/2))


    def attraction (self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.star:
            self.distance_to_star = distance

        force = self.g * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position (self, celestial_bodies): #this will calculate the speed the bodies move in the X and Y directions, then update their placemente within the simulation.
        total_fx = total_fy = 0
        for celestial_body in celestial_bodies:
            if self == celestial_body:
                continue

            fx, fy = self.attraction(celestial_body)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.timestep
        self.y_vel += total_fy / self.mass * self.timestep
        self.x += self.x_vel*self.timestep
        self.y += self.y_vel*self.timestep
        self.orbit.append((self.x, self.y))

#pygame loop: Keeps track of events happening in the program
def main():
    run = True #while this is set to True, the simulation will keep running
    clock = pygame.time.Clock() #limits the speed of the simulation to a set value, 60 frames per second in this case

    sun = Celestial_Body(0, 0, 30, yellow, 1.98892 * 10**30)
    sun.star = True

    earth = Celestial_Body(1 * Celestial_Body.au, 0, 16, blue, 5.9742 * 10**24)
    earth.y_vel = -29.783 * 1000

    mars = Celestial_Body(1.524 * Celestial_Body.au, 0, 12, red, 6.39 * 10**23)
    mars.y_vel = -24.077 * 1000

    mercury = Celestial_Body(0.387 * Celestial_Body.au, 0, 8, dark_grey, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Celestial_Body(0.723 * Celestial_Body.au, 0, 14, white, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    celestial_bodies = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        win.fill((0, 0, 0))

        for event in pygame.event.get(): #when we click on the "X" button on the top right of the screen, it will change the "run" value to False
            if event.type == pygame.QUIT:
                run = False
        
        for celestial_body in celestial_bodies:
            celestial_body.update_position(celestial_bodies)
            celestial_body.draw(win)

        pygame.display.update() #takes all actions done before the update and paste the mon the screen

    pygame.quit()

main() #calling the event loop function
