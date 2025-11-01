import random
import heapq
import copy
import time

import pygame

pygame.init()

WIDTH = 800
HEIGHT = 860  # Increased to accommodate UI panel

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Squid Board")
font = pygame.font.Font("freesansbold.ttf", 20)
timer = pygame.time.Clock()
fps = 60

red_pieces = ['circle', 'square', 'triangle', 'square', 'circle']
red_guns = ['short_gun', 'long_gun', 'blast_gun', 'long_gun', 'short_gun']
red_locations = [(2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]  # Centered at top
red_healths = [30, 30, 30, 30, 30]
captured_pieces_red = []

blue_pieces = ['circle', 'square', 'triangle', 'square', 'circle']
blue_guns = ['short_gun', 'long_gun', 'blast_gun', 'long_gun', 'short_gun']
blue_locations = [(3, 9), (4, 9), (5, 9), (6, 9), (7, 9)]  # Centered at bottom  
blue_healths = [30, 30, 30, 30, 30]
captured_pieces_blue = []

# 0 - red turn no selection: 1-red turn piece selected: 2-red turn shooting: 3- blue turn no selection, 4 - blue turn piece selected: 5-blue turn shooting

turn_step = random.choice([0, 3])
selection = 100
valid_moves = []
valid_shoot = []
health_pickup_exist = 0
health_pickup_location = []

# Stores the index of dead pieces. This is used to disable (visibility off) dead pieces after they die.
dead_red = []
dead_blue = []

# Game over state
game_over = False
winner = None

# Stalemate detection
consecutive_no_actions = 0  # Track consecutive turns with no valid actions
MAX_NO_ACTIONS = 2  # If both players can't move, declare stalemate

# AI configuration
AI_ENABLED = True  # AI vs AI mode
AI_DELAY = 0.5  # Delay in seconds between AI moves for visualization
MINIMAX_DEPTH = 3  # Depth for Minimax search (3-4 for balanced performance)


# Weapon
short_gun = pygame.image.load("res/weapon/short.png")
short_gun = pygame.transform.scale(short_gun, (18, 18))

long_gun = pygame.image.load("res/weapon/long.png")
long_gun = pygame.transform.scale(long_gun, (18, 18))

blast_gun = pygame.image.load("res/weapon/blast.png")
blast_gun = pygame.transform.scale(blast_gun, (16, 16))

# Pieces
red_circle = pygame.image.load("res/circle_red.png")
red_circle = pygame.transform.scale(red_circle, (55, 55))
red_square = pygame.image.load("res/square_red.png")
red_square = pygame.transform.scale(red_square, (55, 55))
red_triangle = pygame.image.load("res/triangle_red.png")
red_triangle = pygame.transform.scale(red_triangle, (55, 55))

blue_circle = pygame.image.load("res/circle_blue.png")
blue_circle = pygame.transform.scale(blue_circle, (55, 55))
blue_square = pygame.image.load("res/square_blue.png")
blue_square = pygame.transform.scale(blue_square, (55, 55))
blue_triangle = pygame.image.load("res/triangle_blue.png")
blue_triangle = pygame.transform.scale(blue_triangle, (55, 55))

health_pickup = pygame.image.load("res/health_pickup.png")
health_pickup = pygame.transform.scale(health_pickup, (55, 55))

red_images = [red_circle, red_square, red_triangle]
blue_images = [blue_circle, blue_square, blue_triangle]
gun_images = [short_gun, long_gun, blast_gun]

piece_list = ['circle', 'square', 'triangle']
gun_list = ['short_gun', 'long_gun', 'blast_gun']

# Sounds
fire_sfx = pygame.mixer.Sound("res/Sounds/fire.mp3")
reload_sfx = pygame.mixer.Sound("res/Sounds/reload.mp3")
piece_place_sfx = pygame.mixer.Sound("res/Sounds/piece_place.mp3")
death_sfx = pygame.mixer.Sound("res/Sounds/death.mp3")


# check variables/ flashing counter


def draw_board():
    # Draw checkerboard with better colors
    for i in range(10):
        for j in range(10):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, (240, 240, 245), [j * 80, i * 80, 80, 80])  # Light tile
            else:
                pygame.draw.rect(screen, (200, 210, 220), [j * 80, i * 80, 80, 80])  # Darker tile
    
    # Draw grid lines with softer color
    for i in range(1, 10):
        pygame.draw.line(screen, (150, 150, 160), (0, 80 * i), (800, 80 * i), 1)
        pygame.draw.line(screen, (150, 150, 160), (80 * i, 0), (80 * i, 800), 1)
    
    # Draw border
    pygame.draw.rect(screen, (80, 80, 90), [0, 0, WIDTH, HEIGHT], 4)


def draw_piece():
    # Red
    for i in range(len(red_pieces)):
        if i in dead_red:
            continue

        index = piece_list.index(red_pieces[i])
        index_gun = gun_list.index(red_guns[i])
        
        # Draw shadow effect
        shadow_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surface, (0, 0, 0, 50), (30, 30), 28)
        screen.blit(shadow_surface, (red_locations[i][0] * 80 + 10, red_locations[i][1] * 80 + 22))
        
        # Draw piece
        screen.blit(red_images[index], (red_locations[i][0] * 80 + 12.5, red_locations[i][1] * 80 + 20.5))

        # Guns
        if red_guns[i] == 'blast_gun':
            screen.blit(gun_images[index], (red_locations[i][0] * 80 + 50, red_locations[i][1] * 80 + 5))
        else:
            screen.blit(gun_images[index], (red_locations[i][0] * 80 + 48, red_locations[i][1] * 80 + 8))

        # Enhanced health bar with gradient colors
        health_percent = red_healths[i] / 30.0
        if health_percent > 0.6:
            health_color = (50, 205, 50)  # Green
        elif health_percent > 0.3:
            health_color = (255, 215, 0)  # Yellow
        else:
            health_color = (255, 69, 0)  # Red-orange
        
        # Health bar background
        pygame.draw.rect(screen, (60, 60, 60), [red_locations[i][0] * 80 + 14, red_locations[i][1] * 80 + 11.5, 32, 9])
        # Health bar border
        pygame.draw.rect(screen, (200, 200, 200), [red_locations[i][0] * 80 + 14, red_locations[i][1] * 80 + 11.5, 32, 9], 1)
        # Health bar fill
        pygame.draw.rect(screen, health_color, [red_locations[i][0] * 80 + 15, red_locations[i][1] * 80 + 12.5, red_healths[i], 7])

        # Selection highlight with glow effect
        if turn_step < 3 and selection == i:
            # Outer glow
            glow_surface = pygame.Surface((84, 84), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (255, 100, 100, 100), [0, 0, 84, 84], 8, border_radius=10)
            screen.blit(glow_surface, (red_locations[i][0] * 80 - 2, red_locations[i][1] * 80 - 2))
            # Inner border
            pygame.draw.rect(screen, (255, 50, 50), [red_locations[i][0] * 80 + 1, red_locations[i][1] * 80 + 1, 78, 78], 3, border_radius=8)

    # Blue
    for i in range(len(blue_pieces)):
        if i in dead_blue:
            continue

        index = piece_list.index(blue_pieces[i])
        
        # Draw shadow effect
        shadow_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surface, (0, 0, 0, 50), (30, 30), 28)
        screen.blit(shadow_surface, (blue_locations[i][0] * 80 + 10, blue_locations[i][1] * 80 + 22))
        
        # Draw piece
        screen.blit(blue_images[index], (blue_locations[i][0] * 80 + 12.5, blue_locations[i][1] * 80 + 20.5))

        # Guns
        if blue_guns[i] == 'blast_gun':
            screen.blit(gun_images[index], (blue_locations[i][0] * 80 + 50, blue_locations[i][1] * 80 + 5))
        else:
            screen.blit(gun_images[index], (blue_locations[i][0] * 80 + 48, blue_locations[i][1] * 80 + 8))

        # Enhanced health bar with gradient colors
        health_percent = blue_healths[i] / 30.0
        if health_percent > 0.6:
            health_color = (50, 205, 50)  # Green
        elif health_percent > 0.3:
            health_color = (255, 215, 0)  # Yellow
        else:
            health_color = (255, 69, 0)  # Red-orange
        
        # Health bar background
        pygame.draw.rect(screen, (60, 60, 60), [blue_locations[i][0] * 80 + 14, blue_locations[i][1] * 80 + 11.5, 32, 9])
        # Health bar border
        pygame.draw.rect(screen, (200, 200, 200), [blue_locations[i][0] * 80 + 14, blue_locations[i][1] * 80 + 11.5, 32, 9], 1)
        # Health bar fill
        pygame.draw.rect(screen, health_color, [blue_locations[i][0] * 80 + 15, blue_locations[i][1] * 80 + 12.5, blue_healths[i], 7])

        # Selection highlight with glow effect
        if turn_step >= 3 and selection == i:
            # Outer glow
            glow_surface = pygame.Surface((84, 84), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (100, 150, 255, 100), [0, 0, 84, 84], 8, border_radius=10)
            screen.blit(glow_surface, (blue_locations[i][0] * 80 - 2, blue_locations[i][1] * 80 - 2))
            # Inner border
            pygame.draw.rect(screen, (50, 120, 255), [blue_locations[i][0] * 80 + 1, blue_locations[i][1] * 80 + 1, 78, 78], 3, border_radius=8)


def spawn_health_pickup(exist):
    if exist == 0:
        exist = 1
        while True:
            a = (random.randint(0, 9), random.randint(2, 7))
            if a not in red_locations and a not in blue_locations:
                health_pickup_location.append(a)
                screen.blit(health_pickup, (a[0] * 80 + 48, a[1] * 80 + 8))
                break


def draw_ui_info():
    """Draw turn indicator and team status at the bottom"""
    # Background panel
    panel_height = 60
    panel_y = HEIGHT - panel_height
    
    # Semi-transparent panel
    panel_surface = pygame.Surface((WIDTH, panel_height), pygame.SRCALPHA)
    panel_surface.fill((40, 40, 50, 230))
    screen.blit(panel_surface, (0, panel_y))
    
    # Border line
    pygame.draw.line(screen, (100, 100, 120), (0, panel_y), (WIDTH, panel_y), 2)
    
    # Turn indicator
    turn_font = pygame.font.Font("freesansbold.ttf", 24)
    if turn_step < 3:
        turn_text = turn_font.render("Red Team's Turn", True, (255, 120, 120))
        turn_color = (255, 100, 100)
    else:
        turn_text = turn_font.render("Blue Team's Turn", True, (120, 180, 255))
        turn_color = (100, 150, 255)
    
    # Turn indicator circle
    pygame.draw.circle(screen, turn_color, (100, panel_y + 30), 15)
    pygame.draw.circle(screen, (255, 255, 255), (100, panel_y + 30), 15, 2)
    
    screen.blit(turn_text, (130, panel_y + 15))
    
    # Team status - Red
    red_alive = len([i for i in range(len(red_pieces)) if i not in dead_red])
    red_status_text = pygame.font.Font("freesansbold.ttf", 18).render(f"Red: {red_alive}/5", True, (255, 150, 150))
    screen.blit(red_status_text, (500, panel_y + 20))
    
    # Team status - Blue
    blue_alive = len([i for i in range(len(blue_pieces)) if i not in dead_blue])
    blue_status_text = pygame.font.Font("freesansbold.ttf", 18).render(f"Blue: {blue_alive}/5", True, (150, 200, 255))
    screen.blit(blue_status_text, (630, panel_y + 20))


# Check all the pieces valid move
def check_option(pieces, locations, turn, own_locations=None, enemy_locations=None):
    """
    Check valid moves for pieces.
    If own_locations/enemy_locations not provided, uses global red_locations/blue_locations
    """
    if own_locations is None:
        own_locations = red_locations if turn == 'red' else blue_locations
    if enemy_locations is None:
        enemy_locations = blue_locations if turn == 'red' else red_locations
        
    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'circle':
            moves_list = check_circle(location, turn, own_locations, enemy_locations)

        elif piece == 'square':
            moves_list = check_square(location, turn, own_locations, enemy_locations)
        elif piece == 'triangle':
            moves_list = check_triangle(location, turn, own_locations, enemy_locations)

        all_moves_list.append(moves_list)
    return all_moves_list


def check_shoot(pieces, locations, turn, own_locations=None, enemy_locations=None):
    """
    Check valid shoot targets for pieces.
    If own_locations/enemy_locations not provided, uses global red_locations/blue_locations
    """
    if own_locations is None:
        own_locations = red_locations if turn == 'red' else blue_locations
    if enemy_locations is None:
        enemy_locations = blue_locations if turn == 'red' else red_locations
        
    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'short_gun':
            moves_list = check_short_gun(location, turn, own_locations, enemy_locations)

        elif piece == 'long_gun':
            moves_list = check_long_gun(location, turn, own_locations, enemy_locations)
        elif piece == 'blast_gun':
            moves_list = check_blast(location, turn)

        all_moves_list.append(moves_list)
    return all_moves_list


def check_short_gun(position, color, _red_locations, _blue_locations):
    moves_list = []
    if color == 'red':
        if (position[0], position[1] + 1) not in _red_locations and position[1] < 9:
            moves_list.append((position[0], position[1] + 1))

        if ((position[0], position[1] + 2) not in _red_locations and position[1] < 8 and
                (position[0], position[1] + 1) not in _blue_locations):
            moves_list.append((position[0], position[1] + 2))

        if (position[0] + 1, position[1]) not in _red_locations and position[0] < 9:
            moves_list.append((position[0] + 1, position[1]))

        if (position[0] + 2, position[1]) not in _red_locations and position[0] < 8 and (
                position[0] + 1, position[1]) not in _blue_locations:
            moves_list.append((position[0] + 2, position[1]))

        if (position[0], position[1] - 1) not in _red_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))

        if (position[0], position[1] - 2) not in _red_locations and position[1] > 1 and (
                position[0], position[1] - 1) not in _blue_locations:
            moves_list.append((position[0], position[1] - 2))

        if (position[0] - 1, position[1]) not in _red_locations and position[0] > 0:
            moves_list.append((position[0] - 1, position[1]))

        if (position[0] - 2, position[1]) not in _red_locations and position[0] > 1 and (
                position[0] - 1, position[1]) not in _blue_locations:
            moves_list.append((position[0] - 2, position[1]))

    else:
        if (position[0], position[1] + 1) not in _blue_locations and position[1] < 9:
            moves_list.append((position[0], position[1] + 1))

        if (position[0], position[1] + 2) not in _blue_locations and position[1] < 8 and (
                position[0], position[1] + 1) not in _red_locations:
            moves_list.append((position[0], position[1] + 2))

        if (position[0] + 1, position[1]) not in _blue_locations and position[0] < 9:
            moves_list.append((position[0] + 1, position[1]))

        if (position[0] + 2, position[1]) not in _blue_locations and position[0] < 8 and (
                position[0] + 1, position[1]) not in _red_locations:
            moves_list.append((position[0] + 2, position[1]))

        if (position[0], position[1] - 1) not in _blue_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))

        if (position[0], position[1] - 2) not in _blue_locations and position[1] > 1 and (
                position[0], position[1] - 1) not in _red_locations:
            moves_list.append((position[0], position[1] - 2))

        if (position[0] - 1, position[1]) not in _blue_locations and position[0] > 0:
            moves_list.append((position[0] - 1, position[1]))

        if (position[0] - 2, position[1]) not in _blue_locations and position[0] > 1 and (
                position[0] - 1, position[1]) not in _red_locations:
            moves_list.append((position[0] - 2, position[1]))

    return moves_list


def check_long_gun(position, color, _red_locations, _blue_locations):
    moves_list = []
    if color == 'red':
        if (position[0] + 1, position[1] + 1) not in _red_locations and position[0] < 9 and position[1] < 9:
            moves_list.append((position[0] + 1, position[1] + 1))

        if (position[0] + 2, position[1] + 2) not in _red_locations and position[0] < 8 and position[1] < 8 and (
                position[0] + 1, position[1] + 1) not in _blue_locations:
            moves_list.append((position[0] + 2, position[1] + 2))

        if (position[0] + 1, position[1] - 1) not in _red_locations and position[0] < 9 and position[1] > 0:
            moves_list.append((position[0] + 1, position[1] - 1))

        if (position[0] + 2, position[1] - 2) not in _red_locations and position[0] < 8 and position[1] > 1 and (
                position[0] + 1, position[1] - 1) not in _blue_locations:
            moves_list.append((position[0] + 2, position[1] - 2))

        if (position[0] - 1, position[1] + 1) not in _red_locations and position[0] > 0 and position[1] < 9:
            moves_list.append((position[0] - 1, position[1] + 1))

        if (position[0] - 2, position[1] + 2) not in _red_locations and position[0] > 1 and position[1] < 8 and (
                position[0] - 1, position[1] + 1) not in _blue_locations:
            moves_list.append((position[0] - 2, position[1] + 2))

        if (position[0] - 1, position[1] - 1) not in _red_locations and position[0] > 0 and position[1] > 0:
            moves_list.append((position[0] - 1, position[1] - 1))

        if (position[0] - 2, position[1] - 2) not in _red_locations and position[0] > 1 and position[1] > 1 and (
                position[0] - 1, position[1] - 1) not in _blue_locations:
            moves_list.append((position[0] - 2, position[1] - 2))

    else:
        if (position[0] + 1, position[1] + 1) not in _blue_locations and position[0] < 9 and position[1] < 9:
            moves_list.append((position[0] + 1, position[1] + 1))

        if (position[0] + 2, position[1] + 2) not in _blue_locations and position[0] < 8 and position[1] < 8 and (
                position[0] + 1, position[1] + 1) not in _red_locations:
            moves_list.append((position[0] + 2, position[1] + 2))

        if (position[0] + 1, position[1] - 1) not in _blue_locations and position[0] < 9 and position[1] > 0:
            moves_list.append((position[0] + 1, position[1] - 1))

        if (position[0] + 2, position[1] - 2) not in _blue_locations and position[0] < 8 and position[1] > 1 and (
                position[0] + 1, position[1] - 1) not in _red_locations:
            moves_list.append((position[0] + 2, position[1] - 2))

        if (position[0] - 1, position[1] + 1) not in _blue_locations and position[0] > 0 and position[1] < 9:
            moves_list.append((position[0] - 1, position[1] + 1))

        if (position[0] - 2, position[1] + 2) not in _blue_locations and position[0] > 1 and position[1] < 8 and (
                position[0] - 1, position[1] + 1) not in _red_locations:
            moves_list.append((position[0] - 2, position[1] + 2))

        if (position[0] - 1, position[1] - 1) not in _blue_locations and position[0] > 0 and position[1] > 0:
            moves_list.append((position[0] - 1, position[1] - 1))

        if (position[0] - 2, position[1] - 2) not in _blue_locations and position[0] > 1 and position[1] > 1 and (
                position[0] - 1, position[1] - 1) not in _red_locations:
            moves_list.append((position[0] - 2, position[1] - 2))

    return moves_list


def check_blast(position, color):
    moves_list = []
    # Check all 4 cardinal directions at distance 2, ensuring within bounds
    if position[0] + 2 <= 9:  # Right
        moves_list.append((position[0] + 2, position[1]))
    if position[1] + 2 <= 9:  # Down
        moves_list.append((position[0], position[1] + 2))
    if position[0] - 2 >= 0:  # Left
        moves_list.append((position[0] - 2, position[1]))
    if position[1] - 2 >= 0:  # Up
        moves_list.append((position[0], position[1] - 2))
    return moves_list


def blast_damage(position, _red_locations, _blue_locations):
    print("Blast")
    #print('position')
    #print(position)
    for i in range(len(red_pieces)):
        # Skip dead pieces
        if i in dead_red:
            continue
            
        a = abs(position[0] - _red_locations[i][0])
        b = abs(position[1] - _red_locations[i][1])

        #print((_red_locations[i][0], _red_locations[i][1]))
        if a + b == 0:
            red_healths[i] -= 29
        elif (a + b) == 1:
            red_healths[i] -= 14
        elif (a + b) == 2:
            if (position[0] + 1, position[1] + 1) == (_red_locations[i][0], _red_locations[i][1]):
                red_healths[i] -= 7
            elif (position[0] + 1, position[1] - 1) == (_red_locations[i][0], _red_locations[i][1]):
                red_healths[i] -= 7
            elif (position[0] - 1, position[1] - 1) == (_red_locations[i][0], _red_locations[i][1]):
                red_healths[i] -= 7
            elif (position[0] - 1, position[1] + 1) == (_red_locations[i][0], _red_locations[i][1]):
                red_healths[i] -= 7

    for i in range(len(blue_pieces)):
        # Skip dead pieces
        if i in dead_blue:
            continue
            
        a = abs(position[0] - _blue_locations[i][0])
        b = abs(position[1] - _blue_locations[i][1])
        if (a + b) == 0:
            blue_healths[i] -= 29
        elif (a + b) == 1:
            blue_healths[i] -= 14
        elif (a + b) == 2:
            if (position[0] + 1, position[1] + 1) == (_blue_locations[i][0], _blue_locations[i][1]):
                blue_healths[i] -= 7
            elif (position[0] + 1, position[1] - 1) == (_blue_locations[i][0], _blue_locations[i][1]):
                blue_healths[i] -= 7
            elif (position[0] - 1, position[1] - 1) == (_blue_locations[i][0], _blue_locations[i][1]):
                blue_healths[i] -= 7
            elif (position[0] - 1, position[1] + 1) == (_blue_locations[i][0], _blue_locations[i][1]):
                blue_healths[i] -= 7


def check_circle(position, color, _red_locations, _blue_locations):
    moves_list = []
    dxdy_list = []

    if (position[0], position[1] + 1) not in _red_locations and \
            (position[0], position[1] + 1) not in _blue_locations and position[1] < 9:
        moves_list.append((position[0], position[1] + 1))
        dxdy_list.append((0, 1))

    if (position[0], position[1] + 2) not in _red_locations and \
            (position[0], position[1] + 2) not in _blue_locations and position[1] < 8:
        moves_list.append((position[0], position[1] + 2))
        dxdy_list.append((0, 2))

    if (position[0] + 1, position[1]) not in _red_locations and \
            (position[0] + 1, position[1]) not in _blue_locations and position[0] < 9:
        moves_list.append((position[0] + 1, position[1]))
        dxdy_list.append((1, 0))

    if (position[0] + 2, position[1]) not in _red_locations and \
            (position[0] + 2, position[1]) not in _blue_locations and position[0] < 8:
        moves_list.append((position[0] + 2, position[1]))
        dxdy_list.append((2, 0))

    if (position[0], position[1] - 1) not in _red_locations and \
            (position[0], position[1] - 1) not in _blue_locations and position[1] > 0:
        moves_list.append((position[0], position[1] - 1))
        dxdy_list.append((0, -1))

    if (position[0], position[1] - 2) not in _red_locations and \
            (position[0], position[1] - 2) not in _blue_locations and position[1] > 1:
        moves_list.append((position[0], position[1] - 2))
        dxdy_list.append((0, -2))

    if (position[0] - 1, position[1]) not in _red_locations and \
            (position[0] - 1, position[1]) not in _blue_locations and position[0] > 0:
        moves_list.append((position[0] - 1, position[1]))
        dxdy_list.append((-1, 0))

    if (position[0] - 2, position[1]) not in _red_locations and \
            (position[0] - 2, position[1]) not in _blue_locations and position[0] > 1:
        moves_list.append((position[0] - 2, position[1]))
        dxdy_list.append((-2, 0))

    return moves_list


def check_square(position, color, _red_locations, _blue_locations):
    moves_list = []
    dxdy_list = []

    if (position[0] + 1, position[1] + 1) not in _red_locations and \
            (position[0] + 1, position[1] + 1) not in _blue_locations and position[0] < 9 and position[1] < 9:
        moves_list.append((position[0] + 1, position[1] + 1))
        dxdy_list.append((1, 1))

    if (position[0] + 2, position[1] + 2) not in _red_locations and \
            (position[0] + 2, position[1] + 2) not in _blue_locations and position[0] < 8 and position[1] < 8:
        moves_list.append((position[0] + 2, position[1] + 2))
        dxdy_list.append((2, 2))

    if (position[0] + 1, position[1] - 1) not in _red_locations and \
            (position[0] + 1, position[1] - 1) not in _blue_locations and position[0] < 9 and position[1] > 0:
        moves_list.append((position[0] + 1, position[1] - 1))
        dxdy_list.append((1, -1))

    if (position[0] + 2, position[1] - 2) not in _red_locations and \
            (position[0] + 2, position[1] - 2) not in _blue_locations and position[0] < 8 and position[1] > 1:
        moves_list.append((position[0] + 2, position[1] - 2))
        dxdy_list.append((2, -2))

    if (position[0] - 1, position[1] + 1) not in _red_locations and \
            (position[0] - 1, position[1] + 1) not in _blue_locations and position[0] > 0 and position[1] < 9:
        moves_list.append((position[0] - 1, position[1] + 1))
        dxdy_list.append((-1, 1))

    if (position[0] - 2, position[1] + 2) not in _red_locations and \
            (position[0] - 2, position[1] + 2) not in _blue_locations and position[0] > 1 and position[1] < 8:
        moves_list.append((position[0] - 2, position[1] + 2))
        dxdy_list.append((-2, +2))

    if (position[0] - 1, position[1] - 1) not in _red_locations and \
            (position[0] - 1, position[1] - 1) not in _blue_locations and position[0] > 0 and position[1] > 0:
        moves_list.append((position[0] - 1, position[1] - 1))
        dxdy_list.append((-1, -1))

    if (position[0] - 2, position[1] - 2) not in _red_locations and \
            (position[0] - 2, position[1] - 2) not in _blue_locations and position[0] > 1 and position[1] > 1:
        moves_list.append((position[0] - 2, position[1] - 2))
        dxdy_list.append((-2, -2))

    return moves_list


def check_triangle(position, color, _red_locations, _blue_locations):
    moves_list = []
    dxdy_list = []
    # if color == 'red':
    if (position[0] + 1, position[1]) not in _red_locations and \
            (position[0] + 1, position[1]) not in _blue_locations and position[0] < 9:
        moves_list.append((position[0] + 1, position[1]))
        dxdy_list.append((1, 0))

    if (position[0] + 1, position[1] + 1) not in _red_locations and \
            (position[0] + 1, position[1] + 1) not in _blue_locations and position[0] < 9 and position[1] < 9:
        moves_list.append((position[0] + 1, position[1] + 1))
        dxdy_list.append((1, 1))

    if (position[0], position[1] + 1) not in _red_locations and \
            (position[0], position[1] + 1) not in _blue_locations and position[1] < 9:
        moves_list.append((position[0], position[1] + 1))
        dxdy_list.append((0, 1))

    if (position[0] - 1, position[1] + 1) not in _red_locations and \
            (position[0] - 1, position[1] + 1) not in _blue_locations and position[0] > 0 and position[1] < 9:
        moves_list.append((position[0] - 1, position[1] + 1))
        dxdy_list.append((-1, 1))

    if (position[0] - 1, position[1]) not in _red_locations and \
            (position[0] - 1, position[1]) not in _blue_locations and position[0] > 0:
        moves_list.append((position[0] - 1, position[1]))
        dxdy_list.append((-1, 0))

    if (position[0] - 1, position[1] - 1) not in _red_locations and \
            (position[0] - 1, position[1] - 1) not in _blue_locations and position[0] > 0 and position[1] > 0:
        moves_list.append((position[0] - 1, position[1] - 1))
        dxdy_list.append((-1, -1))

    if (position[0], position[1] - 1) not in _red_locations and \
            (position[0], position[1] - 1) not in _blue_locations and position[1] > 0:
        moves_list.append((position[0], position[1] - 1))
        dxdy_list.append((0, -1))

    if (position[0] + 1, position[1] - 1) not in _red_locations and \
            (position[0] + 1, position[1] - 1) not in _blue_locations and position[0] < 9 and position[1] > 0:
        moves_list.append((position[0] + 1, position[1] - 1))
        dxdy_list.append((1, -1))

    return moves_list


def check_valid_moves(_red_options, _blue_options, _selection):
    if turn_step < 3:
        option_list = _red_options
    else:
        option_list = _blue_options
    valid_options = option_list[_selection]
    return valid_options


def check_valid_shoot(_red_locations, _blue_locations, _selection):
    if turn_step < 3:
        option_list = check_shoot(red_guns, _red_locations, 'red')
    else:
        option_list = check_shoot(blue_guns, _blue_locations, 'blue')
    valid_options = option_list[_selection]
    return valid_options



def check_healths():
    global game_over, winner
    #print(red_healths)
    #print(blue_healths)

    for i in range(len(red_pieces)):
        if i in dead_red:
            continue
        if red_healths[i] <= 0:
            captured_pieces_red.append(red_pieces[i])
            #red_pieces.pop(i)
            #red_locations.pop(i)
            #red_healths.pop(i)
            print("read dead")
            death_sfx.play()
            dead_red.append(i)

    for i in range(len(blue_pieces)):
        if i in dead_blue:
            continue
        if blue_healths[i] <= 0:
            captured_pieces_blue.append(blue_pieces[i])
            #blue_pieces.pop(i)
            #blue_locations.pop(i)
            #blue_healths.pop(i)
            print("blue dead")
            death_sfx.play()
            dead_blue.append(i)
    
    # Check if all pieces of one team are dead
    if len(dead_red) == len(red_pieces):
        game_over = True
        winner = "Blue"
        print("Blue Team Wins!")
    elif len(dead_blue) == len(blue_pieces):
        game_over = True
        winner = "Red"
        print("Red Team Wins!")


def check_stalemate():
    """Check if both teams have no valid actions (stalemate)"""
    global game_over, winner, consecutive_no_actions
    
    # Check if red has any valid actions
    red_state = GameState(red_locations, blue_locations, red_healths, blue_healths, dead_red, dead_blue)
    red_actions = get_all_possible_actions(red_state, is_red_turn=True)
    
    # Check if blue has any valid actions
    blue_state = GameState(red_locations, blue_locations, red_healths, blue_healths, dead_red, dead_blue)
    blue_actions = get_all_possible_actions(blue_state, is_red_turn=False)
    
    # If neither team has valid actions, it's a stalemate
    if not red_actions and not blue_actions:
        game_over = True
        # Determine winner based on total health or piece count
        red_total_health = sum(h for i, h in enumerate(red_healths) if i not in dead_red)
        blue_total_health = sum(h for i, h in enumerate(blue_healths) if i not in dead_blue)
        red_alive = len([i for i in range(len(red_pieces)) if i not in dead_red])
        blue_alive = len([i for i in range(len(blue_pieces)) if i not in dead_blue])
        
        if red_alive > blue_alive:
            winner = "Red"
        elif blue_alive > red_alive:
            winner = "Blue"
        elif red_total_health > blue_total_health:
            winner = "Red"
        elif blue_total_health > red_total_health:
            winner = "Blue"
        else:
            winner = "Draw"
        
        print(f"Stalemate! Winner: {winner}")
        return True
    
    return False


def draw_valid(moves):
    """Draw valid move positions with enhanced visuals"""
    if turn_step < 3:
        color = (255, 150, 150)
        outer_color = (255, 100, 100)
    else:
        color = (150, 200, 255)
        outer_color = (100, 150, 255)
    
    for i in range(len(moves)):
        # Pulsing effect - outer circle
        pygame.draw.circle(screen, outer_color + (80,) if len(outer_color) == 3 else outer_color, 
                          (moves[i][0] * 80 + 40, moves[i][1] * 80 + 40), 12)
        # Inner circle
        pygame.draw.circle(screen, color, (moves[i][0] * 80 + 40, moves[i][1] * 80 + 40), 8)
        # Center dot
        pygame.draw.circle(screen, (255, 255, 255), (moves[i][0] * 80 + 40, moves[i][1] * 80 + 40), 3)


def draw_valid_shoot(moves):
    """Draw valid shoot positions with crosshair"""
    if turn_step < 3:
        color = (255, 100, 100)
    else:
        color = (100, 150, 255)
    
    for i in range(len(moves)):
        center_x = moves[i][0] * 80 + 40
        center_y = moves[i][1] * 80 + 40
        
        # Crosshair
        pygame.draw.circle(screen, (200, 200, 200), (center_x, center_y), 15, 2)
        pygame.draw.line(screen, color, (center_x - 10, center_y), (center_x + 10, center_y), 3)
        pygame.draw.line(screen, color, (center_x, center_y - 10), (center_x, center_y + 10), 3)
        # Center dot
        pygame.draw.circle(screen, color, (center_x, center_y), 4)


def draw_game_over_popup():
    """Draw enhanced game over popup with winner and buttons"""
    # Semi-transparent overlay with gradient
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)
    overlay.fill((20, 20, 30))
    screen.blit(overlay, (0, 0))
    
    # Popup box with shadow
    popup_width = 450
    popup_height = 320
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2
    
    # Draw shadow
    shadow_surface = pygame.Surface((popup_width + 10, popup_height + 10), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surface, (0, 0, 0, 100), [0, 0, popup_width + 10, popup_height + 10], border_radius=20)
    screen.blit(shadow_surface, (popup_x - 5, popup_y - 5))
    
    # Main popup box with gradient effect
    pygame.draw.rect(screen, (45, 45, 60), [popup_x, popup_y, popup_width, popup_height], border_radius=15)
    pygame.draw.rect(screen, (100, 100, 120), [popup_x, popup_y, popup_width, popup_height], 4, border_radius=15)
    
    # Trophy/Star decoration at top
    trophy_y = popup_y + 30
    if winner == "Red":
        pygame.draw.circle(screen, (255, 200, 100), (WIDTH // 2, trophy_y), 35)
        pygame.draw.circle(screen, (255, 220, 120), (WIDTH // 2, trophy_y), 30)
        # Inner star effect
        for angle in range(0, 360, 72):
            import math
            x = WIDTH // 2 + int(20 * math.cos(math.radians(angle)))
            y = trophy_y + int(20 * math.sin(math.radians(angle)))
            pygame.draw.circle(screen, (255, 100, 100), (x, y), 8)
    elif winner == "Blue":
        pygame.draw.circle(screen, (100, 180, 255), (WIDTH // 2, trophy_y), 35)
        pygame.draw.circle(screen, (120, 200, 255), (WIDTH // 2, trophy_y), 30)
        # Inner star effect
        for angle in range(0, 360, 72):
            import math
            x = WIDTH // 2 + int(20 * math.cos(math.radians(angle)))
            y = trophy_y + int(20 * math.sin(math.radians(angle)))
            pygame.draw.circle(screen, (50, 100, 255), (x, y), 8)
    else:  # Draw
        pygame.draw.circle(screen, (150, 150, 150), (WIDTH // 2, trophy_y), 35)
        pygame.draw.circle(screen, (180, 180, 180), (WIDTH // 2, trophy_y), 30)
    
    # Winner text with shadow
    winner_font = pygame.font.Font("freesansbold.ttf", 42)
    if winner == "Red":
        # Text shadow
        shadow_text = winner_font.render("Red Team Wins!", True, (100, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(WIDTH // 2 + 2, popup_y + 120 + 2))
        screen.blit(shadow_text, shadow_rect)
        # Main text
        winner_text = winner_font.render("Red Team Wins!", True, (255, 120, 120))
    elif winner == "Blue":
        # Text shadow
        shadow_text = winner_font.render("Blue Team Wins!", True, (0, 50, 100))
        shadow_rect = shadow_text.get_rect(center=(WIDTH // 2 + 2, popup_y + 120 + 2))
        screen.blit(shadow_text, shadow_rect)
        # Main text
        winner_text = winner_font.render("Blue Team Wins!", True, (120, 180, 255))
    else:  # Draw
        # Text shadow
        shadow_text = winner_font.render("It's a Draw!", True, (50, 50, 50))
        shadow_rect = shadow_text.get_rect(center=(WIDTH // 2 + 2, popup_y + 120 + 2))
        screen.blit(shadow_text, shadow_rect)
        # Main text
        winner_text = winner_font.render("It's a Draw!", True, (200, 200, 200))
    
    text_rect = winner_text.get_rect(center=(WIDTH // 2, popup_y + 120))
    screen.blit(winner_text, text_rect)
    
    # Enhanced Reset button with gradient
    reset_button_rect = pygame.Rect(popup_x + 60, popup_y + 210, 150, 60)
    pygame.draw.rect(screen, (80, 180, 80), reset_button_rect, border_radius=10)
    pygame.draw.rect(screen, (120, 220, 120), [reset_button_rect.x + 2, reset_button_rect.y + 2, reset_button_rect.width - 4, 28], border_radius=8)
    pygame.draw.rect(screen, (200, 255, 200), reset_button_rect, 3, border_radius=10)
    reset_text = pygame.font.Font("freesansbold.ttf", 24).render("Reset", True, (255, 255, 255))
    reset_text_rect = reset_text.get_rect(center=reset_button_rect.center)
    screen.blit(reset_text, reset_text_rect)
    
    # Enhanced Exit button with gradient
    exit_button_rect = pygame.Rect(popup_x + 240, popup_y + 210, 150, 60)
    pygame.draw.rect(screen, (180, 80, 80), exit_button_rect, border_radius=10)
    pygame.draw.rect(screen, (220, 120, 120), [exit_button_rect.x + 2, exit_button_rect.y + 2, exit_button_rect.width - 4, 28], border_radius=8)
    pygame.draw.rect(screen, (255, 200, 200), exit_button_rect, 3, border_radius=10)
    exit_text = pygame.font.Font("freesansbold.ttf", 24).render("Exit", True, (255, 255, 255))
    exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
    screen.blit(exit_text, exit_text_rect)
    
    return reset_button_rect, exit_button_rect


def reset_game():
    """Reset all game variables to initial state"""
    global red_pieces, red_guns, red_locations, red_healths, captured_pieces_red
    global blue_pieces, blue_guns, blue_locations, blue_healths, captured_pieces_blue
    global turn_step, selection, valid_moves, valid_shoot
    global health_pickup_exist, health_pickup_location, dead_red, dead_blue
    global game_over, winner, red_options, blue_options, consecutive_no_actions
    
    # Reset red team
    red_pieces = ['circle', 'square', 'triangle', 'square', 'circle']
    red_guns = ['short_gun', 'long_gun', 'blast_gun', 'long_gun', 'short_gun']
    red_locations = [(2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]  # Centered at top
    red_healths = [30, 30, 30, 30, 30]
    captured_pieces_red = []
    
    # Reset blue team
    blue_pieces = ['circle', 'square', 'triangle', 'square', 'circle']
    blue_guns = ['short_gun', 'long_gun', 'blast_gun', 'long_gun', 'short_gun']
    blue_locations = [(3, 9), (4, 9), (5, 9), (6, 9), (7, 9)]  # Centered at bottom
    blue_healths = [30, 30, 30, 30, 30]
    captured_pieces_blue = []
    
    # Reset game state
    # Randomly choose who goes first for fairness
    turn_step = random.choice([0, 3])  # 0 = Red starts, 3 = Blue starts
    selection = 100
    valid_moves = []
    valid_shoot = []
    health_pickup_exist = 0
    health_pickup_location = []
    dead_red = []
    dead_blue = []
    game_over = False
    winner = None
    consecutive_no_actions = 0
    
    # Recalculate options
    red_options = check_option(red_pieces, red_locations, 'red')
    blue_options = check_option(blue_pieces, blue_locations, 'blue')


# ========== AI IMPLEMENTATION WITH MINIMAX AND ALPHA-BETA PRUNING ==========

class GameState:
    """Represents a game state for Minimax search"""
    def __init__(self, red_locs, blue_locs, red_hp, blue_hp, dead_r, dead_b):
        self.red_locations = [loc for loc in red_locs]
        self.blue_locations = [loc for loc in blue_locs]
        self.red_healths = [hp for hp in red_hp]
        self.blue_healths = [hp for hp in blue_hp]
        self.dead_red = [d for d in dead_r]
        self.dead_blue = [d for d in dead_b]
    
    def copy(self):
        return GameState(self.red_locations, self.blue_locations, 
                        self.red_healths, self.blue_healths,
                        self.dead_red, self.dead_blue)
    
    def is_terminal(self):
        """Check if game is over (all pieces of one team dead)"""
        all_red_dead = len(self.dead_red) == len(red_pieces)
        all_blue_dead = len(self.dead_blue) == len(blue_pieces)
        return all_red_dead or all_blue_dead


def simulate_move_and_shoot(state, is_red_turn, piece_idx, new_location, shoot_target):
    """
    Simulate a move+shoot action and return the resulting state.
    Returns new GameState after the action.
    Validates bounds to prevent out-of-board positions.
    """
    # Validate inputs are within board bounds
    if not (0 <= new_location[0] <= 9 and 0 <= new_location[1] <= 9):
        return state  # Return unchanged state if invalid move
    if not (0 <= shoot_target[0] <= 9 and 0 <= shoot_target[1] <= 9):
        return state  # Return unchanged state if invalid shoot
    
    new_state = state.copy()
    
    if is_red_turn:
        # Move the piece
        new_state.red_locations[piece_idx] = new_location
        
        # Apply shooting damage
        gun_type = red_guns[piece_idx]
        
        if gun_type == 'blast_gun':
            # Apply blast damage
            for i in range(len(blue_pieces)):
                if i in new_state.dead_blue:
                    continue
                a = abs(shoot_target[0] - new_state.blue_locations[i][0])
                b = abs(shoot_target[1] - new_state.blue_locations[i][1])
                if a + b == 0:
                    new_state.blue_healths[i] -= 29
                elif (a + b) == 1:
                    new_state.blue_healths[i] -= 14
                elif (a + b) == 2:
                    if (shoot_target[0] + 1, shoot_target[1] + 1) == (new_state.blue_locations[i][0], new_state.blue_locations[i][1]):
                        new_state.blue_healths[i] -= 7
                    elif (shoot_target[0] + 1, shoot_target[1] - 1) == (new_state.blue_locations[i][0], new_state.blue_locations[i][1]):
                        new_state.blue_healths[i] -= 7
                    elif (shoot_target[0] - 1, shoot_target[1] - 1) == (new_state.blue_locations[i][0], new_state.blue_locations[i][1]):
                        new_state.blue_healths[i] -= 7
                    elif (shoot_target[0] - 1, shoot_target[1] + 1) == (new_state.blue_locations[i][0], new_state.blue_locations[i][1]):
                        new_state.blue_healths[i] -= 7
            
            # Blast also damages red pieces (friendly fire)
            for i in range(len(red_pieces)):
                if i in new_state.dead_red:
                    continue
                a = abs(shoot_target[0] - new_state.red_locations[i][0])
                b = abs(shoot_target[1] - new_state.red_locations[i][1])
                if a + b == 0:
                    new_state.red_healths[i] -= 29
                elif (a + b) == 1:
                    new_state.red_healths[i] -= 14
                elif (a + b) == 2:
                    if (shoot_target[0] + 1, shoot_target[1] + 1) == (new_state.red_locations[i][0], new_state.red_locations[i][1]):
                        new_state.red_healths[i] -= 7
                    elif (shoot_target[0] + 1, shoot_target[1] - 1) == (new_state.red_locations[i][0], new_state.red_locations[i][1]):
                        new_state.red_healths[i] -= 7
                    elif (shoot_target[0] - 1, shoot_target[1] - 1) == (new_state.red_locations[i][0], new_state.red_locations[i][1]):
                        new_state.red_healths[i] -= 7
                    elif (shoot_target[0] - 1, shoot_target[1] + 1) == (new_state.red_locations[i][0], new_state.red_locations[i][1]):
                        new_state.red_healths[i] -= 7
        else:
            # Regular gun damage
            if shoot_target in new_state.blue_locations:
                blue_idx = new_state.blue_locations.index(shoot_target)
                if blue_idx not in new_state.dead_blue:
                    new_state.blue_healths[blue_idx] -= 10
    else:
        # Blue's turn
        new_state.blue_locations[piece_idx] = new_location
        
        gun_type = blue_guns[piece_idx]
        
        if gun_type == 'blast_gun':
            # Apply blast damage to red
            for i in range(len(red_pieces)):
                if i in new_state.dead_red:
                    continue
                a = abs(shoot_target[0] - new_state.red_locations[i][0])
                b = abs(shoot_target[1] - new_state.red_locations[i][1])
                if a + b == 0:
                    new_state.red_healths[i] -= 29
                elif (a + b) == 1:
                    new_state.red_healths[i] -= 14
                elif (a + b) == 2:
                    if (shoot_target[0] + 1, shoot_target[1] + 1) == (new_state.red_locations[i][0], new_state.red_locations[i][1]):
                        new_state.red_healths[i] -= 7
                    elif (shoot_target[0] + 1, shoot_target[1] - 1) == (new_state.red_locations[i][0], new_state.red_locations[i][1]):
                        new_state.red_healths[i] -= 7
                    elif (shoot_target[0] - 1, shoot_target[1] - 1) == (new_state.red_locations[i][0], new_state.red_locations[i][1]):
                        new_state.red_healths[i] -= 7
                    elif (shoot_target[0] - 1, shoot_target[1] + 1) == (new_state.red_locations[i][0], new_state.red_locations[i][1]):
                        new_state.red_healths[i] -= 7
            
            # Blast also damages blue pieces (friendly fire)
            for i in range(len(blue_pieces)):
                if i in new_state.dead_blue:
                    continue
                a = abs(shoot_target[0] - new_state.blue_locations[i][0])
                b = abs(shoot_target[1] - new_state.blue_locations[i][1])
                if a + b == 0:
                    new_state.blue_healths[i] -= 29
                elif (a + b) == 1:
                    new_state.blue_healths[i] -= 14
                elif (a + b) == 2:
                    if (shoot_target[0] + 1, shoot_target[1] + 1) == (new_state.blue_locations[i][0], new_state.blue_locations[i][1]):
                        new_state.blue_healths[i] -= 7
                    elif (shoot_target[0] + 1, shoot_target[1] - 1) == (new_state.blue_locations[i][0], new_state.blue_locations[i][1]):
                        new_state.blue_healths[i] -= 7
                    elif (shoot_target[0] - 1, shoot_target[1] - 1) == (new_state.blue_locations[i][0], new_state.blue_locations[i][1]):
                        new_state.blue_healths[i] -= 7
                    elif (shoot_target[0] - 1, shoot_target[1] + 1) == (new_state.blue_locations[i][0], new_state.blue_locations[i][1]):
                        new_state.blue_healths[i] -= 7
        else:
            # Regular gun damage
            if shoot_target in new_state.red_locations:
                red_idx = new_state.red_locations.index(shoot_target)
                if red_idx not in new_state.dead_red:
                    new_state.red_healths[red_idx] -= 10
    
    # Update dead pieces
    for i in range(len(red_pieces)):
        if i not in new_state.dead_red and new_state.red_healths[i] <= 0:
            new_state.dead_red.append(i)
    
    for i in range(len(blue_pieces)):
        if i not in new_state.dead_blue and new_state.blue_healths[i] <= 0:
            new_state.dead_blue.append(i)
    
    return new_state


def heuristic_aggressive(state, is_red_player):
    """
    Improved Aggressive heuristic (for Red AI):
    - Maximize damage to enemies
    - Prioritize killing low-health enemies
    - Consider board positioning
    - Evaluate threats to own pieces
    """
    if is_red_player:
        # Red perspective
        own_health = sum(h for i, h in enumerate(state.red_healths) if i not in state.dead_red)
        enemy_health = sum(h for i, h in enumerate(state.blue_healths) if i not in state.dead_blue)
        own_alive = len([i for i in range(len(red_pieces)) if i not in state.dead_red])
        enemy_alive = len([i for i in range(len(blue_pieces)) if i not in state.dead_blue])
        
        # Piece count advantage - BALANCED WEIGHTS
        piece_advantage = (own_alive - enemy_alive) * 1000
        
        # Health advantage (negative enemy health is good) - BALANCED WEIGHTS
        health_advantage = -enemy_health * 15 + own_health * 5
        
        # Bonus for low-health enemies (easier to kill) - BALANCED WEIGHTS
        low_health_bonus = sum(50 if 0 < h <= 15 else 0 for i, h in enumerate(state.blue_healths) if i not in state.dead_blue)
        
        # Positioning: pieces closer to enemy territory score higher
        position_score = 0
        # for i in range(len(red_pieces)):
        #     if i not in state.dead_red:
        #         # Reward advancing forward (higher y value)
        #         position_score += state.red_locations[i][1] * 2
        
        score = piece_advantage + health_advantage + low_health_bonus + position_score
    else:
        # Blue perspective - BALANCED WEIGHTS (same as Red)
        own_health = sum(h for i, h in enumerate(state.blue_healths) if i not in state.dead_blue)
        enemy_health = sum(h for i, h in enumerate(state.red_healths) if i not in state.dead_red)
        own_alive = len([i for i in range(len(blue_pieces)) if i not in state.dead_blue])
        enemy_alive = len([i for i in range(len(red_pieces)) if i not in state.dead_red])
        
        # Fixed: Use same balanced weights as Red for fair competition
        piece_advantage = (own_alive - enemy_alive) * 1000
        health_advantage = -enemy_health * 15 + own_health * 5
        low_health_bonus = sum(50 if 0 < h <= 15 else 0 for i, h in enumerate(state.red_healths) if i not in state.dead_red)
        
        position_score = 0
        # for i in range(len(blue_pieces)):
        #     if i not in state.dead_blue:
        #         # Reward advancing forward (lower y value)
        #         position_score += (9 - state.blue_locations[i][1]) * 2
        
        score = piece_advantage + health_advantage + low_health_bonus + position_score
    
    return score


def heuristic_defensive(state, is_red_player):
    """
    Improved Defensive heuristic (for Blue AI):
    - Prioritize own survival and health
    - Maintain defensive positions
    - Secondary goal: opportunistic damage
    - Avoid risky moves
    """
    
    if is_red_player:
        own_health = sum(h for i, h in enumerate(state.red_healths) if i not in state.dead_red)
        enemy_health = sum(h for i, h in enumerate(state.blue_healths) if i not in state.dead_blue)
        own_alive = len([i for i in range(len(red_pieces)) if i not in state.dead_red])
        enemy_alive = len([i for i in range(len(blue_pieces)) if i not in state.dead_blue])
        
        # Balanced weights - same scale as aggressive
        piece_advantage = (own_alive - enemy_alive) * 500
        health_advantage = -enemy_health * 100 + own_health * 5
        low_health_bonus = sum(50 if 0 < h <= 15 else 0 for i, h in enumerate(state.blue_healths) if i not in state.dead_blue)
        
        position_score = 0
        
        score = piece_advantage + health_advantage + low_health_bonus + position_score
    else:
        # Blue perspective - BALANCED WEIGHTS (same as Red)
        own_health = sum(h for i, h in enumerate(state.blue_healths) if i not in state.dead_blue)
        enemy_health = sum(h for i, h in enumerate(state.red_healths) if i not in state.dead_red)
        own_alive = len([i for i in range(len(blue_pieces)) if i not in state.dead_blue])
        enemy_alive = len([i for i in range(len(red_pieces)) if i not in state.dead_red])
        
        # Balanced weights - same scale as aggressive
        piece_advantage = (own_alive - enemy_alive) * 500
        health_advantage = -enemy_health * 100 + own_health * 5
        low_health_bonus = sum(50 if 0 < h <= 15 else 0 for i, h in enumerate(state.red_healths) if i not in state.dead_red)
        
        position_score = 0
        
        score = piece_advantage + health_advantage + low_health_bonus + position_score
    
    return score


def get_all_possible_actions(state, is_red_turn):
    """
    Generate all possible (piece_index, move_location, shoot_target) actions for current player.
    Validates all moves and shoots are within board bounds.
    """
    possible_actions = []
    
    if is_red_turn:
        pieces_to_check = [(i, red_pieces[i], state.red_locations[i]) for i in range(len(red_pieces)) if i not in state.dead_red]
        all_move_options = check_option(red_pieces, state.red_locations, 'red', state.red_locations, state.blue_locations)
        
        for piece_idx, piece_type, piece_loc in pieces_to_check:
            valid_moves = all_move_options[piece_idx]
            
            if not valid_moves:
                continue
            
            for move_loc in valid_moves:
                # Validate move is within bounds
                if not (0 <= move_loc[0] <= 9 and 0 <= move_loc[1] <= 9):
                    continue
                    
                # Calculate shoot options from new position   - [red_guns[piece_idx]]=['short_gun']  [move_loc]=(x,y)
                shoot_options = check_shoot([red_guns[piece_idx]], [move_loc], 'red', state.red_locations, state.blue_locations)[0]
                
                if not shoot_options:
                    continue
                
                for shoot_target in shoot_options:
                    # Validate shoot target is within bounds
                    if not (0 <= shoot_target[0] <= 9 and 0 <= shoot_target[1] <= 9):
                        continue
                    possible_actions.append((piece_idx, move_loc, shoot_target))
    else:
        pieces_to_check = [(i, blue_pieces[i], state.blue_locations[i]) for i in range(len(blue_pieces)) if i not in state.dead_blue]
        all_move_options = check_option(blue_pieces, state.blue_locations, 'blue', state.blue_locations, state.red_locations)
        
        for piece_idx, piece_type, piece_loc in pieces_to_check:
            valid_moves = all_move_options[piece_idx]
            
            if not valid_moves:
                continue
            
            for move_loc in valid_moves:
                # Validate move is within bounds
                if not (0 <= move_loc[0] <= 9 and 0 <= move_loc[1] <= 9):
                    continue
                    
                shoot_options = check_shoot([blue_guns[piece_idx]], [move_loc], 'blue', state.blue_locations, state.red_locations)[0]
                
                if not shoot_options:
                    continue
                
                for shoot_target in shoot_options:
                    # Validate shoot target is within bounds
                    if not (0 <= shoot_target[0] <= 9 and 0 <= shoot_target[1] <= 9):
                        continue
                    possible_actions.append((piece_idx, move_loc, shoot_target))
    
    return possible_actions


def minimax_alpha_beta(state, depth, alpha, beta, is_maximizing, is_red_player, heuristic_func):
    """
    Minimax algorithm with Alpha-Beta pruning.
    
    Args:
        state: Current game state
        depth: Remaining search depth
        alpha: Alpha value for pruning
        beta: Beta value for pruning
        is_maximizing: True if maximizing player's turn
        is_red_player: True if evaluating from Red's perspective
        heuristic_func: Heuristic function to use
    
    Returns:
        Best score for current player
    """
    # Terminal conditions
    if depth == 0 or state.is_terminal():
        return heuristic_func(state, is_red_player)
    
    # Get all possible actions for current turn
    possible_actions = get_all_possible_actions(state, is_maximizing == is_red_player)
    
    # If no actions available, return heuristic
    if not possible_actions:
        return heuristic_func(state, is_red_player)
    
    if is_maximizing:
        max_eval = float('-inf')
        for action in possible_actions:
            piece_idx, move_loc, shoot_target = action
            # Simulate the action
            new_state = simulate_move_and_shoot(state, is_maximizing == is_red_player, piece_idx, move_loc, shoot_target)
            # Recursive call
            eval_score = minimax_alpha_beta(new_state, depth - 1, alpha, beta, False, is_red_player, heuristic_func)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval
    else:
        min_eval = float('inf')
        for action in possible_actions:
            piece_idx, move_loc, shoot_target = action
            # Simulate the action
            new_state = simulate_move_and_shoot(state, is_maximizing == is_red_player, piece_idx, move_loc, shoot_target)
            # Recursive call
            eval_score = minimax_alpha_beta(new_state, depth - 1, alpha, beta, True, is_red_player, heuristic_func)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval


def ai_decide_action_minimax(is_red_turn):
    """
    Use Minimax with Alpha-Beta pruning to find the best move+shoot combination.
    Red AI uses aggressive heuristic, Blue AI uses defensive heuristic.
    
    Returns: (piece_index, move_location, shoot_target) or None
    """
    current_state = GameState(red_locations, blue_locations, red_healths, blue_healths, dead_red, dead_blue)
    
    # Choose heuristic based on player
    if is_red_turn:
        heuristic_func = heuristic_aggressive
    else:
        heuristic_func = heuristic_defensive
    
    # Get all possible actions
    possible_actions = get_all_possible_actions(current_state, is_red_turn)
    
    if not possible_actions:
        return None
    
    # Shuffle actions to add variety (different pieces can start each turn)
    random.shuffle(possible_actions)
    
    # Find best action using Minimax with Alpha-Beta pruning
    best_action = None
    best_score = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    
    for action in possible_actions:
        piece_idx, move_loc, shoot_target = action
        
        # Simulate the action
        resulting_state = simulate_move_and_shoot(current_state, is_red_turn, piece_idx, move_loc, shoot_target)
        
        
        # Evaluate with Minimax (opponent's turn next, so minimizing)
        score = minimax_alpha_beta(resulting_state, MINIMAX_DEPTH - 1, alpha, beta, False, is_red_turn, heuristic_func)
        
        if score > best_score:
            best_score = score
            best_action = action
            alpha = max(alpha, score)
    
    return best_action


# Initialize Pygame
pygame.init()
# Load the background music
pygame.mixer.music.load('res/Sounds/background_music.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

# game loop
red_options = check_option(red_pieces, red_locations, 'red')
blue_options = check_option(blue_pieces, blue_locations, 'blue')
run = True
last_ai_move_time = 0
ai_action = None
ai_piece_selected = None
ai_move_location = None
ai_shoot_target = None

while run:
    timer.tick(fps)
    screen.fill((50, 55, 65))  # Better background color
    check_healths()
    
    # Check for stalemate after checking healths
    if not game_over:
        check_stalemate()
    
    draw_board()
    draw_piece()
    draw_ui_info()  # Draw UI panel

    if selection != 100:
        if turn_step == 1 or turn_step == 4:
            valid_moves = check_valid_moves(red_options, blue_options, selection)
            draw_valid(valid_moves)
        elif turn_step == 2 or turn_step == 5:
            valid_shoot = check_valid_shoot(red_locations, blue_locations, selection)
            draw_valid_shoot(valid_shoot)

    # Draw game over popup if game ended
    reset_btn = None
    exit_btn = None
    if game_over:
        reset_btn, exit_btn = draw_game_over_popup()

    # AI Logic
    if AI_ENABLED and not game_over:
        current_time = time.time()
        
        # Check if it's time for AI to make a decision
        if current_time - last_ai_move_time >= AI_DELAY:
            # Red AI's turn
            if turn_step == 0:
                # Red AI decides on action
                ai_action = ai_decide_action_minimax(is_red_turn=True)
                if ai_action:
                    ai_piece_selected, ai_move_location, ai_shoot_target = ai_action
                    selection = ai_piece_selected
                    turn_step = 1
                    piece_place_sfx.play()
                    consecutive_no_actions = 0  # Reset counter on valid action
                else:
                    # No valid moves, skip turn
                    consecutive_no_actions += 1
                    turn_step = 3
                    selection = 100
                    print(f"Red has no valid actions. Consecutive no-actions: {consecutive_no_actions}")
                last_ai_move_time = current_time
                    
            elif turn_step == 1:
                # Execute the move
                # Safety check
                if ai_action and 0 <= selection < len(red_pieces) and selection not in dead_red:
                    # Validate move location is within bounds 
                    if 0 <= ai_move_location[0] <= 9 and 0 <= ai_move_location[1] <= 9:
                        red_locations[selection] = ai_move_location
                        turn_step = 2
                        reload_sfx.play()
                    else:
                        consecutive_no_actions += 1
                        turn_step = 3  # Skip if invalid
                else:
                    consecutive_no_actions += 1
                    turn_step = 3
                last_ai_move_time = current_time
                
            elif turn_step == 2:
                # Execute the shoot
                if ai_action and 0 <= selection < len(red_pieces) and selection not in dead_red:
                    # Validate shoot target is within bounds
                    if 0 <= ai_shoot_target[0] <= 9 and 0 <= ai_shoot_target[1] <= 9:
                        fire_sfx.play()
                        print(f"[DEBUG] Red piece {selection} shooting at {ai_shoot_target}")
                        if selection == 2:  # Blast gun
                            print(f"[DEBUG] Blast gun damage at {ai_shoot_target}")
                            blast_damage(ai_shoot_target, red_locations, blue_locations)
                        elif ai_shoot_target in blue_locations:
                            x = blue_locations.index(ai_shoot_target)
                            if x not in dead_blue:
                                print(f"[DEBUG] Red hit Blue piece {x} at {ai_shoot_target}. Health: {blue_healths[x]} -> {blue_healths[x]-10}")
                                blue_healths[x] -= 10
                                if blue_healths[x] <= 0:
                                    captured_pieces_blue.append(blue_pieces[x])
                                    if x not in dead_blue:
                                        dead_blue.append(x)
                                        print(f"[DEBUG] Blue piece {x} died!")
                        else:
                            print(f"[DEBUG] Red missed - target {ai_shoot_target} not occupied by Blue")
                        
                        spawn_health_pickup(health_pickup_exist)
                        red_options = check_option(red_pieces, red_locations, 'red')
                        blue_options = check_option(blue_pieces, blue_locations, 'blue')
                
                turn_step = 3
                selection = 100
                valid_moves = []
                valid_shoot = []
                ai_action = None
                last_ai_move_time = current_time
            
            # Blue AI's turn
            elif turn_step == 3:
                # Blue AI decides on action
                ai_action = ai_decide_action_minimax(is_red_turn=False)
                if ai_action:
                    ai_piece_selected, ai_move_location, ai_shoot_target = ai_action
                    selection = ai_piece_selected
                    turn_step = 4
                    piece_place_sfx.play()
                    consecutive_no_actions = 0  # Reset counter on valid action
                else:
                    # No valid moves, skip turn
                    consecutive_no_actions += 1
                    turn_step = 0
                    selection = 100
                    print(f"Blue has no valid actions. Consecutive no-actions: {consecutive_no_actions}")
                last_ai_move_time = current_time
                    
            elif turn_step == 4:
                # Execute the move
                if ai_action and 0 <= selection < len(blue_pieces) and selection not in dead_blue:
                    # Validate move location is within bounds
                    if 0 <= ai_move_location[0] <= 9 and 0 <= ai_move_location[1] <= 9:
                        blue_locations[selection] = ai_move_location
                        turn_step = 5
                        reload_sfx.play()
                    else:
                        consecutive_no_actions += 1
                        turn_step = 0  # Skip if invalid
                else:
                    consecutive_no_actions += 1
                    turn_step = 0
                last_ai_move_time = current_time
                
            elif turn_step == 5:
                # Execute the shoot
                if ai_action and 0 <= selection < len(blue_pieces) and selection not in dead_blue:
                    # Validate shoot target is within bounds
                    if 0 <= ai_shoot_target[0] <= 9 and 0 <= ai_shoot_target[1] <= 9:
                        fire_sfx.play()
                        print(f"[DEBUG] Blue piece {selection} shooting at {ai_shoot_target}")
                        if selection == 2:  # Blast gun
                            print(f"[DEBUG] Blast gun damage at {ai_shoot_target}")
                            blast_damage(ai_shoot_target, red_locations, blue_locations)
                        elif ai_shoot_target in red_locations:
                            y = red_locations.index(ai_shoot_target)
                            if y not in dead_red:
                                print(f"[DEBUG] Blue hit Red piece {y} at {ai_shoot_target}. Health: {red_healths[y]} -> {red_healths[y]-10}")
                                red_healths[y] -= 10
                                if red_healths[y] <= 0:
                                    captured_pieces_red.append(red_pieces[y])
                                    if y not in dead_red:
                                        dead_red.append(y)
                                        print(f"[DEBUG] Red piece {y} died!")
                        else:
                            print(f"[DEBUG] Blue missed - target {ai_shoot_target} not occupied by Red")
                        
                        spawn_health_pickup(health_pickup_exist)
                        red_options = check_option(red_pieces, red_locations, 'red')
                        blue_options = check_option(blue_pieces, blue_locations, 'blue')
                
                turn_step = 0
                selection = 100
                valid_moves = []
                valid_shoot = []
                ai_action = None
                last_ai_move_time = current_time
            
            # Check if we've had too many consecutive no-actions (stalemate)
            if consecutive_no_actions >= MAX_NO_ACTIONS:
                print("Too many consecutive no-actions, checking stalemate...")
                check_stalemate()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        # Handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            # Handle game over buttons
            if game_over:
                if reset_btn and reset_btn.collidepoint(mouse_pos):
                    reset_game()
                    reload_sfx.play()
                elif exit_btn and exit_btn.collidepoint(mouse_pos):
                    run = False

    pygame.display.flip()

pygame.quit()
