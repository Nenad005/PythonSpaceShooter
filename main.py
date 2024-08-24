import pygame, os, sys
import configparser

from pygame import mixer
from sys import exit

config = configparser.ConfigParser()
config.read('config.ini')
settings = config['SETTINGS']

WIDTH, HEIGHT = 900, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PRVA IGRA')
pygame.init()

RUN = False

YELLOW_SCORE = 0
RED_SCORE = 0

clock = pygame.time.Clock()

clear = lambda: os.system('cls')

#ZVUK 

VOLUME = float(settings['volume'])

mixer.music.load(os.path.join('Assets', 'sounds', 'background.wav'))
mixer.music.set_volume(VOLUME)
mixer.music.play(-1)

LASER_SOUND = mixer.Sound(os.path.join('Assets', 'sounds', 'laser.wav'))
LASER_SOUND.set_volume(VOLUME)

HIT_SOUND = mixer.Sound(os.path.join('Assets', 'sounds', 'hit.wav'))
HIT_SOUND.set_volume(VOLUME)

EXPLOSION_SOUND = mixer.Sound(os.path.join('Assets', 'sounds', 'explosion.wav'))
EXPLOSION_SOUND.set_volume(VOLUME)

WIN_SOUND = mixer.Sound(os.path.join('Assets', 'sounds', 'win.wav'))
WIN_SOUND.set_volume(VOLUME)

#KONSTANTE

PLAYER1_NAME = settings['yellow']
PLAYER2_NAME = settings['red']

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60

VEL = float(settings['vel'])

MAX_HEALTH = int(float(settings['max_health'])//1)

MAX_BULLETS = int(float(settings['max_bullets'])//1)
BULLET_VEL = float(settings['bullet_vel'])

S_WIDTH, S_HEIGHT = 60, 40
B_WIDTH, B_HEIGHT = 30, 10

HEART_SIZE = 25

FONT_SIZE = 30
W_FONT_SIZE = 100
FONT = pygame.font.Font(os.path.join('Assets', 'fonts', 'font.ttf'), FONT_SIZE)
W_FONT = pygame.font.Font(os.path.join('Assets', 'fonts', 'font.ttf'), W_FONT_SIZE)

BORDER = pygame.Rect((WIDTH/2) - 3, 0, 6, HEIGHT)

#SLIKE

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'pictures', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate((pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (S_WIDTH, S_HEIGHT))), 90)

YELLOW_BULLET_IMAGE = pygame.image.load(os.path.join('Assets', 'pictures', 'laser.png'))
YELLOW_BULLET = pygame.transform.rotate((pygame.transform.scale(YELLOW_BULLET_IMAGE, (B_HEIGHT, B_WIDTH))), 270)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'pictures', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate((pygame.transform.scale(RED_SPACESHIP_IMAGE, (S_WIDTH, S_HEIGHT))), 270)

RED_BULLET_IMAGE = pygame.image.load(os.path.join('Assets', 'pictures', 'laser2.png'))
RED_BULLET = pygame.transform.rotate((pygame.transform.scale(RED_BULLET_IMAGE, (B_HEIGHT, B_WIDTH))), 90)

SPACE_IMAGE = pygame.image.load(os.path.join('Assets', 'pictures', 'space.png'))
SPACE_BG = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))

HEART_IMAGE = pygame.image.load(os.path.join('Assets', 'pictures', 'heart.png'))
HEART = pygame.transform.scale(HEART_IMAGE, (HEART_SIZE, HEART_SIZE))

#METODE

def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_lives, red_lives):
    #WIN.fill(WHITE)
    global YELLOW_SCORE
    global RED_SCORE
    global RUN

    WIN.blit(SPACE_BG, (0, 0))
    
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    for bullet in yellow_bullets:

        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
            continue

        bullet.x += BULLET_VEL

        if bullet.colliderect(red):
            yellow_bullets.remove(bullet)
            HIT_SOUND.play()

            if len(red_lives) > 0:
                red_lives.pop()

        WIN.blit(YELLOW_BULLET, bullet)

    for bullet in red_bullets:

        if bullet.x < 0:
            red_bullets.remove(bullet)
            continue

        if bullet.colliderect(yellow):
            red_bullets.remove(bullet)
            HIT_SOUND.play()

            if len(yellow_lives) > 0:
                yellow_lives.pop()

        bullet.x -= BULLET_VEL
        WIN.blit(RED_BULLET, bullet)

    for i in range (len(yellow_lives)):
        WIN.blit(HEART, (5 + i * HEART_SIZE, 5))

    for i in range (len(red_lives)):
        WIN.blit(HEART, (WIDTH-5-HEART_SIZE - i * HEART_SIZE, 5))

    

    if len(yellow_lives) == 0 and len(red_lives) != 0:
        RED_SCORE += 1
        EXPLOSION_SOUND.play()
        draw_score()
        pygame.display.update()
        draw_winner(PLAYER2_NAME + ' WINS!!!')
        RUN = False

    if len(red_lives) == 0 and len(yellow_lives) != 0:
        YELLOW_SCORE += 1
        EXPLOSION_SOUND.play()
        draw_score()
        pygame.display.update()
        draw_winner(PLAYER1_NAME + ' WINS!!!')
        RUN = False

    if len(red_lives) == 0 and len(yellow_lives) == 0:
        YELLOW_SCORE += 1
        RED_SCORE += 1
        EXPLOSION_SOUND.play()
        draw_score()
        pygame.display.update()
        draw_winner('TIE GAME!!!')
        RUN = False

    draw_score()
    pygame.draw.rect(WIN, WHITE, BORDER)
    pygame.display.update()
    

def move(keys_pressed, yellow, red):

    if keys_pressed[pygame.K_w] and yellow.y  > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y < HEIGHT - YELLOW_SPACESHIP.get_height():
        yellow.y += VEL
    if keys_pressed[pygame.K_a] and yellow.x > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x < (WIDTH/2)-YELLOW_SPACESHIP.get_width():
        yellow.x += VEL  
    if keys_pressed[pygame.K_UP] and red.y > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y < HEIGHT - RED_SPACESHIP.get_height():
        red.y += VEL
    if keys_pressed[pygame.K_LEFT] and red.x > (WIDTH/2):
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x < WIDTH-YELLOW_SPACESHIP.get_width():
        red.x += VEL  

def main():
    global RUN

    yellow = pygame.Rect(100, 300, S_HEIGHT, S_WIDTH)
    red = pygame.Rect(780, 300, S_HEIGHT, S_WIDTH)

    #clock = pygame.time.Clock()
    RUN = True

    yellow_bullets = [] 
    red_bullets = []
    
    yellow_lives = [None] * MAX_HEALTH
    red_lives = [None] * MAX_HEALTH

    while RUN:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                RUN = False
                quit();

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + S_HEIGHT ,yellow.y + S_WIDTH/2 - B_HEIGHT/2, B_WIDTH, B_HEIGHT)
                    yellow_bullets.append(bullet)
                    LASER_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x - B_WIDTH ,red.y + S_WIDTH/2 - B_HEIGHT/2, B_WIDTH, B_HEIGHT)
                    red_bullets.append(bullet)
                    LASER_SOUND.play()
                if event.key == pygame.K_q:
                    heal(yellow_lives)

        keys_pressed = pygame.key.get_pressed()
        move(keys_pressed, yellow, red)

        #print('YELLOW ----> X : ', yellow.x, ', Y : ', yellow.y, '\nRED ----> X : ',red.x, ', Y : ',red.y)
        #clear()

        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_lives, red_lives)

    main()

def heal(player_lives):
    n = 2
    if len(player_lives) < MAX_HEALTH and len(player_lives) > MAX_HEALTH - n:
        n = MAX_HEALTH - len(player_lives)
    elif len(player_lives) >= MAX_HEALTH:
        return
    for i in range(n):
        player_lives.append([None])

def draw_score():
    YELLOW_TEXT = FONT.render(PLAYER1_NAME + ' : ' + str(YELLOW_SCORE), True, WHITE)
    WIN.blit(YELLOW_TEXT, (0, HEIGHT - FONT_SIZE))

    RED_TEXT = FONT.render(PLAYER2_NAME + ' : ' + str(RED_SCORE), True, WHITE)
    WIN.blit(RED_TEXT, (WIDTH - RED_TEXT.get_width(), HEIGHT - FONT_SIZE))


def draw_winner(winner):

    WINNER_TEXT = W_FONT.render(winner , True, WHITE,)
    WIN.blit(WINNER_TEXT, center(WIN, WINNER_TEXT))
    pygame.display.update()
    WIN_SOUND.play()
    pygame.time.wait(3000)

def center(PROZOR, SLIKA):

    height = (PROZOR.get_height()/2.0) - SLIKA.get_height() / 2.0
    width = (PROZOR.get_width()/2.0) - SLIKA.get_width() / 2.0
    return (width, height)

def quit():

    pygame.quit()
    exit()

if __name__ == '__main__':

    print(__name__)
    main()
    pass