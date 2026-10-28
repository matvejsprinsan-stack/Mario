import pygame

class Camera:
    def __init__(self, width, height):
        self.dx = 0
        self.dy = 0
        self.width = width
        self.height = height

    def apply(self, entity):
        # Возвращает прямоугольник объекта со смещением для отрисовки,
        # не меняя его реальных физических координат в игре
        return entity.rect.move(self.dx, self.dy)

    def update(self, target):
        # Центрируем камеру по игроку (экран 800px, значит середина — 400px)
        self.dx = -target.rect.centerx + 400
        self.dy = 0  # По вертикали камеру пока держим на месте

        # Ограничение: не даем камере уйти за левый край карты (меньше 0)
        if self.dx > 0:
            self.dx = 0