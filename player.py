import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 32
        self.height = 48
        
        # Загружаем кадры анимации
        try:
            # Кадр стояния (на месте)
            self.image_idle = pygame.transform.scale(
                pygame.image.load(os.path.join('player2.png')).convert_alpha(), 
                (self.width, self.height)
            )
            # Кадры ходьбы
            self.walk_frames = [
                pygame.transform.scale(pygame.image.load(os.path.join('walk1.png')).convert_alpha(), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load(os.path.join('walk2.png')).convert_alpha(), (self.width, self.height))
            ]
        except pygame.error as e:
            print(f"Ошибка загрузки кадров анимации: {e}")
            # Резервный вариант, если файлов нет
            self.image_idle = pygame.Surface((self.width, self.height))
            self.image_idle.fill((230, 50, 50))
            self.walk_frames = [self.image_idle, self.image_idle]

        self.image = self.image_idle
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Физика
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.8
        self.jump_strength = -17
        self.speed = 5

        # Переменные для анимации
        self.anim_index = 0      # Текущий номер кадра ходьбы
        self.anim_speed = 6      # Скорость смены кадров (чем меньше цифра, тем быстрее идет)
        self.anim_counter = 0    # Счетчик времени для смены кадров
        self.facing_right = True # Куда смотрит персонаж (True — вправо, False — влево)

    def update(self, platforms):
        # 1. Считывание клавиш и определение движения
        self.vel_x = 0
        keys = pygame.key.get_pressed()
        is_moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.facing_right = False
            is_moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
            self.facing_right = True
            is_moving = True

        # --- ЛОГИКА АНИМАЦИИ ---
        # Проверяем, стоит ли персонаж на земле и движется ли он
        is_on_ground = self.check_ground(platforms)

        if is_moving and is_on_ground:
            # Увеличиваем счетчик кадров
            self.anim_counter += 1
            if self.anim_counter >= self.anim_speed:
                self.anim_counter = 0
                # Переключаемся на следующий кадр ходьбы (циклично: 0 -> 1 -> 0 -> 1...)
                self.anim_index = (self.anim_index + 1) % len(self.walk_frames)
            
            current_image = self.walk_frames[self.anim_index]
        else:
            # Если стоит на месте или в воздухе — показываем обычную статичную картинку
            current_image = self.image_idle
            self.anim_index = 0

        # Если персонаж смотрит налево, зеркально отражаем картинку по горизонтали
        if not self.facing_right:
            self.image = pygame.transform.flip(current_image, True, False)
        else:
            self.image = current_image
        # -----------------------

        # 2. Движение по X и коллизии со стенами
        self.rect.x += self.vel_x
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_x > 0:
                    self.rect.right = p.rect.left
                elif self.vel_x < 0:
                    self.rect.left = p.rect.right

        # 3. Гравитация и движение по Y
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                elif self.vel_y < 0:
                    self.rect.top = p.rect.bottom
                    self.vel_y = 0

    def check_ground(self, platforms):
        # Вспомогательный метод: проверяет, стоит ли персонаж на земле
        self.rect.y += 2
        hit = False
        for p in platforms:
            if self.rect.colliderect(p.rect):
                hit = True
        self.rect.y -= 2
        return hit

    def jump(self, platforms):
        if self.check_ground(platforms):
            self.vel_y = self.jump_strength