import pygame


class Grid:
    """Решетка на игровом поле"""
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, screen):
        """Рисование решетки на игровом поле"""
        x = self.width/10
        y = self.height/20
        for i in range(10):
            cell = pygame.Rect(x*i, 0, 1, self.height)
            pygame.draw.rect(screen, (0, 125, 0), cell)
        for i in range(20):
            cell = pygame.Rect(0, y*i, self.width, 1)
            pygame.draw.rect(screen, (0, 100, 0), cell)
