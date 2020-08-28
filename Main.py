import pygame
import os
from Board import Board
from datetime import datetime


# Constants
WINDOW_STARTING_X_POS = 200
WINDOW_STARTING_Y_POS = 50

GAME_WIDTH = 960
GAME_HEIGHT = 960
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 960
DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)

FPS = 144
TRANSPARENT_ALPHA = 128

DEFAULT_TEXT_SIZE = 96
DEFAULT_TEXT_FONT = 'arial'

EASY_BUTTON = 40
MEDIUM_BUTTON = 39
HARD_BUTTON = 40
RESTART_BUTTON = 69

LEFT_CLICK = 1
RIGHT_CLICK = 3

# colors
WHITE = (200, 200, 200)
BLACK = (0, 0, 0)


# Returning the block size according to the difficulty chosen by the player
def get_block_size(difficulty):
    if difficulty == 'easy':
        return 120
    elif difficulty == 'medium':
        return 80
    else:
        return 60


def get_bomb_number(difficulty):
    if difficulty == 'easy':
        return 10
    elif difficulty == 'medium':
        return 25
    else:
        return 40


def draw_image(path, x, y):
    img = pygame.image.load(path)
    screen.blit(img, (x, y))


# Returns a tuple in the format of (x,y) describing the grid position according to the mouse position
def get_coordinates(mouse_position):
    x, y = mouse_position
    grid_x = x // block_size
    grid_y = y // block_size
    return grid_x, grid_y


def draw_grid():
    # Drawing the tiles
    for x in range(GAME_WIDTH // block_size):
        for y in range(GAME_HEIGHT // block_size):
            draw_image(f'media/{DIFFICULTY.lower()}/facingDown.png', x * block_size, y * block_size)


def draw_settings():
    for i in range(SCREEN_HEIGHT // block_size):
        rect = pygame.Rect(GAME_WIDTH, i * block_size, SCREEN_WIDTH - GAME_WIDTH, block_size)
        pygame.draw.rect(screen, WHITE, rect)
    draw_flag_counter()
    draw_time(get_current_time())
    draw_buttons()


def draw_time(time):
    text_font = pygame.font.SysFont('comic sans', 48)
    text = text_font.render(f'Time: {str(time)}', True, (250, 250, 250))
    screen.blit(text, (GAME_WIDTH, block_size))


def draw_flag_counter():
    text_font = pygame.font.SysFont('comic sans', 48)
    text = text_font.render(f'Flags: {str(flag_number)}', True, (250, 250, 250))
    screen.blit(text, (GAME_WIDTH, 0))


def draw_buttons():
    draw_image('media/buttons/easy.png', GAME_WIDTH, 240)
    draw_image('media/buttons/medium.png', GAME_WIDTH, 360)
    draw_image('media/buttons/hard.png', GAME_WIDTH, 480)
    draw_image('media/buttons/restart.png', GAME_WIDTH, 600)


def draw_revealed_on_zero():
    for i, row in enumerate(board.board):
        for j, cell in enumerate(row):
            if cell.revealed:
                y, x = i * block_size, j * block_size
                if cell.bomb:
                    return
                else:       # Number
                    draw_image(f'media/{DIFFICULTY}/{str(cell.number)}.png', x, y)


def on_first_click(mouse_position):
    # Pressed something outside the game AKA settings
    # Getting the cell clicked on according to mouse position
    coordinates = get_coordinates(mouse_position)
    bomb_number = get_bomb_number(DIFFICULTY)                           # Number of bombs according to difficulty
    board.fill_board(bomb_number, coordinates)                          # Creating the grid
    clicked_cell = board.get_cell(coordinates[0], coordinates[1])       # Getting the cell clicked on
    if clicked_cell.number == 0:                                        # Clears the zeroes if needed
        board.reveal_zeroes(coordinates[0], coordinates[1])
    clicked_cell.revealed = True                                        # Revealing the cell clicked on
    draw_revealed_on_zero()


def on_left_click(mouse_position):
    # Getting the cell clicked on
    x, y = get_coordinates(mouse_position)          # Getting the grid positions clicked on
    clicked_cell = board.get_cell(x, y)

    if clicked_cell.flagged:     # If clicked cell is flagged do nothing
        return

    if clicked_cell.bomb:      # Checking if the player clicked on a bomb and is supposed to lose
        on_bomb_click(y, x)    # Game_over
    elif clicked_cell.number == 0:        # Special case for the number zero
        board.reveal_zeroes(x, y)
        clicked_cell.revealed = True
        draw_revealed_on_zero()         # Revealing all the zero numbered cells needed to be revealed
    else:       # Draw the fitting number
        draw_image(f'media/{DIFFICULTY}/{str(clicked_cell.number)}.png', x * block_size, y * block_size)
        clicked_cell.revealed = True


def on_right_click(mouse_position):
    global flag_number
    # Getting the cell clicked on
    x, y = get_coordinates(mouse_position)
    clicked_cell = board.get_cell(x, y)

    if clicked_cell.revealed:       # Can't flag a revealed cell
        return

    if clicked_cell.flagged:  # If cell already flagged remove flag
        clicked_cell.flagged = False
        draw_image(f'media/{DIFFICULTY}/facingDown.png', x * block_size, y * block_size)    # Removing the flag
        flag_number += 1
    elif flag_number == 0:      # If no more flags are left exit
        return
    else:       # Has flags left and cell is not flagged
        clicked_cell.flagged = True
        draw_image(f'media/{DIFFICULTY}/flagged.png', x * block_size, y * block_size)
        flag_number -= 1


# Drawing the bomb on screen and showing a game over screen
def on_bomb_click(i, j):
    global lost     # Changing the lost variable to true

    # Drawing the bomb on the screen
    y, x = i * block_size, j * block_size
    draw_image(f'media/{DIFFICULTY}/facingDown.png', block_size * j, block_size * i)
    draw_image('media/general/bomb.png', x + int(block_size / 2) - 24, y + int(block_size / 2) - 24)

    # Creating transparent surface to draw on our screen
    temp = get_transparent_surface(GAME_WIDTH, GAME_HEIGHT)

    # Creating our game over text
    text = create_text('Game Over', DEFAULT_TEXT_FONT, DEFAULT_TEXT_SIZE, BLACK)

    # displaying our text on the screen and drawing the screen on our main screen
    temp.blit(text, (GAME_WIDTH // 2 - text.get_width() // 2, GAME_HEIGHT // 2 - text.get_height() // 2))
    screen.blit(temp, (0, 0))

    # Telling the main game loop the player lost
    lost = True


def get_current_time():
    current_time = datetime.now()
    time_difference = int((current_time - START_TIME).total_seconds())
    return time_difference


def on_settings_click(mouse_position):
    # Getting the coordinates
    x = mouse_position[0]
    y = mouse_position[1]

    # For easier calculations
    from_start_x = x - GAME_WIDTH

    # UPDATE LATER
    if y < 240:        # If no button was pressed on
        return
    if from_start_x <= 120 and 240 < y < 240 + EASY_BUTTON:      # If easy button pressed
        if DIFFICULTY == 'easy':        # If the difficulty is already easy do nothing
            return
        else:
            on_difficulty_changed('easy')
    elif from_start_x <= 120 and 360 < y < 360 + MEDIUM_BUTTON:  # If medium button pressed
        if DIFFICULTY == 'medium':
            return
        else:
            on_difficulty_changed('medium')
    elif from_start_x <= 120 and 480 < y < 480 + HARD_BUTTON:    # If hard button pressed
        if DIFFICULTY == 'hard':
            return
        else:
            on_difficulty_changed('hard')
    elif from_start_x < 240 and 600 < y < 600 + RESTART_BUTTON:  # If reset button pressed
        on_difficulty_changed(DIFFICULTY)       # Resetting the game


def is_player_won():
    if board.get_revealed() == number_of_tiles - get_bomb_number(DIFFICULTY):
        return True
    # Checking if all bombed cells are flagged - if yes player has won
    bombed_cells = board.get_bombed()
    for cell in bombed_cells:
        if not cell.flagged:
            return False
    return True


def get_transparent_surface(width, height):
    temp = pygame.Surface((width, height))
    temp.set_alpha(TRANSPARENT_ALPHA)
    temp.fill(WHITE)
    return temp


def on_win():
    # Updating the settings so the flag number updates if needed
    draw_settings()
    # Creating surface to draw on
    win_surface = get_transparent_surface(GAME_WIDTH, GAME_HEIGHT)

    # Creating our game over text
    text = create_text('You Won!', DEFAULT_TEXT_FONT, DEFAULT_TEXT_SIZE, BLACK)

    # displaying our text on the screen and drawing the screen on our main screen
    win_surface.blit(text, (GAME_WIDTH // 2 - text.get_width() // 2, GAME_HEIGHT // 2 - text.get_height() // 2))
    screen.blit(win_surface, (0, 0))


def create_text(text, font, size, color):
    # Creating our game over text
    text_font = pygame.font.SysFont(font, size)
    return text_font.render(text, True, color)


# Reset the game
def on_difficulty_changed(difficulty):
    global DIFFICULTY, block_size, flag_number, board, number_of_tiles
    # Changing variables which depend of difficulty
    DIFFICULTY = difficulty
    block_size = get_block_size(difficulty)
    flag_number = get_bomb_number(difficulty)
    board = Board(int(GAME_WIDTH / block_size), int(GAME_HEIGHT / block_size))
    number_of_tiles = board.width * board.height

    # Redraw the grid and change more global variables the game depends on
    restart_game()


# Change back to default all of the game variables
def reset_game_vars():
    global START_TIME, running, lost, won, first_click
    START_TIME = datetime.now()
    running = True
    lost = False
    won = False
    first_click = True


# Redraw the grid and change global variables not relying on difficulty
def restart_game():
    reset_game_vars()
    draw_grid()
    draw_settings()


# Initializing the game
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WINDOW_STARTING_X_POS, WINDOW_STARTING_Y_POS)       # Making the window appear in the middle of the screen when first started
pygame.init()

# game variables
DIFFICULTY = 'easy'
block_size = get_block_size(DIFFICULTY)
flag_number = get_bomb_number(DIFFICULTY)       # Number of flags is equal to number of bombs
board = Board(int(GAME_WIDTH / block_size), int(GAME_HEIGHT / block_size))
number_of_tiles = board.width * board.height


# Creating the screen and setting it up
screen = pygame.display.set_mode(DIMENSIONS)
pygame.display.set_caption('Minesweeper')

# Setting up game loop
START_TIME = datetime.now()
clock = pygame.time.Clock()
running = True
lost = False
won = False
first_click = True

draw_grid()
draw_settings()


while running:
    clock.tick(FPS)
    if not lost and not won:
        draw_settings()

    # Checking for events
    for event in pygame.event.get():        # Iterating over all events
        if event.type == pygame.QUIT:       # Closing the game if the the exit button was clicked
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:    # On mouse click
            position = pygame.mouse.get_pos()
            if event.button == LEFT_CLICK:   # Left mouse click
                if position[0] > GAME_WIDTH:
                    on_settings_click(position)
                    continue
                if first_click:
                    on_first_click(position)
                    first_click = False
                if won or lost:     # Making it so the player can't change the grid after winning or losing
                    continue
                else:
                    on_left_click(position)
                # Do something
            elif event.button == RIGHT_CLICK:     # Right mouse click
                if position[0] > GAME_WIDTH:    # If player pressed right click outside of the game grid do nothing
                    continue
                if won or lost:
                    continue
                on_right_click(position)
            if is_player_won():
                won = True
                on_win()

    # Updating the screen
    pygame.display.update()

