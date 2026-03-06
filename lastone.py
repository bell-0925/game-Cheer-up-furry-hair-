import pygame as pg
import random
from random import choice
from os import path

# SETTINGS
# game options/settings
TITLE = "Jumpy"
WIDTH = 1600
HEIGHT = 900
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"

# 이미지시도
current_path = path.dirname(__file__)
image_path = path.join(current_path, "img")

# Player properties
PLAYER_ACC = 3.5
PLAYER_FRICTION = -0.2
PLAYER_GRAVITY = 1.2
PLAYER_JUMP = 25

# main platform
PLATFORM_MAIN=[(0,HEIGHT)]
# Starting platforms
PLATFORM_LIST = [
                 (WIDTH/2, HEIGHT/2),
                 (WIDTH-50, HEIGHT - 60),
                 (WIDTH/2 - 50, HEIGHT*3/4),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE

# SPRITES

vec = pg.math.Vector2

class Spritesheet:
    # Utility class for loading spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # Grab an image out of a lager spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width//2, height//2))
        return image
    
    def get_image2(self, x, y, width, height):
        # Grab an image out of a lager spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width, height))
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0

        self.load_images()
        self.image = self.standing_frames[0]

        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)

        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(320, 94, 120, 200),
                                self.game.spritesheet.get_image(0, 294, 120, 200)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)

        self.walk_frames_r = [self.game.spritesheet.get_image(120, 294, 120, 200),
                              self.game.spritesheet.get_image(240, 294, 120, 200)]
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)

        self.walk_frames_l = [pg.transform.flip(frame, True, False)
                              for frame in self.walk_frames_r]

        self.jump_frame = self.game.spritesheet.get_image(200, 94, 120, 200)
        self.jump_frame.set_colorkey(BLACK)

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 0.1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 0.1
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x*PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5*self.acc

        if self.pos.x > WIDTH + self.rect.width/2:
            self.pos.x = 0 - self.rect.width/2
        if self.pos.x < 0 - self.rect.width/2:
            self.pos.x = WIDTH + self.rect.width/2

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()

        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = ((self.current_frame + 1)
                                      % len(self.walk_frames_l))

                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom

        if not self.jumping and not self.walking:
            if (now - self.last_update) > 350:
                self.last_update = now
                self.current_frame = ((self.current_frame + 1)
                                      % len(self.standing_frames))
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game

        images = [self.game.spritesheet.get_image(0 ,0 ,380 ,94),
                  self.game.spritesheet.get_image(0, 94, 200, 100)]


        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Platform2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game

        images = [self.game.spritesheet.get_image2(0, 288, WIDTH, HEIGHT),
                  self.game.spritesheet.get_image2(213, 1662, WIDTH, HEIGHT)]

        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Boss(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(path.join(image_path, "kunai.png"))       

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (10, HEIGHT/2)  
        self.pos = vec(10,random.randrange(10, HEIGHT-10))  
        self.vel = vec(0, 0)                                        
        self.acc = vec(0, 0)       
        
    def update(self):                                                   # 키다운 이벤트
            self.acc = vec(PLAYER_GRAVITY,0)

            self.acc.y += self.vel.y*PLAYER_FRICTION
            self.vel += self.acc
            self.pos += self.vel + 0.5*self.acc

            if self.pos.y > HEIGHT:
                self.pos.y = HEIGHT
            if self.pos.y < 0:
                self.pos.y = 0

            if self.pos.x > WIDTH -10 or self.pos.x < 10:
                self.vel.x*=-1

            self.rect.midbottom = self.pos

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(path.join(image_path, "arrow.png"))       

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, 10)
        self.random=random.seed(random.randrange(0,WIDTH))
        self.pos = vec(random.randrange(10,WIDTH-10),10)  
        self.vel = vec(0, 0)                                        
        self.acc = vec(0, 0)       
        
    def update(self):                                                   # 키다운 이벤트
            self.acc = vec(0, PLAYER_GRAVITY)

            self.acc.x += self.vel.x*PLAYER_FRICTION
            self.acc.y=random.uniform(0.0,1.0)
            self.vel += self.acc
            self.pos += self.vel + 0.5*self.acc
            if self.pos.x > WIDTH:
                self.pos.x = WIDTH
            if self.pos.x < 0:
                self.pos.x = 0

            self.rect.midbottom = self.pos  

class Coin(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(path.join(image_path, "gold.png"))       

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (10, HEIGHT/2)  
        self.pos = vec(random.randrange(10,WIDTH-10),random.randrange(100,HEIGHT-600))  
        self.vel = vec(0, 0)                                         
        self.acc = vec(0, 0)       
        
    def update(self):                                                   
            self.acc = vec(PLAYER_GRAVITY,0)

            if self.pos.y > HEIGHT:
                self.pos.y = HEIGHT
            if self.pos.y < 0:
                self.pos.y = 0

            if self.pos.x > WIDTH -10 or self.pos.x < 10:
                self.vel.x*=-1

            self.rect.midbottom = self.pos
            
               
# MAIN
class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
        self.boss=Boss()
        self.enemy=Enemy()
        self.coin=Coin()
        self.platform_change_time = 10000/2  
        self.time_since_last_plat = 0 
        self.boss_spawn_time = 10000/4 # 보스가 출현할 시간 간격 (30초)
        self.time_since_last_boss = 0  # 마지막 보스 출현 후 경과 시간
        self.enemy_spawn_time = 10000/10 # 보스가 출현할 시간 간격 (30초)
        self.time_since_last_enemy = 0  # 마지막 보스 출현 후 경과 시간
        self.coin_spawn_time = 10000/4 # 보스가 출현할 시간 간격 (30초)
        self.time_since_last_coin = 0  # 마지막 보스 출현 후 경과 시간
        
    def load_data(self):
        # Load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        try:
            with open(path.join(self.dir, HS_FILE), 'r') as f:
                self.highscore = int(f.read())
        except FileNotFoundError:
            self.highscore = 0

        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.play=pg.sprite.Group()
        self.group=pg.sprite.Group()
        self.coingroup=pg.sprite.Group() 
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.play.add(self.player)

        for p in PLATFORM_MAIN:
            plat=Platform2(self, *p)
            self.all_sprites.add(plat)
            self.platforms.add(plat)
        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            self.score += 1

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platfrom
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.y < lowest.rect.centery:
                    self.player.pos.y = lowest.rect.top + 0.1
                    self.player.vel.y = 0
                    self.player.jumping = False

        #if self.player.rect > 0:
        #    damage = pg.sprite.spritecollide(self.player, self.boss, False)
        #    if damage:
        #        self.plater.rect < damage[0]
                    
        dt = self.clock.tick(FPS)  # 시간 간격
        self.time_since_last_plat += dt
        if self.time_since_last_plat >= self.platform_change_time:
            self.time_since_last_plat = 0  # 시간 리셋
            skip=True
            for plat in self.platforms:
                if skip:
                    skip=False
                    continue
                plat.kill() 
        self.time_since_last_boss += dt
        if self.time_since_last_boss >= self.boss_spawn_time:
            self.boss.kill() 
            self.time_since_last_boss = 0  # 시간 리셋
            for i in range(1,3):
                self.boss=Boss()
                self.all_sprites.add(self.boss)  # 보스를 스프라이트 그룹에 추가
                self.group.add(self.boss)
    
        self.time_since_last_enemy += dt
        if self.time_since_last_enemy >= self.enemy_spawn_time:
            self.enemy.kill()
            self.time_since_last_enemy = 0  # 시간 리셋
            for i in range(6):
                self.enemy=Enemy()
                self.group.add(self.enemy)
                self.all_sprites.add(self.enemy) 

        self.time_since_last_coin += dt
        if self.time_since_last_coin >= self.boss_spawn_time:
            self.coin.kill() 
            self.time_since_last_coin = 0  # 시간 리셋
            for i in range(2):
                self.coin=Coin()
                self.all_sprites.add(self.coin)  # 코인을 스프라이트 그룹에 추가
                self.coingroup.add(self.coin)
    
            
            
        # Die
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if self.player.pos.y == 600:
            self.playing = False

        #충돌 감지 후 플레이 종료
        if pg.sprite.spritecollide(self.player,self.group,True):
            self.playing=False

        
        if pg.sprite.spritecollide(self.player,self.coingroup,True):
             self.score += 100
        

        # Spawn new platforms
        while len(self.platforms) < 16:
            width = random.randrange(50, 100)
            p = Platform(self, random.randrange(0, WIDTH - width), random.randrange(0, HEIGHT))
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        # Game Loop - Events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # Game Loop - Draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score), 22, WHITE, WIDTH/2, 15)

        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Arrows to move, Space to jump",
                       22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play",
                       22, WHITE, WIDTH/2, HEIGHT*3/4)
        self.draw_text("High Score : " + str(self.highscore),
                       22, WHITE, WIDTH/2, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Score : " + str(self.score),
                       22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play again",
                       22, WHITE, WIDTH/2, HEIGHT*3/4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!",
                           22, WHITE, WIDTH/2, HEIGHT/2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score : " + str(self.highscore),
                           22, WHITE, WIDTH/2, 15)

        pg.display.flip()
        self.wait_for_close()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
    def wait_for_close(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    waiting = False
                    self.running=False
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()        