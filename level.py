import pygame
import os  # Импортируем os для работы с путями

TILE_SIZE = 40  # Размер одного блока в пикселях

LEVEL_MAP = [
    # Добавляем пустые строки сверху, чтобы опустить уровень ниже:
    "----------------------------------------",
    "----------------------------------------",
    "----------------------------------------",
    "----------------------------------------",
    "----------------------------------------", 
    # Старые строки уровня:
    "-                                      -",
    "-                   ###                -",
    "-                                      -",
    "-         ###             ####       -",  # Добавили кустик 'b'
    "-                                      -",
    "-                                      -",
    "-    #####                       ##### -",
    "-       b            bbb           b        -",
    "########################################",
    "########################################",  # Земля теперь окажется ниже
]

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Пытаемся загрузить текстуру земли/камня
        full_path = os.path.join('dirt.png.webp')
        
        try:
            # Загружаем картинку и масштабируем под размер блока (TILE_SIZE x TILE_SIZE)
            tile_image = pygame.image.load(full_path).convert()
            self.image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
        except (pygame.error, FileNotFoundError) as e:
            # Резервный вариант: если файл не найден, рисуем коричневый квадрат
            print(f"Не удалось загрузить 'dirt.png.webp': {e}")
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill((120, 80, 50))  # Коричневый цвет земли
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Bush(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 50
        self.height = 30
        
        # Пытаемся загрузить картинку куста
        full_path = os.path.join('bush.png')
        try:
            img = pygame.image.load(full_path).convert_alpha()
            self.image = pygame.transform.scale(img, (self.width, self.height))
        except (pygame.error, FileNotFoundError):
            # Резервный куст, если файла нет
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, (34, 139, 34), (0, 10, 50, 20))
            pygame.draw.ellipse(self.image, (46, 139, 87), (10, 0, 30, 20))
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + (TILE_SIZE - self.height)


def load_level():
    platforms = pygame.sprite.Group()
    bushes = pygame.sprite.Group()  # Создаем группу для кустов
    x = 0
    y = 0
    for row in LEVEL_MAP:
        for col in row:
            if col == "#":
                block = Block(x, y)
                platforms.add(block)
            elif col == "b":
                bush = Bush(x, y)
                bushes.add(bush)
            x += TILE_SIZE
        y += TILE_SIZE
        x = 0
    return platforms, bushes  # Возвращаем ровно два значения, как и ждет main.py