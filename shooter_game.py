#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
score = 0
lost = 0
num_fire = 0
heart = 5
reloading = False
class GameSprite(sprite.Sprite):
    def __init__(self,image1,speed,x,y,size_x,size_y):
        super().__init__()
        self.image = transform.scale(image.load(image1),(size_x,size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < window_width-80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',-10,self.rect.centerx,self.rect.top,15,20)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > window_hight:
            self.rect.y = 0
            self.rect.x = randint(80,window_width-80)
            self.speed = randint(1,5)
            lost  = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
window_width = 700
window_hight = 500
window = display.set_mode((window_width,window_hight))
display.set_caption('Space war')
background = transform.scale(image.load('galaxy.jpg'),(window_width,window_hight))
mixer.init()
font.init()
mixer.music.load('space.ogg')
mixer.music.play()
FPS = 60
font1 = font.SysFont('Arial',36)
font2 = font.SysFont('Arial',36)
font3 = font.SysFont('Arial',200)
win = font3.render('Win',True,(255,215,0))
lose = font3.render('Lose',True,(180,0,0))
asteroids = sprite.Group()
finish = False
rocket = Player('rocket.png',10,5,window_hight-100,80,100)
clock = time.Clock()
game = True
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png',randint(1,5),randint(80,window_width-80),-40,80,50)
    monsters.add(monster)
for i in range(1,3):
    asteroid = Enemy('asteroid.png',randint(1,3),randint(80,window_width-80),-40,80,50)
    asteroids.add(asteroid)
fire_sound = mixer.Sound('fire.ogg')
while game == True:
    for e in event.get():
        if e.type ==QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and reloading == False:
                    fire_sound.play()
                    rocket.fire()
                    num_fire += 1
                if num_fire >= 5 and reloading == False:
                    reloading = True
                    last_time = timer()              
    if finish != True:
        window.blit(background,(0,0))
        text_lose = font1.render('Пропущено:' + str(lost),1,(255,255,255))
        text_score = font2.render('Очки:' + str(score),1,(255,255,255))
        heart_picture = font2.render('Жизни:' + str(heart),1,(0,150,0))
        window.blit(text_lose,(10,50))
        window.blit(text_score,(10,20))
        window.blit(heart_picture,(550,10))
        rocket.update()
        rocket.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)
        sprite_group = sprite.groupcollide(monsters, bullets, True, True)
        if reloading == True:
            tim_fiks = timer()
            if tim_fiks - last_time < 2:
                rel_text = font2.render('Ожидайте перезарядку...',1,(150,0,0))
                window.blit(rel_text,(260,460))
            else:
                num_fire = 0
                reloading = False
        for i in sprite_group:
            score += 1
            monster = Enemy('ufo.png',randint(1,5),randint(80,window_width-80),-40,80,50)
            monsters.add(monster)
        if sprite.spritecollide(rocket,asteroids,False) or sprite.spritecollide(rocket,monsters,False) :
            sprite.spritecollide(rocket,asteroids,True)
            sprite.spritecollide(rocket,monsters,True)
            heart -= 1
        if heart == 0 or lost >= 10:
            finish = True
            window.blit(lose,(200,200))
        if score >= 10:
            finish = True
            window.blit(win,(200,200))
        display.update()
    clock.tick(FPS)

