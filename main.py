from platform import release
import pygame
import math

pygame.init()

HEIGHT = 600
WIDTH = 600
WHITE = (255, 255, 255)
GRAY = (25, 25, 25)
BLACK = (0, 0, 0)
font = pygame.font.SysFont('Arial', 25)

screen = pygame.display.set_mode([WIDTH+200, HEIGHT])
pygame.display.set_caption('Ray Tracing')

pygame.draw.rect(screen, GRAY, pygame.Rect(WIDTH, 0, 200, HEIGHT))

running = True
walls = list()
rays = list()

pi2 = 2 * 3.14
n = 720
using_rayt = False
drawing = False
prev_pos = None

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


    def check_intersection(self, wall):

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

wall1 = Wall(0, 0, WIDTH, 0)
wall2 = Wall(WIDTH, 0, WIDTH, HEIGHT)
wall3 = Wall(WIDTH, HEIGHT, 0, HEIGHT)
wall4 = Wall(0, HEIGHT, 0, 0)

obstacle_wall1 = Wall(0, 0, 100, 100)
obstacle_wall2 = Wall(100, 100, 100, 300)
obstacle_wall3 = Wall(300, 0, 250, 150)
obstacle_wall4 = Wall(300, HEIGHT, 250, HEIGHT-150)

walls.extend([wall1, wall2, wall3, wall4, obstacle_wall1, obstacle_wall2, obstacle_wall3, obstacle_wall4])

# ray tracing btn
pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH+25, 25, 150, 50))
btn_text = font.render('Ray Tracing', True, WHITE)
btn_text_rect = btn_text.get_rect()
btn_text_rect.center = (WIDTH+100, 50)
screen.blit(btn_text, btn_text_rect)

# make walls btn
pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH+25, 100, 150, 50))
btn_text = font.render('Make Walls', True, WHITE)
btn_text_rect = btn_text.get_rect()
btn_text_rect.center = (WIDTH+100, 125)
screen.blit(btn_text, btn_text_rect)

# reset btn
pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH+25, 175, 150, 50))
btn_text = font.render('Reset', True, WHITE)
btn_text_rect = btn_text.get_rect()
btn_text_rect.center = (WIDTH+100, 200)
screen.blit(btn_text, btn_text_rect)

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


    if pygame.mouse.get_pressed()[0]:
        released = False
        if (WIDTH+25 < mouse_pos[0] < WIDTH+175):

            if (25 < mouse_pos[1] < 75):
                using_rayt = True
                drawing = False

            elif (100 < mouse_pos[1] < 150):
                drawing = True
                using_rayt = False
                n = 36
                walls = [wall1, wall2, wall3, wall4]
                pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, WIDTH, HEIGHT))

            elif (175 < mouse_pos[1] < 225):
                using_rayt = False
                drawing = False
                prev_pos = None
                walls = [wall1, wall2, wall3, wall4, obstacle_wall1, obstacle_wall2, obstacle_wall3, obstacle_wall4]
                n = 360
                pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, WIDTH, HEIGHT))

    if using_rayt:
        if 0 < mouse_pos[0] < WIDTH and 0 < mouse_pos[1] < HEIGHT:       
            i = 0
            for ray in rays:
                min_d = math.inf
                record_p = list()
                for wall in walls:
                    point = ray.check_intersection(wall)

                    if point:

                        d = distance_from_points(mouse_pos, point)

                        if d < min_d:
                            min_d = d
                            record_p = point

                if record_p != list():
                    ray.draw(record_p)    

                i += 1

    elif drawing == True:
        if 0 < mouse_pos[0] < WIDTH and pygame.mouse.get_pressed()[0]:
            new_wall = Wall(prev_pos[0] if prev_pos != None else mouse_pos[0], prev_pos[1] if prev_pos != None else mouse_pos[1], mouse_pos[0], mouse_pos[1])
            walls.append(new_wall)
            pygame.draw.line(screen, WHITE, prev_pos if prev_pos != None else mouse_pos, mouse_pos, 1)
            prev_pos = mouse_pos
            


    pygame.display.update()
    if using_rayt:
        pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, WIDTH, HEIGHT))
    rays = list()