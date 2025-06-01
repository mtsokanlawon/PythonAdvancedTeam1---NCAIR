import pygame
from pygame import mixer
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

# Define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# Fighter data
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# Load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
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
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
start_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 5, y - 5, 410, 40))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

def create_fighters(mode):
    f1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
    f2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
    if mode == "pvc":
        f2.is_ai = True
    return f1, f2

# --- Menu loop ---
mode = None
menu = True
while menu:
    screen.fill((0, 0, 0))
    draw_text("WARWIZ", count_font, YELLOW, SCREEN_WIDTH // 2 - 150, 100)
    draw_text("1 - Player vs Player", start_font, WHITE, SCREEN_WIDTH // 2 - 140, 250)
    draw_text("2 - Player vs Computer", start_font, WHITE, SCREEN_WIDTH // 2 - 140, 300)
    draw_text("Q - Quit", start_font, WHITE, SCREEN_WIDTH // 2 - 140, 350)

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

    pygame.display.update()

# Game setup
fighter_1, fighter_2 = create_fighters(mode)
run = True
start = False

while run:
    draw_bg()

    if not start:
        start_text = "Press Key S To Start"
        pygame.draw.rect(screen, RED, (295, (SCREEN_HEIGHT / 3) - 5, 410, 50))
        pygame.draw.rect(screen, WHITE, (300, SCREEN_HEIGHT / 3, 400, 40))
        draw_text(start_text, start_font, BLACK, 20 + (SCREEN_WIDTH / 3), SCREEN_HEIGHT / 3)
    else:
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
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif not fighter_2.alive:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            screen.blit(victory_img, (360, 150))
            if (pygame.time.get_ticks() - round_over_time) > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                fighter_1, fighter_2 = create_fighters(mode)

        fighter_1.draw(screen)
        fighter_2.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            start = True
        # Quit while game is on
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
                pygame.quit()
                exit()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
