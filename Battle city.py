import os
import sys
import pygame
import pyglet

pygame.init()
size = WIDTH, HEIGHT = 650, 650
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
o = 1
o2 = 4
FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    f = 1
    image = load_image('main1.png')
    fon = pygame.transform.scale(image, (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == 13 and f == 2:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if f > 1:
                    f -= 1
                image = load_image(f'main{f}.png')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if f < 3:
                    f += 1             
                image = load_image(f'main{f}.png')
            fon = pygame.transform.scale(image, (WIDTH, HEIGHT))  
            screen.blit(fon, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)
        
        
def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))     


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {'wall': pygame.transform.scale(load_image('wall.png'), (50, 50)),
               'bricks': pygame.transform.scale(load_image('bricks.png'), (50, 50)),
               'water': pygame.transform.scale(load_image('water.png'), (50, 50)),
               'empty': pygame.transform.scale(load_image('fon.png'), (50, 50)),
               'trees': pygame.transform.scale(load_image('trees.png'), (50, 50))}

player_image = pygame.transform.scale(load_image('tank1.png'), (50, 50))
player_image2 = pygame.transform.scale(load_image('tank2b.png'), (50, 50))


tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)  


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)       
        
    def update(self):
        global o
        oldx = self.rect.x
        oldy = self.rect.y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 50
            self.image = pygame.transform.scale(load_image('tank1l.png'), (50, 50))
            o = 3
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 50
            self.image = pygame.transform.scale(load_image('tank1.png'), (50, 50))
            o = 2
        elif keys[pygame.K_UP]:
            self.rect.y -= 50
            self.image = pygame.transform.scale(load_image('tank1.png'), (50, 50))
            o = 1
        elif keys[pygame.K_DOWN]:
            self.rect.y += 50 
            self.image = pygame.transform.scale(load_image('tank1b.png'), (50, 50))
            o = 4
        x = pygame.sprite. spritecollideany(self, tiles_group)
        if x != None:
            if x.image == tile_images['wall'] or x.image == tile_images['water'] or x.image == tile_images['bricks'] or\
               pygame.sprite.spritecollideany(self, player_group2): 
                self.rect.x, self.rect.y = oldx, oldy
            if x.image != tile_images['trees']:
                if o == 1:
                    self.image = pygame.transform.scale(load_image('tank1.png'), (50, 50))
                elif o == 2:
                    self.image = pygame.transform.scale(load_image('tank1r.png'), (50, 50))
                elif o == 3:
                    self.image = pygame.transform.scale(load_image('tank1l.png'), (50, 50))
                elif o == 4:
                    self.image = pygame.transform.scale(load_image('tank1b.png'), (50, 50)) 
            else:
                self.image = pygame.transform.scale(load_image('tank_in_trees.png') , (50, 50))           
    
    def die(self):
        global die
        self.image = pygame.transform.scale(load_image('die.png'), (50, 50))    
        die.play()
            
            
class Player2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group2)
        self.image = pygame.transform.scale(load_image('tank2b.png'), (50, 50))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)       
        
    def update(self):
        global o2
        oldx = self.rect.x
        oldy = self.rect.y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 25
            self.image = pygame.transform.scale(load_image('tank2l.png'), (50, 50))
            o2 = 3
        elif keys[pygame.K_d]:
            self.rect.x += 25
            self.image = pygame.transform.scale(load_image('tank2r.png'), (50, 50))
            o2 = 2
        elif keys[pygame.K_w]:
            self.rect.y -= 25
            self.image = pygame.transform.scale(load_image('tank2.png'), (50, 50))
            o2 = 1
        elif keys[pygame.K_s]:
            self.rect.y += 25
            self.image = pygame.transform.scale(load_image('tank2b.png'), (50, 50))
            o2 = 4
        x = pygame.sprite.spritecollideany(self, tiles_group)
        if x != None:
            if x.image == tile_images['wall'] or x.image == tile_images['water'] or x.image == tile_images['bricks'] or\
               pygame.sprite.spritecollideany(self, player_group):
                self.rect.x, self.rect.y = oldx, oldy
            if x.image != tile_images['trees']:
                if o2 == 1:
                    self.image = pygame.transform.scale(load_image('tank2.png'), (50, 50))
                elif o2 == 2:
                    self.image = pygame.transform.scale(load_image('tank2r.png'), (50, 50))
                elif o2 == 3:
                    self.image = pygame.transform.scale(load_image('tank2l.png'), (50, 50))
                elif o2 == 4:
                    self.image = pygame.transform.scale(load_image('tank2b.png'), (50, 50)) 
            else:
                self.image = pygame.transform.scale(load_image('tank2_in_trees.png') , (50, 50))  
                
    def die(self):
        global die
        self.image = pygame.transform.scale(load_image('die.png'), (50, 50)) 
        die.play()
            
            
player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player_group2 = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
bullet_group2 = pygame.sprite.Group()

def generate_level(level):
    new_player, x, y = None, None, None   
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y) 
            elif level[y][x] == '+':
                Tile('bricks', x, y)   
            elif level[y][x] == '=':
                Tile('water', x, y)  
            elif level[y][x] == '-':
                Tile('trees', x, y)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '1':
                Tile('empty', x, y)
                new_player = Player(x, y)
                new_player.add(player_group)
            elif level[y][x] == '2':
                Tile('empty', x, y)
                new_player2 = Player2(x, y)
                new_player2.add(player_group2)
    return new_player, new_player2, x, y


class BulletP1(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, o):
        super().__init__(bullet_group, all_sprites)
        self.x, self.y = pos_x, pos_y
        self.o = o
        if o == 1:
            self.image = pygame.transform.scale(load_image('bullet.png'), (10, 10))
        elif o == 2:
            self.image = pygame.transform.scale(load_image('bulletr.png'), (10, 10))
        elif o == 3:
            self.image = pygame.transform.scale(load_image('bulletl.png'), (10, 10))
        elif o == 4:
            self.image = pygame.transform.scale(load_image('bulletb.png'), (10, 10))        
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 20, tile_height * pos_y + 20) 
        
    def check(self):
        x = pygame.sprite.spritecollideany(self, tiles_group)
        if x == None:
            return True
        if x.image == tile_images['wall'] or x.image == tile_images['bricks'] or\
           pygame.sprite.spritecollideany(self, player_group2) or pygame.sprite.spritecollide(self, bullet_group2, True): 
            if x.image == tile_images['bricks']:
                x.kill()
                if self.o == 2:
                    Tile('empty', (self.rect.x + 30) // 50, (self.rect.y - 20) // 50)
                elif self.o == 4:
                    Tile('empty', (self.rect.x - 20) // 50, (self.rect.y + 30) // 50)
                else:
                    Tile('empty', (self.rect.x - 20) // 50, (self.rect.y - 20) // 50)
            if pygame.sprite.spritecollideany(self, player_group2):
                self.die()
            return False
        if x.image != tile_images['trees']:
            if self.o == 1:
                self.image = pygame.transform.scale(load_image('bullet.png'), (10, 10))
            elif self.o == 2:
                self.image = pygame.transform.scale(load_image('bulletr.png'), (10, 10))
            elif self.o == 3:
                self.image = pygame.transform.scale(load_image('bulletl.png'), (10, 10))
            elif self.o == 4:
                self.image = pygame.transform.scale(load_image('bulletb.png'), (10, 10)) 
        else:
            self.image = load_image('bullet_in_trees.png') 
        return True
        
    def update(self):
        if self.check():
            if self.o == 1:
                self.rect.y -= 10
            elif self.o == 2:
                self.rect.x += 10
            elif self.o == 3:
                self.rect.x -= 10
            elif self.o == 4:
                self.rect.y += 10
        else:
            self.kill()
            
    def die(self):
        global player2
        player2.die()        
        end_screen(1)    
            
            
class BulletP2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, o2):
        super().__init__(bullet_group2, all_sprites)
        self.x, self.y = pos_x, pos_y
        self.o2 = o2
        if o2 == 1:
            self.image = pygame.transform.scale(load_image('bullet.png'), (10, 10))
        elif o2 == 2:
            self.image = pygame.transform.scale(load_image('bulletr.png'), (10, 10))
        elif o2 == 3:
            self.image = pygame.transform.scale(load_image('bulletl.png'), (10, 10))
        elif o2 == 4:
            self.image = pygame.transform.scale(load_image('bulletb.png'), (10, 10))        
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 20, tile_height * pos_y + 20) 
        
    def check(self):
        x = pygame.sprite.spritecollideany(self, tiles_group)
        if x == None:
            return True
        if x.image == tile_images['wall'] or x.image == tile_images['bricks'] or\
           pygame.sprite.spritecollideany(self, player_group) or pygame.sprite.spritecollide(self, bullet_group, True): 
            if x.image == tile_images['bricks']:
                x.kill()
                if self.o2 == 2:
                    Tile('empty', (self.rect.x + 30) // 50, (self.rect.y - 20) // 50)
                elif self.o2 == 4:
                    Tile('empty', (self.rect.x - 20) // 50, (self.rect.y + 30) // 50)
                else:
                    Tile('empty', (self.rect.x - 20) // 50, (self.rect.y - 20) // 50)  
            if pygame.sprite.spritecollideany(self, player_group):
                self.die()
            return False
        if x.image != tile_images['trees']:
            if self.o2 == 1:
                self.image = pygame.transform.scale(load_image('bullet.png'), (10, 10))
            elif self.o2 == 2:
                self.image = pygame.transform.scale(load_image('bulletr.png'), (10, 10))
            elif self.o2 == 3:
                self.image = pygame.transform.scale(load_image('bulletl.png'), (10, 10))
            elif self.o2 == 4:
                self.image = pygame.transform.scale(load_image('bulletb.png'), (10, 10)) 
        else:
            self.image = load_image('bullet_in_trees.png')         
        return True
        
    def update(self):
        if self.check():
            if self.o2 == 1:
                self.rect.y -= 10
            elif self.o2 == 2:
                self.rect.x += 10
            elif self.o2 == 3:
                self.rect.x -= 10
            elif self.o2 == 4:
                self.rect.y += 10
        else:
            self.kill()
    
    def die(self):
        global player
        player.die()
        end_screen(2)
               
               
def end_screen(num):
    clock.tick(2)
    if num == 1:
        image = load_image('gameover1.png')  
    else:
        image = load_image('gameover2.png')
    fon = pygame.transform.scale(image, (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()   
    


start_screen()
start = pyglet.media.load('Начало.wav', streaming=False)
shoot = pyglet.media.load('Выстрел.wav', streaming=False)
die = pyglet.media.load('Смерть.wav', streaming=False)
start.play()
player, player2, level_x, level_y = generate_level(load_level('level1.txt'))
running = True
fps = 50
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False     
        if event.type == pygame.KEYDOWN and event.key == 13:
            bullet = BulletP1(player.rect.x // 50, player.rect.y // 50, o)
            bullet.add(bullet_group)
            shoot.play()
        if event.type == pygame.KEYDOWN and event.key == 32:
            bullet2 = BulletP2(player2.rect.x // 50, player2.rect.y // 50, o2)
            bullet2.add(bullet_group2) 
            shoot.play()
        player_group.update()
        player_group2.update()
    screen.fill((0, 255, 0))
    all_sprites.update()
    all_sprites.draw(screen)
    player_group.draw(screen)
    player_group2.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
terminate()