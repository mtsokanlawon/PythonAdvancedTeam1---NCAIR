import pygame # selected Package for game in python, handles GUI
# use mixer module of pygame for audio and sound effects handling
from fighterv2 import Fighter

pygame.init()

# Create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('WarWiz')

# Define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PAUSE_MENU_COLOR = (30, 30, 30) # A close to black dark color 

# Define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000 # 2 seconds

# Fighter data
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4 
WARRIOR_OFFSET = [72, 56] # [x , y]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# Load music and sounds effects
# music
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000) # -1: continue playing as long as the program is running
# sound effects(fx)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.5)

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Load background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# Load spritesheets
warrior_sheet = pygame.image.load("assets/images/Warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# Load victory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# Animation steps
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# Fonts
title_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
start_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
menu_font = start_font

# Main Game Functions
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))
    
# this handles the background size, since the original size is bigger, this scales it down to fit perfectly in the game window 
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))
    
# this handles the rectangular bar that displays the health size, give full health yellow and as the player is beign attacked it displays red color 
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 5, y - 5, 410, 40))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))
# this handles the fighters parameters, and the instructs the computer to play using ai when the user choses player vs computer
def create_fighters(mode) -> tuple:
    f1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
    f2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
    if mode == "pvc":
        f2.is_ai = True
    return f1, f2

# Handle game pausing
paused = False

def draw_pause_menu(screen, font):
    menu_surface = pygame.Surface((400, 200))
    menu_surface.fill(PAUSE_MENU_COLOR)
    pygame.draw.rect(menu_surface, (200, 200, 200), menu_surface.get_rect(), 4)

    continue_text = font.render("Press C to Continue", True, (255, 255, 255))
    quit_text = font.render("Press Q to Quit", True, (255, 255, 255))

    menu_surface.blit(continue_text, (50, 50))
    menu_surface.blit(quit_text, (50, 100))

    screen.blit(menu_surface, (screen.get_width() // 2 - 200, screen.get_height() // 2 - 100))

# Menu loop
mode = None
menu = True
while menu:
    screen.fill(BLACK) # fill screen with black color
    draw_text("WARWIZ", title_font, YELLOW, SCREEN_WIDTH // 2 - 150, 100)
    draw_text("1 - Player vs Player", menu_font, WHITE, SCREEN_WIDTH // 2 - 140, 250)
    draw_text("2 - Player vs Computer", menu_font, WHITE, SCREEN_WIDTH // 2 - 140, 300)
    draw_text("Q - Quit", menu_font, WHITE, SCREEN_WIDTH // 2 - 140, 350)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = "pvp"
                menu = False
            elif event.key == pygame.K_2:
                mode = "pvc"
                menu = False
            elif event.key == pygame.K_q:
                pygame.quit()
                exit()

    pygame.display.update() # display changes to screen

# Game setup
# create fighter instances
fighter_1, fighter_2 = create_fighters(mode)

# game loop
run = True
start = False

while run:
    draw_bg()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # check for input to start the game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            start = True
        # get input for pause while game is on
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
        # check for inputs while pause menu is displayed
        if paused and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False
            if event.key == pygame.K_c:
                paused = False

        # Quit while game is on
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
                pygame.quit()
                exit()

    # Display Start instruction while start is False
    if not start:
        start_text = "Press Key 'S' To Start"
        pygame.draw.rect(screen, RED, (295, (SCREEN_HEIGHT / 3) - 5, 410, 50))
        pygame.draw.rect(screen, WHITE, (300, SCREEN_HEIGHT / 3, 400, 40))
        draw_text(start_text, start_font, BLACK, 20 + (SCREEN_WIDTH / 3), SCREEN_HEIGHT / 3)

    # Run game   
    else:
        if not paused:
            draw_health_bar(fighter_1.health, 20, 20)
            draw_health_bar(fighter_2.health, 580, 20)
            draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
            draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

            if intro_count <= 0:
                fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_2, round_over)
                fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_1, round_over)
            else:
                draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()

            fighter_1.update()
            fighter_2.update()

            if not round_over:
                if not fighter_1.alive:
                    score[1] += 1 # update score for player 2
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
                elif not fighter_2.alive:
                    score[0] += 1 # update score for player 1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
            else:
                screen.blit(victory_img, (360, 150))
                if (pygame.time.get_ticks() - round_over_time) > ROUND_OVER_COOLDOWN:
                    round_over = False
                    intro_count = 3
                    fighter_1, fighter_2 = create_fighters(mode) #reinstantiate fighters after each round.
                    # All stats return to max

            # display concurrent actions after all updates.
            fighter_1.draw(screen)
            fighter_2.draw(screen)

        # chack for pause and display pause menu.
        if paused:
                draw_pause_menu(screen, menu_font)

    

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
