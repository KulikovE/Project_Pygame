import os
import sys
import pygame
import random
import time

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
sound1 = pygame.mixer.Sound('data/nachalo.wav')
udar = pygame.mixer.Sound('data/udar.wav')
udar_sten = pygame.mixer.Sound('data/udar_sten.wav')
proigr = pygame.mixer.Sound('data/Proigr.wav')
win = pygame.mixer.Sound('data/win.wav')
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
pygame.display.set_caption('Ping-pong')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# создадим группу, содержащую все спрайты
all_sprites = pygame.sprite.Group()
igrok = pygame.sprite.Group()
igrok2 = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders_l = pygame.sprite.Group()
vertical_borders_r = pygame.sprite.Group()
nachal = pygame.sprite.Group()
# создадим спрайт
sprite = pygame.sprite.Sprite()
sprite_nach = pygame.sprite.Sprite()
sprite_vich = pygame.sprite.Sprite()
# sprite1 = pygame.sprite.Sprite()
# определим его вид
sprite.image = load_image("sprite.png")
sprite_nach.image = load_image("Nachat.png", -1)
sprite_vich.image = load_image("Vihod.png", -1)
# sprite1.image = load_image("sprite.png")
# и размерыё
sprite_nach.rect = sprite_nach.image.get_rect()
sprite_vich.rect = sprite_vich.image.get_rect()
sprite_nach.rect.x = 100
sprite_nach.rect.y = 100
sprite_vich.rect.x = 100
sprite_vich.rect.y = 300
sprite.rect = sprite.image.get_rect()
sprite.rect.x = 50
# sprite1.rect = sprite.image.get_rect()
# sprite1.rect.x = 570
# добавим спрайт в группу
igrok.add(sprite)
nachal.add(sprite_nach)
nachal.add(sprite_vich)
chet_r, chet_l = 0, 0
pobeditel = 0


# igrok.add(sprite1)


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y, spec_shar):
        super().__init__(all_sprites)
        self.radius = radius
        self.spec_shar = spec_shar
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        if spec_shar == 0:
            pygame.draw.circle(self.image, pygame.Color("red"),
                               (radius, radius), radius)
        else:
            pygame.draw.circle(self.image, pygame.Color("black"),
                               (radius, radius), 3)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-2, -1, 1, 2])
        self.ras_y = 700
        self.kon = 0
        self.raz_dv = 0
        self.udar = 0

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
            if self.spec_shar == 0:
                udar_sten.play()
        if pygame.sprite.spritecollideany(self, vertical_borders_l) and self.spec_shar == 0:
            self.kon = 1
            self.konec()
            global chet_r
            proigr.play()
            chet_r += 1
            global pobeditel
            global zapusk_igr
            global pobed_ec
            if chet_r == 5:
                pobeditel = 0
                zapusk_igr = False
                pobed_ec = True
        if pygame.sprite.spritecollideany(self, vertical_borders_r) and self.spec_shar == 0:
            self.kon = 1
            self.konec()
            global chet_l
            win.play()
            chet_l += 1
            if chet_l == 5:
                pobeditel = 1
                zapusk_igr = False
                pobed_ec = True
        if pygame.sprite.spritecollideany(self, igrok) and self.spec_shar == 0:
            self.vx = (-self.vx) + 0.1
            udar.play()
            self.udar = 1
        if pygame.sprite.spritecollideany(self, igrok2) and self.spec_shar == 0:
            self.vx = (-self.vx) - 0.1
            udar.play()
        if self.spec_shar == 1 and self.rect.x > 550 and self.rect.x < 565:
            self.ras_y = self.rect.y
            self.raz_dv = 1

    def konec(self):
        self.rect.x = 300
        self.rect.y = 300
        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-2, -1, 1, 2])

    def get_speed(self):
        return self.vx, self.vy

    def sk_dop_sh(self, vx, vy, x, y):
        self.rect.x = x
        self.rect.y = y
        self.vx = vx * 6
        self.vy = vy * 6
        # print(self.vx, self.vy)


#        self.ras_y = 700


class Palka2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(igrok2)
        self.image = pygame.Surface((17, 130), pygame.SRCALPHA)
        pygame.draw.rect(self.image, pygame.Color("white"),
                         (0, 0, 6, 130))
        self.rect = pygame.Rect((x, y, 6, 130))
        # self.vx = random.randint(-5, 5)
        # self.vy = random.randrange(-5, 5)

    def update(self, p):
        if self.rect.y > p and self.rect.y > 5:
            self.rect = self.rect.move(0, -1)
        if self.rect.y < p and self.rect.y < 450:
            self.rect = self.rect.move(0, 1)


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            if x1 < 200:
                self.add(vertical_borders_l)
                self.image = pygame.Surface([1, y2 - y1])
                self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
            else:
                self.add(vertical_borders_r)
                self.image = pygame.Surface([1, y2 - y1])
                self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


def draw_chet(chet_l, chet_r):
    font = pygame.font.Font(None, 100)
    chet = str(chet_l) + '   |   ' + str(chet_r)
    text = font.render(chet, True, (100, 255, 100))
    screen.blit(text, (215, 100))


pobed_ec = False
running = True
Border(5, 5, width - 5, 5)
Border(5, height - 5, width - 5, height - 5)
Border(50, 5, 50, height - 5)
Border(width - 45, 5, width - 45, height - 5)
pal = Palka2(550, 300)
shar = Ball(20, 300, 300, 0)
dop_shar = Ball(20, 300, 300, 1)
vx_s, vy_s = shar.get_speed()
dop_shar.vx, dop_shar.vy = vx_s * 6, vy_s * 6
fps = 60
clock = pygame.time.Clock()
peremesh = 300
zapusk_igr = True
sl = 0  # задержка после пройгрыша

while running:
    Mouse_x, Mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            zapusk_igr = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if (x >= 105 and x <= 520) and (y >= 105 and y <= 250):
                running = False
                sound1.play()
            if (x >= 105 and x <= 520) and (y >= 305 and y <= 455):
                running = False
                zapusk_igr = False
    screen.fill((0, 0, 0))
    nachal.draw(screen)
    pygame.display.flip()

while zapusk_igr:
    shar.update()
    dop_shar.update()
    if shar.kon == 1:
        vx_s, vy_s = shar.get_speed()
        dop_shar.sk_dop_sh(vx_s, vy_s, 300, 300)
        shar.kon = 0
        time.sleep(0.5)
        sl = 1
    if shar.udar == 1:
        vx_s, vy_s = shar.get_speed()
        dop_shar.sk_dop_sh(vx_s, vy_s, shar.rect.x, shar.rect.y)
        shar.udar = 0
    if dop_shar.raz_dv == 1:
        peremesh = dop_shar.ras_y  # Перемещение игрока 2 в расчитанный y
        dop_shar.raz_dv = 0
        # while sprite1.rect.y != peremesh:
    pal.update(peremesh - 65)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            zapusk_igr = False
    if pygame.key.get_pressed()[pygame.K_DOWN] and sprite.rect.y < 450:
        sprite.rect.y += 2
        # sprite1.rect.y = sprite.rect.y
    if pygame.key.get_pressed()[pygame.K_UP] and sprite.rect.y > 0:
        sprite.rect.y -= 2
        # sprite1.rect.y = sprite.rect.y
    clock.tick(fps)
    screen.fill((0, 0, 0))
    draw_chet(chet_l, chet_r)
    all_sprites.draw(screen)
    igrok.draw(screen)
    igrok2.draw(screen)
    pygame.display.flip()
    if sl == 1:
        time.sleep(1)
        sl = 0
while pobed_ec:
    screen.fill((0, 0, 0))
    if pobeditel == 0:
        font = pygame.font.Font(None, 65)
        chet = 'Победил компьютер'
        text = font.render(chet, True, (255, 255, 100))
        screen.blit(text, (20, 100))
    else:
        font = pygame.font.Font(None, 65)
        chet = 'Победил игрок'
        text = font.render(chet, True, (100, 255, 100))
        screen.blit(text, (20, 100))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pobed_ec = False
    pygame.display.flip()
pygame.quit()
