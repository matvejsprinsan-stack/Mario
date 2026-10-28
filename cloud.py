import pygame
import random

class Cloud(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        # Создаем белое облако с помощью эллипсов или прямоугольников (если нет картинки)
        self.image = pygame.Surface((120, 50), pygame.SRCALPHA)
        # Рисуем пушистое облако из кругов/эллипсов
        pygame.draw.ellipse(self.image, (255, 255, 255, 220), (0, 15, 80, 35))
        pygame.draw.ellipse(self.image, (255, 255, 255, 220), (30, 0, 70, 45))
        pygame.draw.ellipse(self.image, (255, 255, 255, 220), (60, 15, 60, 35))
        
        self.rect = self.image.get_rect()
        # Случайная позиция по вертикали в верхней части экрана
        self.rect.x = random.randint(screen_width, screen_width + 500)
        self.rect.y = random.randint(30, 200)
        
        # Медленная скорость движения облака
        self.speed = random.uniform(0.5, 1.5)
        self.screen_width = screen_width

    def update(self):
        # Облако плывет влево
        self.rect.x -= self.speed
        
        # Если облако уплыло за левый край экрана — переносим его вправо
        if self.rect.right < 0:
            self.rect.x = self.screen_width + random.randint(50, 200)
            self.rect.y = random.randint(30, 200)
            self.speed = random.uniform(0.5, 1.5)