import pygame
import sys
from player import Player
from level import load_level
from camera import Camera
from enemy import Enemy  # Импортируем класс врага

# Инициализация
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
SKY_BLUE = (135, 206, 235)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario Prototype - With Enemies & Clouds")
clock = pygame.time.Clock()

# Загружаем уровень
platforms, bushes = load_level()

# Создаем игрока
player = Player(100, 200)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Создаем группу врагов
enemies = pygame.sprite.Group()
enemy1 = Enemy(500, 200)
enemy2 = Enemy(900, 400)
enemies.add(enemy1, enemy2)

# Камера
camera = Camera(1600, 600)

# Загружаем фон неба
bg_image = pygame.image.load('fun (1) (1).jpg').convert()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump(platforms)

    # --- ОБНОВЛЕНИЕ ЛОГИКИ ---
    player.update(platforms)
    enemies.update(platforms)
    camera.update(player)

    # --- ПРОВЕРКА СТОЛКНОВЕНИЙ С ВРАГАМИ ---
    hit_enemies = pygame.sprite.spritecollide(player, enemies, False)
    for enemy in hit_enemies:
        if player.vel_y > 0 and player.rect.bottom <= enemy.rect.centery + 15:
            enemy.kill()
            player.vel_y = -12
        else:
            print("Враг ранил игрока!")
            player.rect.x = 100
            player.rect.y = 200

    # --- ОТРИСОВКА (теперь внутри цикла!) ---
    
    # 1. Сначала рисуем картинку фона
    screen.blit(bg_image, (0, 0))

    # 2. Рисуем статичные кусты (с учетом камеры)
    for bush in bushes:
        screen.blit(bush.image, camera.apply(bush))

    # 3. Затем рисуем платформы
    for p in platforms:
        screen.blit(p.image, camera.apply(p))

    # 4. Враги
    for enemy in enemies:
        screen.blit(enemy.image, camera.apply(enemy))

    # 5. Игрок
    screen.blit(player.image, camera.apply(player))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()