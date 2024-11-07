import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("badman.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)

        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        #keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


#define enemy object
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("enemy.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5,20)

    #move the sprite based on speed
    #remove the sprite when it passes the left edge of screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

#define cloud object
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)

        #the starting position is randomly generated
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0,SCREEN_HEIGHT)
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

#setup for sounds
pygame.mixer.init()

#intialize pygame
pygame.init()

#setup the clock for a decent framerate
clock = pygame.time.Clock()

#creat screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#creates custom event for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY,500)

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
#creates player
player = Player()


#creat groups to hold enemy sprites and all sprites
#- enemies is used for collision detection and position update
#clouds is used for position update
#- all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#load and play background theme song
pygame.mixer.music.load("theme_song.ogg")
pygame.mixer.music.play(loops=-1)

#variable to keep main loop runing
runing = True

while runing:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                runing = False

        elif event.type == QUIT:
            runing = False

        #add new enemy?
        elif event.type == ADDENEMY:
            # ceates the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        #add new cloud?
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)


    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    #enemy and cloud update
    enemies.update()
    clouds.update()

    #fill the screen with light gray
    screen.fill((94,94,94))

    #draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    #check if any enemies collided with player
    if pygame.sprite.spritecollideany(player, enemies):
        #if so then remove the player and stop the loop
        player.kill()
        runing = False

    #flip everything to display
    pygame.display.flip()

    #ensure we maintain a 30 frames per second rate
    clock.tick(30)

#we are done and should stop mixer
pygame.mixer.music.stop()
pygame.mixer.quit()