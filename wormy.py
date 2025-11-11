import random
import pygame
import sys
from pygame.locals import *

FPS = 15
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
assert WINDOW_WIDTH % CELL_SIZE == 0, "Window width must be a multiple of cell size."
assert WINDOW_HEIGHT % CELL_SIZE == 0, "Window height must be a multiple of cell size."
CELL_WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
CELL_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
OBS_COL   = '#908a9c'
BG_COLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 

def main():
    global CLOCK, DISPLAY_SURF, BASIC_FONT, DISPLAY_CENTER

    pygame.init()
    CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 18)
    DISPLAY_CENTER = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2) # mora da bide int ( da se deli so // namesto so /)
    pygame.display.set_caption('Wormy')

    show_start_screen()
    while True:
        runGame()
        show_game_over_screen()


def runGame():
    start_x = random.randint(5, CELL_WIDTH - 10)
    start_y = random.randint(5, CELL_HEIGHT - 10)
    worm_coords = [{'x': start_x,     'y': start_y},
                  {'x': start_x - 1, 'y': start_y},
                  {'x': start_x - 2, 'y': start_y}]
    direction = RIGHT

    # Minimum 5 obstacles - Maximum 5% of cells
    number_of_obstacles = random.randint(5, int(CELL_WIDTH * CELL_HEIGHT * 0.05))
    obstacles_coords = get_obstacle_coords(number_of_obstacles)

    apple = get_random_safe_location(obstacles_coords)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        if worm_coords[HEAD]['x'] == -1 or worm_coords[HEAD]['x'] == CELL_WIDTH or worm_coords[HEAD]['y'] == -1 or worm_coords[HEAD]['y'] == CELL_HEIGHT:
            return
        for wormBody in worm_coords[1:]:
            if wormBody['x'] == worm_coords[HEAD]['x'] and wormBody['y'] == worm_coords[HEAD]['y']:
                return

        new_head = move_worm_head_in_direction(worm_coords, direction)

        if new_head in obstacles_coords:# check if move runs into obstacle
            pass
        else:
            # check if worm has eaten an apple
            if worm_coords[HEAD]['x'] == apple['x'] and worm_coords[HEAD]['y'] == apple['y']:
                # don't remove worm's tail segment
                apple = get_random_safe_location(obstacles_coords)  # set a new apple somewhere
            else:
                del worm_coords[-1]  # remove worm's tail segment

            worm_coords.insert(0, new_head)

        DISPLAY_SURF.fill(BG_COLOR)
        draw_grid()
        draw_worm(worm_coords)
        draw_obstacles(obstacles_coords)
        draw_apple(apple)
        draw_score(len(worm_coords) - 3)
        pygame.display.update()
        CLOCK.tick(FPS)

def draw_press_key_msg():
    pressKeySurf = BASIC_FONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 30)
    DISPLAY_SURF.blit(pressKeySurf, pressKeyRect)

def check_for_key_press():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def show_start_screen():
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title_surf1 = title_font.render('Wormy!', True, WHITE, DARKGREEN) # Kvadratot se crta kako pozadina na tekstot
    title_surf2 = title_font.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAY_SURF.fill(BG_COLOR)
        # Ako se rotira originalnate povrshina se gubi kvalitet
        rotated_surf1 = pygame.transform.rotate(title_surf1, degrees1)
        rotated_rect1 = rotated_surf1.get_rect()
        rotated_rect1.center = DISPLAY_CENTER
        DISPLAY_SURF.blit(rotated_surf1, rotated_rect1)

        rotated_surf2 = pygame.transform.rotate(title_surf2, degrees2)
        rotated_rect2 = rotated_surf2.get_rect()
        rotated_rect2.center = DISPLAY_CENTER
        DISPLAY_SURF.blit(rotated_surf2, rotated_rect2)

        draw_press_key_msg()

        if check_for_key_press():
            pygame.event.get()
            return
        pygame.display.update()
        CLOCK.tick(FPS)
        degrees1 += 3
        degrees2 += 7

def terminate():
    pygame.quit()
    sys.exit()

def get_random_safe_location(obstacle_coords):
    location = {'x': random.randint(0, CELL_WIDTH - 1), 'y': random.randint(0, CELL_HEIGHT - 1)}
    while location in obstacle_coords:
        location = {'x': random.randint(0, CELL_WIDTH - 1), 'y': random.randint(0, CELL_HEIGHT - 1)}
    return location

def show_game_over_screen():
    game_over_font = pygame.font.Font('freesansbold.ttf', 150)
    game_surf = game_over_font.render('Game', True, WHITE)
    over_surf = game_over_font.render('Over', True, WHITE)
    game_rect = game_surf.get_rect()
    over_rect = over_surf.get_rect()
    # game_rect.midtop = (WINDOW_WIDTH / 2, 70)
    # over_rect.midtop = (WINDOW_WIDTH / 2, game_rect.height + 70 + 25)
    # Nacin koj koristi pomalku "Magic numbers"
    game_rect.center = (DISPLAY_CENTER[0], DISPLAY_CENTER[1] - game_surf.get_height() // 2)
    over_rect.center = (DISPLAY_CENTER[0], DISPLAY_CENTER[1] + over_surf.get_height() // 2)

    DISPLAY_SURF.blit(game_surf, game_rect)
    DISPLAY_SURF.blit(over_surf, over_rect)
    draw_press_key_msg()
    pygame.display.update()
    pygame.time.wait(500)
    check_for_key_press()

    while True:
        if check_for_key_press():
            pygame.event.get() # clear event queue
            return

def draw_score(score):
    scoreSurf = BASIC_FONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOW_WIDTH - 120, 10)
    DISPLAY_SURF.blit(scoreSurf, scoreRect)

def draw_worm(worm_coords):
    for coord in worm_coords:
        x = coord['x'] * CELL_SIZE
        y = coord['y'] * CELL_SIZE
        worm_segment_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAY_SURF, DARKGREEN, worm_segment_rect)
        worm_inner_segment_rect = pygame.Rect(x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8)
        pygame.draw.rect(DISPLAY_SURF, GREEN, worm_inner_segment_rect)

def draw_apple(coord):
    x = coord['x'] * CELL_SIZE
    y = coord['y'] * CELL_SIZE
    appleRect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(DISPLAY_SURF, RED, appleRect)

def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE): # draw vertical lines
        pygame.draw.line(DISPLAY_SURF, DARKGRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE): # draw horizontal lines
        pygame.draw.line(DISPLAY_SURF, DARKGRAY, (0, y), (WINDOW_WIDTH, y))

def get_obstacle_coords(number_of_obstacles):
    obstacles = []
    for i in range(number_of_obstacles):
        x = random.randint(0, CELL_WIDTH - 1)
        y = random.randint(0, CELL_HEIGHT - 1)
        obstacles.append({'x':x, 'y':y})
    return tuple(obstacles)

def draw_obstacles(obstacles):
    for coord in obstacles:
        x = coord['x'] * CELL_SIZE
        y = coord['y'] * CELL_SIZE
        obstacle_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAY_SURF, OBS_COL, obstacle_rect)
        obstacle_inner_segment_rect = pygame.Rect(x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4)
        pygame.draw.rect(DISPLAY_SURF, DARKGRAY, obstacle_inner_segment_rect)

def move_worm_head_in_direction(worm_coords, direction):
    if direction == UP:
        new_head = {'x': worm_coords[HEAD]['x'], 'y': worm_coords[HEAD]['y'] - 1}
    elif direction == DOWN:
        new_head = {'x': worm_coords[HEAD]['x'], 'y': worm_coords[HEAD]['y'] + 1}
    elif direction == LEFT:
        new_head = {'x': worm_coords[HEAD]['x'] - 1, 'y': worm_coords[HEAD]['y']}
    elif direction == RIGHT:
        new_head = {'x': worm_coords[HEAD]['x'] + 1, 'y': worm_coords[HEAD]['y']}
    else:
        new_head = {'x': worm_coords[HEAD]['x'], 'y': worm_coords[HEAD]['y']}
    return new_head

if __name__ == '__main__':
    main()