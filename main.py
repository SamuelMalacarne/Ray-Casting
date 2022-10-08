import pygame
import math

pygame.init()

HEIGHT = 400
WIDTH = 400
WHITE = (255, 255, 255)
GRAY = (25, 25, 25)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode([WIDTH+200, HEIGHT])
pygame.display.set_caption('Ray Tracing')

pygame.draw.rect(screen, GRAY, pygame.Rect(WIDTH, 0, 200, HEIGHT))

running = True
walls = list()
rays = list()

pi2 = 2 * 3.14
n = 360

class Wall():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self):
        pygame.draw.line(screen, WHITE, (self.x1, self.y1), (self.x2, self.y2))

class Ray():
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos

    def draw(self, end_p):
        self.end_pos = end_p
        pygame.draw.line(screen, WHITE, self.start_pos, self.end_pos)
        

    def check_intersection(self, wall, mouse_pos, i):

        x3 = self.start_pos[0]
        y3 = self.start_pos[1]
        x4 = self.end_pos[0]
        y4 = self.end_pos[1]

        x1 = wall.x1
        y1 = wall.y1
        x2 = wall.x2
        y2 = wall.y2

        denominator = ((x1-x2)*(y3-y4))-((y1-y2)*(x3-x4))
        if denominator != 0:
            t = (((x1-x3)*(y3-y4))-((y1-y3)*(x3-x4))) / denominator
            u = (((x1-x3)*(y1-y2))-((y1-y3)*(x1-x2))) / denominator

            point = [(x1+t*(x2-x1)), (y1+t*(y2-y1))]

            if 0 < t < 1 and u > 0:
                return point
                
            else:
                return 
        
        else:
            return 

def distance_from_points(p1, p2):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]

    return math.sqrt(pow((x1-x2), 2)+pow((y1-y2), 2))


wall1 = Wall(150, 50, 100, 250)
wall2 = Wall(350, 50, 350, 0)
wall3 = Wall(0, 0, WIDTH, 0)
wall4 = Wall(WIDTH, 0, WIDTH, HEIGHT)
wall5 = Wall(WIDTH, HEIGHT, 0, HEIGHT)
wall6 = Wall(0, HEIGHT, 0, 0)

# , wall3, wall4, wall5, wall6

walls.extend([wall1, wall2, wall3, wall4, wall5, wall6])


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()

    for wall in walls:
        wall.draw()


    for i in range(0, n):
            x = math.cos(i / n * pi2) * 1 + mouse_pos[0]
            y = math.sin(i / n * pi2) * 1 + mouse_pos[1]
            rays.append(Ray(mouse_pos, (x, y)))

    using_rayt = True

    if 0 < mouse_pos[0] < WIDTH and 0 < mouse_pos[1] < HEIGHT and using_rayt:       
        i = 0
        for ray in rays:
            min_d = math.inf
            record_p = list()
            for wall in walls:
                point = ray.check_intersection(wall, mouse_pos, i)

                if point:

                    d = distance_from_points(mouse_pos, point)

                    if d < min_d:
                        min_d = d
                        record_p = point

            if record_p != list():
                ray.draw(record_p)    

            i += 1


    pygame.display.update()
    pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, WIDTH, HEIGHT))
    rays = list()
    points = list()