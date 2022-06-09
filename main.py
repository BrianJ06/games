import pygame
import random
pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
background = (116, 200, 87)

last_update = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.spritesheet = pygame.image.load("C:/Users/rando/Downloads/mystic_woods_free_v0.2/sprites/characters/slime.png")
        self.sprites = []

        self.makeSprite(6, 46, 20, 10)
        self.makeSprite(42, 40, 12, 16)
        self.makeSprite(74, 38, 12, 18)
        self.makeSprite(104, 41, 16, 15)
        self.makeSprite(136, 44, 16, 12)
        self.makeSprite(168, 45, 16, 11)

        self.x = 128
        self.y = 192
        self.direction = 'right'
        self.lastDirection = 'right'
        self.speed = 4

        self.index = 0
        self.image = self.sprites[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (153, 335)

    def makeSprite(self, x, y, w, h):
        sprite = pygame.Surface([40, 36], pygame.SRCALPHA, 32)
        sprite.blit(self.spritesheet, ((40-w)/2, 36-h), (x, y, w, h))
        sprite = pygame.transform.scale(sprite, (80, 72))
        self.sprites.append(sprite)

    def moveUp(self):
        self.rect.centery -= self.speed
    def moveDown(self):
        self.rect.centery += self.speed
    def moveLeft(self):
        self.lastDirection = self.direction
        self.rect.centerx -= self.speed
        self.direction = 'left'
    def moveRight(self):
        self.lastDirection = self.direction
        self.rect.centerx += self.speed
        self.direction = 'right'

    def animate(self):
        if self.index == len(self.sprites)-1:
            self.index = 0
        else:
            self.index += 1

        self.image = self.sprites[self.index]
        self.rect = self.image.get_rect()

        self.rect.centerx = self.x
        self.rect.centery = self.y

    def flip(self):
        if self.lastDirection != self.direction:
            for sprite in self.sprites:
                sprite.blit(pygame.transform.flip(sprite, True, False), sprite.get_rect())


class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.spritesheet = None

    def makeSprite(self, list, x, y, w, h):
        sprite = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        sprite.blit(self.spritesheet, (0, 0), (x, y, w, h))
        sprite = pygame.transform.scale(sprite, (3 * w, 3 * h))
        list.append(sprite)


class Path(Sprite):
    def __init__(self, index, x, y, angle):
        super().__init__()

        self.spritesheet = pygame.image.load("C:/Users/rando/Downloads/First Asset pack.png")

        self.path = []
        self.makeSprite(self.path, 217, 157, 34, 34)    # path
        self.makeSprite(self.path, 217, 92, 34, 4)      # top
        self.makeSprite(self.path, 217, 60, 34, 4)      # bottom
        self.makeSprite(self.path, 248, 61, 4, 34)      # left
        self.makeSprite(self.path, 216, 61, 4, 34)      # right
        self.makeSprite(self.path, 216, 60, 34, 34)     # top left
        self.makeSprite(self.path, 218, 60, 34, 34)     # top right
        self.makeSprite(self.path, 216, 62, 34, 34)     # bottom left
        self.makeSprite(self.path, 218, 62, 34, 34)     # bottom right

        self.image = self.path[index]
        if angle != None:
            self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Cliff(Sprite):
    def __init__(self, index, x, y):
        super().__init__()

        self.spritesheet = pygame.image.load("C:/Users/rando/Downloads/First Asset pack.png")

        self.cliff = []
        self.makeSprite(self.cliff, 83, 246, 24, 18)    # horizontal
        self.makeSprite(self.cliff, 107, 246, 24, 32)   # slope down
        self.makeSprite(self.cliff, 131, 246, 24, 32)   # slope up

        self.image = self.cliff[index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Tree(Sprite):
    def __init__(self, index, x, y):
        super().__init__()

        self.spritesheet = pygame.image.load("C:/Users/rando/Downloads/First Asset pack.png")

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

        self.spritesheet = pygame.image.load("C:/Users/rando/Downloads/First Asset pack.png")

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

        self.spritesheet = pygame.image.load("C:/Users/rando/Downloads/First Asset pack.png")

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

#start screen
width = 960
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Home')

all_sprites = pygame.sprite.Group()
all_rects = []

all_sprites.add(Path(3, 90, 309, 0))
for i in range(9):
    path = Path(0, 102+i*102, 309, i*180)
    top = Path(1, 102+i*102, 297, 0)
    bot = Path(2, 102+i*102, 411, 0)
    all_sprites.add(path, top, bot)

all_sprites.add(Cliff(2, 0, 180), Cliff(0, 72, 180), Cliff(2, 144, 138), Cliff(0, 216, 138), Cliff(1, 288, 138), Cliff(0, 360, 180), Cliff(2, 432, 138),
                Cliff(2, 504, 96), Cliff(0, 576, 96), Cliff(1, 648, 96), Cliff(0, 720, 138), Cliff(1, 792, 138), Cliff(0, 864, 180), Cliff(2, 936, 138))

all_sprites.add(Tree(1, 168, 176), Tree(1, 240, 176))

all_sprites.add(Object(0, 522, 48), Object(1, 426, 224), Object(3, 462, 224), Object(1, 684, 224), Object(2, 720, 224), Object(2, 756, 224), Object(3, 792, 224))

for sprite in all_sprites:
    all_rects.append(sprite.rect)

for i in range(30):
    index = random.randrange(37)
    x = random.randrange(0, 924)
    y = random.randrange(0, 400)
    plant = Plant(index, x, y)
    while plant.rect.collidelist(all_rects) != -1:
        x = random.randrange(0, 924)
        y = random.randrange(0, 400)
        plant = Plant(index, x, y)
    all_sprites.add(plant)
    all_rects.append(plant.rect)


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
    player.dx = 0
    player.dy = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and not keys[pygame.K_s]:
        player.moveUp()
    elif keys[pygame.K_s] and not keys[pygame.K_w]:
        player.moveDown()
    if keys[pygame.K_a] and not keys[pygame.K_d]:
        player.moveLeft()
    if keys[pygame.K_d] and not keys[pygame.K_a]:
        player.moveRight()

    player.x = player.rect.centerx
    player.y = player.rect.centery

    current_time = pygame.time.get_ticks()
    if current_time - last_update >= 80:
        player.animate()
        last_update = current_time

    #update screen
    all_sprites.update()
    player.flip()
    screen.fill(background)
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(30)

pygame.quit()