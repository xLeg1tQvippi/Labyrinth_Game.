import pygame
import pygame as pg
from time import *
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
PURPLE=(255,0,255)
LIGHT_BLUE=(0,255,255)
VIOLET=(136,0,255)
ORANGE=(255,136,0)
DARK_PURPLE=(60,0,10)
W = 700
H = 500
pg.init()
mw = pg.display.set_mode((W, H))
pg.display.set_caption('Лабиринт')
pg.display.set_icon(pg.image.load("app.png"))
clock = pg.time.Clock()
mw.fill(VIOLET)
pic = "player.png"
pic_load = pg.image.load(pic).convert_alpha()
FPS = 60

class GameSprite(pg.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

walls = pg.sprite.Group()
w1 = GameSprite('wall_1.png', W / 2 - W / 3, H / 2, 300, 50)
w2 = GameSprite('wall_2.png', 370, 100, 50, 400)
walls.add(w1)
walls.add(w2)

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = pg.sprite.spritecollide(self,walls,False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        if self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        self.rect.y += self.y_speed
        platforms_touched = pg.sprite.spritecollide(self,walls,False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        if self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 15, 5)
        bullets.add(bullet)
        
        
bullets = pg.sprite.Group()


class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed, direction='left'):
        super().__init__(player_image, player_x, player_y, size_x, size_y)
        self.speed = speed
        self.direction = direction

    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        
        if self.rect.x <= 450:
            self.direction = 'right'
        if self.rect.x >= 650:
            self.direction = 'left'
        
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed):
        super().__init__( player_image, player_x, player_y, size_x, size_y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 700:
            self.kill()

monsters = pg.sprite.Group()
bullets = pg.sprite.Group()
win = pg.transform.scale(pg.image.load("win.png"), (700,500))
monster = Enemy("enemy.png", 200, 200, 50, 50, 2)
final = GameSprite("Ran.png",0,0,50,50)
player = Player(pic, 50, 50, 50, 50, 0,0)
monsters.add(monster)
finish = False
run = True
while run:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False
    

    #mw.fill(VIOLET)
    if e.type == pg.KEYDOWN:
        if e.key == pg.K_LEFT:
            player.x_speed = -5
            if player.rect.x < 0:
                player.rect.x = 0
        elif e.key == pg.K_RIGHT:
            player.x_speed = 5
            if player.rect.x > 650:
                player.rect.x = 650
        elif e.key == pg.K_UP:
            player.y_speed = -5
            if player.rect.y < 0:
                player.rect.y = 0
        elif e.key == pg.K_DOWN:
            player.y_speed = 5
            if player.rect.y > 455:
                player.rect.y = 455
        elif e.key == pg.K_SPACE:
            player.fire()

    pg.display.update()

    if e.type == pg.KEYUP:
        if e.key == pg.K_LEFT:
            player.x_speed = 0
        elif e.key == pg.K_RIGHT:
            player.x_speed = 0
        elif e.key == pg.K_UP:
            player.y_speed = 0
        elif e.key == pg.K_DOWN:
            player.y_speed = 0
    
    if run == True:
        if pg.sprite.collide_rect(player, monster):
            finish = True
    
    if finish != True:

        mw.fill(VIOLET)
        walls.draw(mw)
        player.reset()
        player.update()
        final.reset()
        bullets.draw(mw)
        bullets.update()

        if pg.sprite.collide_rect(player, final):
            finish = True
            mw.blit(win, (0,0))
    else:
        if finish == True:
            sleep(2)
            run = False
    pg.sprite.groupcollide(bullets, walls, True, False)
    if not pg.sprite.groupcollide(monsters, bullets, True, True):
        monsters.draw(mw)
        monsters.update()
#we need create group for monster and pg.sprite.groupcollide(bullets, mosters, True, True) +
#complete the game.
#make presentation of this game.
#features, why we created bullets in this game etc
#we need to represent this game
#presentation making Online.
#Canva etc
#ss

    pg.display.update()
    clock.tick(FPS)