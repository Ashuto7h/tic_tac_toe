import pygame as pg
import sys
from pygame.locals import *
import time

# initialise global variables
XO = 'x'
winner = None
draw = False
width = 400
height = 400
black = (0, 0, 36)
line_color = (0, 255, 255)

# 3*3 board
TABLE = [[None] * 3, [None] * 3, [None] * 3]

# pygame window
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height+100), 0, 32)
pg.display.set_caption("Tic Tac Toe", "Ashuto7h")

# load image
opening_img = pg.image.load('Launch Text.png')
x_img = pg.image.load('X.png')
o_img = pg.image.load('O.png')

# resize image
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))
opening_img = pg.transform.scale(opening_img, (width, height))


# game start function
def game_start():
    screen.blit(opening_img, (0, 0))
    pg.display.update()
    time.sleep(3)
    screen.fill(black)

    # drawing lines
    pg.draw.line(screen, line_color, (int(width / 3), 0), (int(width / 3), height), 5)
    pg.draw.line(screen, line_color, (int(width / 3 * 2), 0), (int(width / 3 * 2), height), 5)
    pg.draw.line(screen, line_color, (0, int(height / 3)), (width, int(height / 3)), 5)
    pg.draw.line(screen, line_color, (0, int(height / 3 * 2)), (width, int(height / 3 * 2)), 5)
    draw_status()


def draw_status():
    global draw
    if winner is None:
        message = XO.upper() + "'s turn"
    else:
        message = winner.upper() + " won"
    if draw:
        message = 'Game Draw'
    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (0, 255, 255))

    # copy render message on board
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(int(width / 2), 500 - 50))
    screen.blit(text, text_rect)
    pg.display.update()


def user_click():
    x, y = pg.mouse.get_pos()
    if x < width / 3:
        col = 1
    elif x < width / 3 * 2:
        col = 2
    elif x < width:
        col = 3
    else:
        col = None

    if y < height / 3:
        row = 1
    elif y < height / 3 * 2:
        row = 2
    elif y < height:
        row = 3
    else:
        row = None
    print('row = ', row, 'col = ', col)
    if row and col and TABLE[row - 1][col - 1] is None:
        draw_x_o(row, col)
        check_win()


def check_win():
    global TABLE, winner, draw
    l_color = (250, 70, 70)
    for row in range(0, 3):
        # for rows
        if (TABLE[row][0] == TABLE[row][1] == TABLE[row][2]) and (TABLE[row][0] is not None):
            winner = TABLE[row][0]
            start = (0, int((row + 1) * height / 3 - height / 6))
            end = (width, int((row + 1) * height / 3 - height / 6))
            pg.draw.line(screen, l_color, start, end, 4)
            break

    for col in range(0, 3):
        if (TABLE[0][col] == TABLE[1][col] == TABLE[2][col]) and (TABLE[0][col] is not None):
            winner = TABLE[0][col]
            start = (int((col + 1) * width / 3 - width / 6), 0)
            end = (int((col + 1) * width / 3 - width / 6), height)
            pg.draw.line(screen, l_color, start, end, 4)
            break

    if (TABLE[0][0] == TABLE[1][1] == TABLE[2][2]) and (TABLE[0][0] is not None):
        winner = TABLE[0][0]
        pg.draw.line(screen, l_color, (50, 50), (350, 350), 4)

    if (TABLE[0][2] == TABLE[1][1] == TABLE[2][0]) and (TABLE[0][2] is not None):
        winner = TABLE[0][2]
        pg.draw.line(screen, l_color, (350, 50), (50, 350), 4)

    if all([all(row) for row in TABLE]) and winner is None:
        draw = True

    draw_status()


def draw_x_o(row, col):
    global TABLE, XO
    posx, posy = 0, 0
    if row == 1:
        posx = 30
    elif row == 2:
        posx = int(width / 3 + 30)
    elif row == 3:
        posx = int(width / 3 * 2 + 30)

    if col == 1:
        posy = 30
    elif col == 2:
        posy = int(height / 3 + 30)
    elif col == 3:
        posy = int(height / 3 * 2 + 30)

    TABLE[row - 1][col - 1] = XO
    if XO == 'x':
        screen.blit(x_img, (posy, posx))
        XO = 'o'
    else:
        screen.blit(o_img, (posy, posx))
        XO = 'x'
    pg.display.update()
    print('TABLE : ', TABLE)
    print('posx : ', posx, 'posy : ', posy)


def reset_game():
    global TABLE, winner, XO, draw
    time.sleep(3)
    XO = 'x'
    draw = False
    game_start()
    winner = None
    TABLE = [[None] * 3, [None] * 3, [None] * 3]


def game_open():
    game_start()
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type is MOUSEBUTTONUP:
                user_click()
                if winner or draw:
                    reset_game()

        pg.display.update()
        CLOCK.tick(fps)


game_open()
