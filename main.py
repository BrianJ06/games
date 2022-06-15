import os
import sys
import pygame
import random
pygame.init()

#bg color
background = (116, 200, 87)

#count frames passed for animations
last_update = 0
water_update = 0

#player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #make sprites for animation frames
        self.spritesheet = pygame.image.load("assets/mainassets/sprites/characters/slime.png")
        self.sprites = []

        self.makeSprite(6, 46, 20, 10)
        self.makeSprite(42, 40, 12, 16)
        self.makeSprite(74, 38, 12, 18)
        self.makeSprite(104, 41, 16, 15)
        self.makeSprite(136, 44, 16, 12)
        self.makeSprite(168, 45, 16, 11)

        self.x = 0
        self.y = 0
        self.direction = 'right'
        self.lastDirection = 'right'
        self.speed = 5

        #create sprite image
        self.index = 0
        self.image = self.sprites[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (153, 348)

    #make sprites
    def makeSprite(self, x, y, w, h):
        sprite = pygame.Surface([20, 18], pygame.SRCALPHA, 32)
        sprite.blit(self.spritesheet, ((20-w)/2, 18-h), (x, y, w, h))
        sprite = pygame.transform.scale(sprite, (40, 36))
        self.sprites.append(sprite)

    #directional movement
    def moveUp(self):
        if current_screen == 1:
            if self.rect.bottom > 306:
                self.rect.centery -= self.speed
        if current_screen == 2:
            self.rect.centery -= self.speed

    def moveDown(self):
        if current_screen == 1:
            if self.rect.bottom < 420:
                self.rect.centery += self.speed
        if current_screen == 2:
            self.rect.centery += self.speed

    def moveLeft(self):
        self.lastDirection = self.direction
        self.direction = 'left'
        if current_screen == 1:
            if self.rect.left > 100:
                self.rect.centerx -= self.speed
        if current_screen == 2:
            self.rect.centerx -= self.speed

    def moveRight(self):
        self.lastDirection = self.direction
        self.direction = 'right'
        if current_screen == 1:
            self.rect.centerx += self.speed
        if current_screen == 2:
            self.rect.centerx += self.speed

    #switch through animation frames
    def animate(self):
        if self.index == len(self.sprites)-1:
            self.index = 0
        else:
            self.index += 1

        self.image = self.sprites[self.index]
        self.rect = self.image.get_rect()

        self.rect.centerx = self.x
        self.rect.centery = self.y

    #flip sprite based on direction faced
    def flip(self):
        if self.lastDirection != self.direction:
            for sprite in self.sprites:
                sprite.blit(pygame.transform.flip(sprite, True, False), sprite.get_rect())

    #enter game if clicked on
    def game(self):
        if 165 < self.rect.centerx < 417 and 576 < self.rect.centery < 708:
            os.execl(sys.executable, 'python', "minesweeper.py", *sys.argv[1:])
        if 191 < self.rect.centerx < 391 and  8 < self.rect.centery < 142:
            os.execl(sys.executable, 'python', "flappybird.py", *sys.argv[1:])

#games to click on
class gameLogo(pygame.sprite.Sprite):
    def __init__(self, index, x, y):
        super().__init__()

        self.logos = []

        #minesweeper
        sprite = pygame.Surface([503, 263], pygame.SRCALPHA, 32)
        img = pygame.image.load("assets/minesweeperassets/minesweeperlogo.png")
        sprite.blit(img, (0, 0))
        sprite = pygame.transform.scale(sprite, (251, 131))
        self.logos.append(sprite)

        #flappy bird
        sprite = pygame.Surface([1500, 1000], pygame.SRCALPHA, 32)
        img = pygame.image.load("assets/flappybirdassets/flappybirdlogo.png")
        sprite.blit(img, (0, 0))
        sprite = pygame.transform.scale(sprite, (200, 133))
        self.logos.append(sprite)

        self.image = self.logos[index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

#define sprite class with makeSprite function
class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.spritesheet = None

    def makeSprite(self, list, x, y, w, h):
        sprite = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        sprite.blit(self.spritesheet, (0, 0), (x, y, w, h))
        sprite = pygame.transform.scale(sprite, (3 * w, 3 * h))
        list.append(sprite)

#sprites used for environment
class Path(Sprite):
    def __init__(self, index, x, y, angle):
        super().__init__()

        self.spritesheet = pygame.image.load("assets/mainassets/First Asset pack.png")

        self.path = []
        self.makeSprite(self.path, 217, 157, 34, 34)    # path
        self.makeSprite(self.path, 217, 92, 34, 4)      # top
        self.makeSprite(self.path, 217, 60, 34, 4)      # bottom
        self.makeSprite(self.path, 248, 61, 4, 34)      # left
        self.makeSprite(self.path, 216, 61, 4, 34)      # right
        self.makeSprite(self.path, 216, 60, 33, 33)     # top left
        self.makeSprite(self.path, 219, 60, 33, 33)     # top right
        self.makeSprite(self.path, 216, 63, 33, 33)     # bottom left
        self.makeSprite(self.path, 219, 63, 33, 33)     # bottom right

        self.image = self.path[index]
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Cliff(Sprite):
    def __init__(self, index, x, y):
        super().__init__()

        self.spritesheet = pygame.image.load("assets/mainassets/First Asset pack.png")

        self.cliff = []
        #land
        self.makeSprite(self.cliff, 83, 246, 24, 18)    # horizontal
        self.makeSprite(self.cliff, 107, 246, 24, 32)   # slope down
        self.makeSprite(self.cliff, 131, 246, 24, 32)   # slope up
        #water
        self.makeSprite(self.cliff, 95, 316, 24, 35)    # horizontal
        self.makeSprite(self.cliff, 119, 330, 24, 35)   # slope down
        self.makeSprite(self.cliff, 143, 330, 24, 35)   # slope up


        self.image = self.cliff[index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Tree(Sprite):
    def __init__(self, index, x, y):
        super().__init__()

        self.spritesheet = pygame.image.load("assets/mainassets/First Asset pack.png")

        self.tree = []
        self.makeSprite(self.tree, 16, 96, 40, 48)      # big tree
        self.makeSprite(self.tree, 61, 112, 22, 32)     # small tree
        self.makeSprite(self.tree, 88, 128, 17, 16)     # bush

        self.image = self.tree[index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Object(Sprite):
    def __init__(self, index, x, y):
        super().__init__()

        self.spritesheet = pygame.image.load("assets/mainassets/First Asset pack.png")

        self.objects = []
        self.makeSprite(self.objects, 35, 8, 50, 76)         # house
        self.makeSprite(self.objects, 112, 128, 12, 16)      # left end of fence
        self.makeSprite(self.objects, 124, 128, 12, 16)      # fence
        self.makeSprite(self.objects, 136, 128, 16, 16)      # right end of fence
        self.makeSprite(self.objects, 156, 132, 11, 12)      # small lilypad
        self.makeSprite(self.objects, 173, 128, 15, 16)      # big lilypad

        self.image = self.objects[index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Plant(Sprite):
    def __init__(self, index, x, y):
        super().__init__()

        self.spritesheet = pygame.image.load("assets/mainassets/First Asset pack.png")

        self.plants = []

        #flowers
        for i in range(4):
            for j in range(3):
                self.makeSprite(self.plants, 24+i*12, 156+j*12, 12, 12)
        self.makeSprite(self.plants, 72, 180, 12, 12)

        #grass
        for i in range(6):
            for j in range(4):
                self.makeSprite(self.plants, 84+i*12, 156+j*12, 12, 12)

        self.image = self.plants[index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Water(Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.spritesheet = pygame.image.load("assets/mainassets/First Asset pack.png")

        self.water = []
        self.makeSprite(self.water, 264, 156, 36, 36)
        self.image = self.water[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        water.append(self)

        self.origx = x
        self.origy = y

    def animate(self):
        self.rect.x += 5
        if self.rect.x > self.origx + 108:
            self.rect.x = self.origx

#start screen
width = 960
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Hi :)')

#sprite groups
all_sprites = pygame.sprite.Group()
all_rects = []
water = []

def start_screen():
    #cliffs on top
    all_sprites.add(Cliff(2, 0, 180), Cliff(0, 72, 180), Cliff(2, 144, 138), Cliff(0, 216, 138), Cliff(1, 288, 138), Cliff(0, 360, 180), Cliff(2, 432, 138),
                    Cliff(2, 504, 96), Cliff(0, 576, 96), Cliff(1, 648, 96), Cliff(0, 720, 138), Cliff(1, 792, 138), Cliff(0, 864, 180), Cliff(2, 936, 138))

    #water
    for i in range(10):
        for j in range(3):
            all_sprites.add(Water(i*108-108, 708-j*108))

    #cliffs on bottom (water)
    all_sprites.add(Cliff(4, 0, 438), Cliff(3, 72, 438), Cliff(4, 144, 480), Cliff(3, 216, 480), Cliff(5, 288, 480), Cliff(3, 360, 438), Cliff(5, 432, 438),
                    Cliff(3, 504, 396), Cliff(4, 576, 438), Cliff(4, 648, 480), Cliff(3, 720, 480), Cliff(5, 792, 480), Cliff(3, 864, 438), Cliff(5, 936, 438))

    #trees and objects
    all_sprites.add(Tree(1, 168, 176), Tree(1, 240, 176), Tree(1, 168, 420), Tree(1, 240, 420), Tree(1, 672, 420), Tree(1, 744, 420))

    all_sprites.add(Object(0, 522, 48), Object(1, 426, 224), Object(3, 462, 224), Object(1, 684, 224), Object(2, 720, 224), Object(2, 756, 224), Object(3, 792, 224))

    all_sprites.add(Tree(0, -36, 222), Tree(0, -36, 288))

    all_sprites.add(Tree(0, -60, -90), Tree(0, 40, -40), Tree(0, 190, -70), Tree(0, 360, -90), Tree(0, -20, 10), Tree(0, 130, -30),
                    Tree(0, 280, -65), Tree(0, 810, -60), Tree(0, 730, -50), Tree(0, 890, -20))

    #paths
    all_sprites.add(Path(3, 90, 309, 0))
    for i in range(9):
        path = Path(0, 102+i*102, 309, i*180)
        top = Path(1, 102+i*102, 297, 0)
        bot = Path(2, 102+i*102, 411, 0)
        all_sprites.add(path, top, bot)

    #add sprites to group
    for sprite in all_sprites:
        all_rects.append(sprite.rect)

    #place plants randomly
    plantCoords = [492, 8, 398, 88, 120, 245, 468, 86, 351, 97, 378, 255, 671, 10, 911, 260, 800, 94, 309, 441, 582, 0, 621, 17,
                   102, 130, 266, 101, 867, 249, 342, 250, 822, 428, 678, 60, 892, 144, 482, 45, 731, 94, 854, 91, 367, 138,
                   529, 2, 303, 88, 96, 439, 388, 437, 627, 440, 893, 450, 693, 201, 115, 276, 758, 196, 531, 42, 841, 130]
    for i in range(len(plantCoords)//2):
        index = random.randrange(37)
        x = plantCoords[2*i]
        y = plantCoords[2*i+1]
        all_sprites.add(Plant(index, x, y))

def screen_2():
    #paths
    for i in range(10):
        path = Path(0, i*102, 309, i*180)
        top = Path(1, i*102, 297, 0)
        bot = Path(2, i*102, 411, 0)
        all_sprites.add(path, top, bot)
    for i in range(4):
        path1 = Path(0, 240, 156+i*102, i*180)
        path2 = Path(0, 618, 156+i*102, i*180)
        if i == 0 or i == 3:
            left1 = Path(3, 228, 156+i*102, 0)
            right1 = Path(4, 342, 156+i*102, 0)
            left2 = Path(3, 606, 156+i*102, 0)
            right2 = Path(4, 720, 156+i*102, 0)
            all_sprites.add(path1, left1, right1, path2, left2, right2)
        elif i == 1:
            left1 = Path(8, 141, 210, 0)
            right1 = Path(7, 342, 210, 0)
            left2 = Path(8, 519, 210, 0)
            right2 = Path(7, 720, 210, 0)
            all_sprites.add(path1, path2, left1, right1, left2, right2)
        elif i == 2:
            left1 = Path(6, 141, 411, 0)
            right1 = Path(5, 342, 411, 0)
            left2 = Path(6, 519, 411, 0)
            right2 = Path(5, 720, 411, 0)
            all_sprites.add(path1, path2, left1, right1, left2, right2)
    all_sprites.add(Path(1, 240, 144, 0), Path(2, 240, 564, 0), Path(1, 618, 144, 0), Path(2, 618, 564, 0))

    #fences
    for i in range(3):
        for j in range(2):
            all_sprites.add(Object(1, -6+i*372, 240+j*160), Object(2, 30+i*372, 240+j*160), Object(2, 66+i*372, 240+j*160),
                            Object(2, 102+i*372, 240+j*160), Object(2, 138+i*372, 240+j*160), Object(3, 174+i*372, 240+j*160))

    #logos
    all_sprites.add(gameLogo(0, 291, 642), gameLogo(1, 291, 75))

#start screen
start_screen()
current_screen = 1

#player sprite
player = Player()
all_sprites.add(player)

running = True

clock = pygame.time.Clock()

while running:
    #end program if window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and not keys[pygame.K_s]:
        player.moveUp()
    if keys[pygame.K_s] and not keys[pygame.K_w]:
        player.moveDown()
    if keys[pygame.K_a] and not keys[pygame.K_d]:
        player.moveLeft()
    if keys[pygame.K_d] and not keys[pygame.K_a]:
        player.moveRight()
    if keys[pygame.K_SPACE]:
        player.game()

    #update position so animated sprites works
    player.x = player.rect.centerx
    player.y = player.rect.centery

    #update animation after a certain num of ticks
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= 80:
        player.animate()
        last_update = current_time
    if current_time - water_update >= 160:
        for tile in water:
            tile.animate()
        water_update = current_time

    #switch between screens
    if player.rect.left > width and current_screen == 1:
        all_sprites.empty()
        all_rects.clear()
        water.clear()
        screen_2()
        all_sprites.add(player)
        player.rect.x = 0
        current_screen = 2
    if player.rect.right < 0 and current_screen == 2:
        all_sprites.empty()
        start_screen()
        all_sprites.add(player)
        player.rect.right = width
        current_screen = 1

    #update screen
    all_sprites.update()
    player.flip()
    screen.fill(background)
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(30)

pygame.quit()
