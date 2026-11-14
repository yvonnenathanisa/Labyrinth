from pygame import*

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_width - 80:
            self.rect.y += self.speed

class Enemy1(GameSprite):
    direction = "left"
    def update(self): 
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy2(GameSprite):
    direction = "right"
    def update(self): 
        if self.rect.x <= 300:
            self.direction = "left"
        if self.rect.x >= win_width - 45:
            self.direction = "right"
        if self.direction == "right":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Walls(sprite.Sprite):
    def __init__(self,color_1,color_2,color_3,wall_x,wall_y,wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.wall_width = wall_width
        self.wall_height = wall_height
        self.image = Surface((self.wall_width, self.wall_height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Labyrinth")
background = transform.scale(image.load("Pyramid.jpg"), (win_width, win_height))

Falcon = Player('hero_1.png', 5, win_height - 80, 5)
Vulture = Enemy1('villian.png', win_width - 80, 280, 2)
Raven = Enemy2('Raven.png', win_width - 80, 280, 4)
treasure = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

w1 = Walls(255, 244, 224, 70, 20, 450, 10)
w2 = Walls(255, 244, 224, 100, 100, 350, 10)
w3 = Walls(255, 244, 224, 50, 20, 10, 380)

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
font = font.Font (None, 70)
win = font.render('YOU WIN!', True, (2, 195, 81))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

mixer.init()
mixer.music.load("Music_backgound.mp3")
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background,(0,0))
        Falcon.update()
        Vulture.update()
        Raven.update()
        Falcon.reset()
        Vulture.reset()
        Raven.reset()
        treasure.reset()

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()

        if sprite.collide_rect(Falcon, Raven) or sprite.collide_rect(Falcon, Vulture) or sprite.collide_rect(Falcon, w1) or sprite.collide_rect(Falcon, w2) or sprite.collide_rect(Falcon, w3):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()

        if sprite.collide_rect(Falcon, treasure):
            finish = True
            window.blit(win, (200, 200))
            money.play()

    display.update()
    clock.tick(FPS)
