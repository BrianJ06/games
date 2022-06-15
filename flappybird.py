import os
import sys
import pygame
import random
import time
pygame.init()

#bg image
background = pygame.image.load("assets/flappybirdassets/sprites/background-day.png")
background = pygame.transform.scale(background, (576, 1024))

#start screen
title = pygame.image.load("assets/flappybirdassets/sprites/message.png")
title = pygame.transform.scale(title, (368, 534))

game_started = False
gameOver = False

start = 0
last_update = 0
score_update = 1.5

gravity = 3

#ground
class Base(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        base = pygame.image.load("assets/flappybirdassets/sprites/base.png")

        sprite = pygame.Surface([336, 72])
        sprite.blit(base, (0, 0), (0, 0, 336, 72))
        sprite = pygame.transform.scale(sprite, (672, 144))

        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = height-144

        self.moved = 0

    #move ground
    def animate(self):
        self.rect.x -= 8
        self.moved += 8

        if self.moved == 96:
            self.rect.x = 0
            self.moved = 0

#bird
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #animation frames
        self.images = [
            pygame.image.load("assets/flappybirdassets/sprites/yellowbird-upflap.png"),
            pygame.image.load("assets/flappybirdassets/sprites/yellowbird-downflap.png"),
            pygame.image.load("assets/flappybirdassets/sprites/yellowbird-midflap.png")
        ]

        #create sprites for frames
        self.sprites = []

        for i in range(3):
            for j in range(2):
                image = self.images[i]
                sprite = pygame.Surface([34, 24], pygame.SRCALPHA, 32)
                sprite.blit(image, (0, 0))
                sprite = pygame.transform.scale(sprite, (68, 48))
                self.sprites.append(sprite)

        self.imageOrig = self.sprites[2]
        self.image = self.sprites[2]
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2
        self.rect.centery = height/2

        self.y = 0
        self.dy = 0
        self.dymax = -24
        self.angle = 0
        self.frame = 1
        self.score = 0

    #jump
    def jump(self):
        self.dy = 24

    #move bird, apply gravity, change angle
    def move(self):
        self.rect.y -= self.dy
        self.dy -= gravity

        if self.dy > -12 and self.angle < 20:
            self.angle = 20
            self.image = pygame.transform.rotate(self.image, self.angle)

        if self.dy < -12 and self.angle > -90:
            self.angle -= 6
            self.image = pygame.transform.rotate(self.image, self.angle)

        self.y = self.rect.centery

    #switch through animation frames
    def animate(self):
        if self.frame < 5:
            self.frame += 1
        else:
            self.frame = 0

        self.image = self.sprites[self.frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2
        self.rect.centery = self.y
        self.image = pygame.transform.rotate(self.image, self.angle)

    #check if bird hits pipes or ground
    def checkDeath(self):
        global gameOver
        if pygame.Rect.colliderect(player.rect, base.rect):
            gameOver = True
        for pipe in pipes:
            if pygame.Rect.colliderect(player.rect, pipe.rect):
                gameOver = True

#pipes
class Pipe(pygame.sprite.Sprite):
    def __init__(self, index, height):
        super().__init__()

        image = pygame.image.load("assets/flappybirdassets/sprites/pipe-green.png")
        self.sprites = []

        # index 0 faces up, index 1 faces down
        for i in range(2):
            sprite = pygame.Surface([52, 320], pygame.SRCALPHA, 32)
            sprite.blit(image, (0, 0))
            sprite = pygame.transform.scale(sprite, (104, 640))
            if i == 1:
                sprite = pygame.transform.rotate(sprite, 180)
            self.sprites.append(sprite)

        self.image = self.sprites[index]
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = height

        pipes.add(self)

    #move pipes to the left
    def move(self):
        self.rect.x -= 8
        if self.rect.right < 0:
            self.kill()

#scoreboard
class Score(pygame.sprite.Sprite):
    def __init__(self, index, x, y):
        super().__init__()

        #number images
        self.images = [
            pygame.image.load("assets/flappybirdassets/sprites/0.png"),
            pygame.image.load("assets/flappybirdassets/sprites/1.png"),
            pygame.image.load("assets/flappybirdassets/sprites/2.png"),
            pygame.image.load("assets/flappybirdassets/sprites/3.png"),
            pygame.image.load("assets/flappybirdassets/sprites/4.png"),
            pygame.image.load("assets/flappybirdassets/sprites/5.png"),
            pygame.image.load("assets/flappybirdassets/sprites/6.png"),
            pygame.image.load("assets/flappybirdassets/sprites/7.png"),
            pygame.image.load("assets/flappybirdassets/sprites/8.png"),
            pygame.image.load("assets/flappybirdassets/sprites/9.png")
        ]

        self.sprites = []

        #make sprites
        for i in range(10):
            image = self.images[i]
            if i == 1:
                sprite = pygame.Surface([16, 36], pygame.SRCALPHA, 32)
                sprite.blit(image, (0, 0))
                sprite = pygame.transform.scale(sprite, (32, 72))
            else:
                sprite = pygame.Surface([24, 36], pygame.SRCALPHA, 32)
                sprite.blit(image, (0, 0))
                sprite = pygame.transform.scale(sprite, (48, 72))
            self.sprites.append(sprite)

        self.image = self.sprites[index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.centery = 100

#game over message
class gameOverSign(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        image = pygame.image.load("assets/flappybirdassets/sprites/gameover.png")

        sprite = pygame.Surface([192, 42], pygame.SRCALPHA, 32)
        sprite.blit(image, (0, 0))
        sprite = pygame.transform.scale(sprite, (384, 84))

        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.centerx = 288
        self.rect.centery = 280

#restart button
class Restart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        image = pygame.image.load("assets/flappybirdassets/sprites/buttons.png")

        button = pygame.Surface([12, 12], pygame.SRCALPHA, 32)
        button.blit(image, (0, 0), (146, 145, 12, 12))
        button = pygame.transform.scale(button, (96, 96))

        self.image = button
        self.rect = self.image.get_rect()
        self.rect.centerx = 288
        self.rect.centery = 400

    #restart program if button is clicked
    def checkClick(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            os.execl(sys.executable, 'python', 'flappybird.py', *sys.argv[1:])

#start screen
width = 576
height = 824
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')

#sprite groups
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()
scores = pygame.sprite.Group()

#create ground and bird
base = Base()
all_sprites.add(base)

player = Player()
all_sprites.add(player)

#update score
def showScore():
    for score in scores:
        all_sprites.remove(score)
        scores.remove(score)
    if player.score < 10:
        newScore = Score(player.score, 264, 100)
        all_sprites.add(newScore)
        scores.add(newScore)
    elif 10 <= player.score < 20:
        onesDigit = int(str(player.score)[1])
        newScore1 = Score(1, 256, 100)
        newScore2 = Score(onesDigit, 288, 100)
        all_sprites.add(newScore1, newScore2)
        scores.add(newScore1, newScore2)
    else:
        tensDigit = int(str(player.score)[0])
        onesDigit = int(str(player.score)[1])
        newScore1 = Score(tensDigit, 240, 100)
        newScore2 = Score(onesDigit, 288, 100)
        all_sprites.add(newScore1, newScore2)
        scores.add(newScore1, newScore2)

running = True

clock = pygame.time.Clock()

while running:
    #end program if window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #start game and jump on click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_started == False:
                game_started = True
                start = time.time()
                showScore()
            player.jump()

    #update screen
    all_sprites.update()
    if game_started == True and gameOver == False:
        base.animate()
        player.move()
        player.animate()
        player.checkDeath()
        showScore()

        for pipe in pipes:
            pipe.move()

        #create new pipes
        current_time = time.time()
        timePassed = current_time - start
        if timePassed - last_update >= 2:
            height = random.randrange(240, 640)
            pipe1 = Pipe(0, height)
            pipe2 = Pipe(1, height-840)
            all_sprites.add(pipe1, pipe2)
            last_update = timePassed

        #add to score
        if timePassed - score_update >= 2:
            player.score += 1
            score_update = timePassed

    #show game over message and restart button
    if gameOver == True:
        all_sprites.add(gameOverSign())
        restart = Restart()
        all_sprites.add(restart)

        if pygame.mouse.get_pressed()[0] == 1:
            restart.checkClick()

    #update screen
    screen.blit(background, (0, 0), (0, 150, 576, 824))
    if game_started == False:
        screen.blit(title, (104, 50), (0, 0, 368, 534))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
