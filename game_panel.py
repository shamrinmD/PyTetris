import pygame
from colors import Color


class Panel:
    """Игровая панель"""
    def __init__(self):
        self.next = None
        self.font = pygame.font.SysFont('arial', 32)

    def draw(self, screen, figure, score, record):
        """Рисование игровой панели"""
        pygame.draw.rect(screen, Color().black, (402, 0, 400, 280))
        screen.blit(self.font.render("SCORE {}".format(score), True, Color().green), (450, 40))
        screen.blit(self.font.render("RECORD {}".format(record), True, Color().green), (450, 180))
        self.next = figure(490, 600)
        self.next.color = Color().green
        screen.blit(self.font.render("Next figure", True, Color().white), (470, 520))
        self.next.draw(screen)
