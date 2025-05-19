#Создай собственный Шутер!

from pygame import *
import random
from time import time as timer

clock = time.Clock()
FPS = 144
win_widht = 1920
win_heigh = 1080

player_size_x = 220
player_size_y = 180

window = display.set_mode(
    (win_widht, win_heigh)
)

display.set_caption("Shooter")
background = transform.scale(
    image.load('background4.png'), (win_widht, win_heigh)
)

lifes_picture = transform.scale(
    image.load('bulletxxx.png'), (60, 60)
)

class GameSprite(sprite.Sprite):
    def __init__(self, image_player, pos_x, pos_y, speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(
            image.load(image_player), (size_x, size_y)
        )
        self.speed = speed
        self.rect = self.image.get_rect() # получаем прямоугольник объекта по картинке
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.size_x = size_x
        self.size_y = size_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

life = 3
num_fire = 0
rel_time = False
bullet_group = sprite.Group()

class Bullet(GameSprite):
    def update_position(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


class Player(GameSprite):
    def update_position(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_heigh - self.size_y - 5:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_widht - self.size_x - 5:
            self.rect.x += self.speed

    def shoot(self):
        pos_x = self.rect.x + self.size_x/2.1
        pos_y = self.rect.y + self.size_y/3
        bullet = Bullet('bulletxxx.png',pos_x, pos_y, 7, 20, 50)
        bullet_group.add(
            bullet
        )

lose_score = 0

class Asteroid(GameSprite):
    def update_position(self):
        global lose_score
        self.rect.y += self.speed
        if self.rect.y > win_heigh:
            self.kill()
            self.new_asteroid()
            lose_score += 1
    @classmethod
    def new_asteroid(cls):
        asteroid_size = random.randint(100, 150)
        speed = random.randint(1, 3)
        position_x = random.randint(50, win_widht-asteroid_size)
        asteroid = Asteroid('meteor_2.png', position_x, -100, speed, asteroid_size, asteroid_size)
        asteroids_group.add(
            asteroid
        )
        

player_position_x = (win_widht - player_size_x)/2
player_position_y = win_heigh - player_size_y - 5

player = Player('player11.png', player_position_x, player_position_y, 7, player_size_x, player_size_y)

asteroids_group = sprite.Group()

for _ in range(5):
    Asteroid.new_asteroid()

font.init()
text = font.SysFont('comicsansms', 50)
bigger_text = font.SysFont('comicsansms', 51)
massive_text = font.SysFont('comicsansms', 100)
score = 0

mixer.init()
mixer.music.load('background_music.mp3')
mixer.music.play()
mixer.music.set_volume(0.02)

game = True
finish = False
while game:
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game = False

        if e.type == QUIT:
            game = False

        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            if num_fire <7 and rel_time == False:
                num_fire += 1
                player.shoot()
            elif num_fire == 7 and rel_time == False:
                rel_time = True
                seconds = timer()

    if not finish:
        window.blit(background, (0, 0))
        score_text = text.render(f'счет: {score}', True, (241, 41, 41))
        lose_score_text = text.render(f"пропущенно: {lose_score}", True, (241, 41, 41))
        score_text1 = bigger_text.render(f'счет: {score}', True, (0, 0, 0))
        lose_score_text1 = bigger_text.render(f"пропущенно: {lose_score}", True, (0, 0, 0))
        player.update_position()
        player.reset()

        if rel_time:
            end_seconds = timer()
            if end_seconds - seconds < 2:
                rel_text = text.render(f"Relaod: {int(end_seconds - seconds) + 1}", True, (241, 41, 41))
                window.blit(rel_text, (win_widht/2 - 100, win_heigh - 100))
            else:
                rel_time = False
                num_fire = 0
        
        if life == 3:
            window.blit(lifes_picture, (1500, 60))
            window.blit(lifes_picture, (1570, 60))
            window.blit(lifes_picture, (1640, 60))

        if life == 2:
            window.blit(lifes_picture, (1500, 60))
            window.blit(lifes_picture, (1570, 60))

        if life == 1:
            window.blit(lifes_picture, (1500, 60))
            
        for obj in bullet_group:
            obj.update_position()
            obj.reset()

        for obj in asteroids_group:
            obj.update_position()
            obj.reset()

        collision = sprite.groupcollide(asteroids_group, bullet_group, True , True)

        if sprite.spritecollide(player, asteroids_group, True):
            life -= 1

        if life == 0 or lose_score == 8:
            lose_text = massive_text.render("вы проиграли!!", True, (255, 255, 255))
            window.blit(lose_text, (win_widht/2-400, win_heigh/2-100))
            finish = True

        if score >= 10:
            win_text = massive_text.render("вы выиграли!!", True, (255, 255, 255))
            window.blit(win_text, (win_widht/2-400, win_heigh/2-100))
            finish = True

        for _ in collision:
            score += 1
            Asteroid.new_asteroid()
        window.blit(lose_score_text1, (0, 50))
        window.blit(score_text1, (0, 0))    
        window.blit(lose_score_text, (0, 50))
        window.blit(score_text, (0, 0))

    display.update()
    clock.tick(FPS)
