import pygame
import os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 36
        self.height = 36
        
        # Пытаемся загрузить картинку врага (если нет — будет фиолетовый квадрат)
        full_path = os.path.join('enemy.png.webp')
        try:
            img = pygame.image.load(full_path).convert_alpha()
            self.image = pygame.transform.scale(img, (self.width, self.height))
        except pygame.error:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((200, 50, 200))  # Фиолетовый цвет для врага по умолчанию
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 2         # Скорость движения врага
        self.direction = 1     # 1 — движется вправо, -1 — влево
        self.vel_y = 0
        self.gravity = 0.8

    def update(self, platforms):
        # 1. Движение по горизонтали
        self.rect.x += self.speed * self.direction

        # Проверка коллизий со стенами (чтобы враг разворачивался при ударе о блок)
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.direction > 0:
                    self.rect.right = p.rect.left
                    self.direction = -1  # Меняем направление на левое
                elif self.direction < 0:
                    self.rect.left = p.rect.right
                    self.direction = 1   # Меняем направление на правое

        # 2. Гравитация и вертикальные коллизии (чтобы враг стоял на платформах)
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