import pygame
import random
import copy
from colors import Color


class Figures:
    """Класс фигур на игровом поле"""
    def __init__(self, width, height):
        self.s_collide = pygame.mixer.Sound('sounds/collide.mp3')
        self.s_break = pygame.mixer.Sound('sounds/break.mp3')
        self.figures = []
        self.tetramino = {0: QTetra, 1: ITetra, 2: LTetra, 3: JTetra, 4: TTetra, 5: ZTetra, 6: STetra}
        self.next_tetra = random.randint(0, 6)
        self.border_bottom = pygame.Rect(0, height, width, 1)
        self.border_left = pygame.Rect(-1, 0, 1, height)
        self.border_right = pygame.Rect(width, 0, 2, height)
        self.offset = 0
        self.count_lines = 0
        self.score = 0
        self.scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    def add(self):
        """Добавление фигуры в список"""
        self.figures.append(self.tetramino[self.next_tetra]())
        self.check_lines()
        self.next_tetra = random.randint(0, 6)

    def draw(self, screen):
        """Рисование границ игрового поля и фигур"""
        pygame.draw.rect(screen, Color().green, self.border_bottom)
        pygame.draw.rect(screen, Color().green, self.border_left)
        pygame.draw.rect(screen, Color().green, self.border_right)
        for figure in self.figures:
            figure.draw(screen)

    def fall(self, speed):
        """Падение фигуры"""
        last_figure = copy.deepcopy(self.figures[-1].blocks)  # Копирование последней фигуры
        self.figures[-1].fall(speed)  # Вызов падения на последней фигуре
        if self.border_bottom.collidelist(self.figures[-1].blocks) != -1:  # Столкновение с нижней границей
            self.figures[-1].blocks = last_figure
            self.add()
        elif self.check_collision():
            self.figures[-1].blocks = last_figure
            self.s_collide.play()
            self.add()

    def rotation(self):
        """Поворот фигуры"""
        last_figure = copy.deepcopy(self.figures[-1].blocks)
        self.figures[-1].rotation(0)
        if self.check_collision():
            self.figures[-1].blocks = copy.deepcopy(last_figure)
        self.offset = self.get_offset()
        for figure in self.figures[-1].blocks:
            figure.x -= self.offset

    def move(self, key):
        """Движение фигуры в стороны"""
        last_figure = copy.deepcopy(self.figures[-1].blocks)
        self.figures[-1].move(key)
        if self.border_bottom.collidelist(self.figures[-1].blocks) != -1:
            self.figures[-1].blocks = last_figure
        elif self.border_left.collidelist(self.figures[-1].blocks) != -1:
            self.figures[-1].blocks = last_figure
        elif self.border_right.collidelist(self.figures[-1].blocks) != -1:
            self.figures[-1].blocks = last_figure
        elif self.check_collision():
            self.figures[-1].blocks = last_figure

    def get_offset(self):
        """Расчет смещения
        Возвращает максимальное значение, на которое будет
        перемещена фигура, если она торчит по правому краю окна

        """
        max_offset = 0
        for figure in self.figures[-1].blocks:
            if figure.x >= self.border_right.x:
                elements = figure.x - self.border_right.x + self.figures[-1].size
                if elements > max_offset:
                    max_offset = elements
        return max_offset

    def check_collision(self):
        """Проверка коллизий"""
        for figure in self.figures[:-1]:
            for block in figure.blocks:
                if block.collidelist(self.figures[-1].blocks) != -1:
                    return True
        return False

    def check_lines(self):
        """Проверка собранных линий и их удаление"""
        size_block = self.figures[-1].size
        lines = []  # Список, содержащий строки для elfktybz
        self.count_lines = 0

        for i in range(20):
            rect = pygame.Rect(0, i*size_block + 20, 400, 1)
            lines.append(rect)  # Линия проверки ряда
        count = 0

        for rect in lines:
            for figure in self.figures:
                for block in figure.blocks:
                    if rect.colliderect(block):
                        count += 1
            list_remove = []  # Cписок, в котором хранятся элементы для удаления

            if count >= 10:  # Удаление объектов, содержащихся в списке удаления
                for figure in self.figures:
                    for block in figure.blocks:
                        if rect.colliderect(block):  # Если блок контактирует с линией проверки
                            list_remove.append(block)  # то он добавляется в список удаления
                    for j in list_remove:
                        if j in figure.blocks:
                            figure.blocks.remove(j)

            if count >= 10:  # Смещение всех блоков над удаленной линией вниз
                for figure in self.figures:
                    for block in figure.blocks:
                        if block.y < rect.y:
                            block.move_ip(0, 40)
                self.count_lines += 1
                self.s_break.play()
            count = 0
        self.score += self.scores[self.count_lines]

    def check_top(self):
        """Проверка достижения верхней границы игрового поля"""
        for figure in self.figures[:-1]:
            for block in figure.blocks:
                if block.y < 0:
                    return True
        return False


class Tetromino:
    """Класс блоков фигур на игровом поле"""
    def __init__(self, x=0, y=0):
        self.size = 40
        if x == 0 and y == 0:
            self.x = self.size*3
            self.y = -self.size
        else:
            self.x = x
            self.y = y
        self.blocks = []
        self.turn = 0
        self.color = Color().color[random.randint(2, 8)]

    def add(self, x, y):
        """Добавления блока фигуры"""
        self.blocks.append(pygame.Rect(x, y, self.size, self.size))

    def draw(self, screen):
        """Рисование блока фигуры"""
        for block in self.blocks:
            pygame.draw.rect(screen, self.color, block)

    def move(self, key):
        """Движение блока в стороны"""
        if key[pygame.K_LEFT]:
            for block in self.blocks:
                block.move_ip(-self.size, 0)
        elif key[pygame.K_RIGHT]:
            for block in self.blocks:
                block.move_ip(self.size, 0)

    def fall(self, speed):
        """Падения блока фигуры"""
        for block in self.blocks:
            block.move_ip(0, speed)


class QTetra(Tetromino):
    """Фигура Q"""
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.add(self.x, self.y)
        self.add(self.x + self.size, self.y)
        self.add(self.x, self.y + self.size)
        self.add(self.x + self.size, self.y + self.size)

    def rotation(self, offset):
        pass


class ITetra(Tetromino):
    """Фигура I"""
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.add(self.x, self.y)
        self.add(self.x, self.y + self.size)
        self.add(self.x, self.y + self.size*2)
        self.add(self.x, self.y + self.size*3)

    def rotation(self, offset):
        """Повороты фигуры I"""
        if self.turn == 0:
            for i in range(len(self.blocks)):
                self.blocks[i].move_ip(i*self.size - offset, -i*self.size)
        elif self.turn == 1:
            for i in range(len(self.blocks)):
                self.blocks[i].move_ip(-i*self.size - offset, i*self.size)
        self.turn += 1
        if self.turn >= 2:
            self.turn = 0


class LTetra(Tetromino):
    """Фигура L"""
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        for i in range(3):
            self.add(self.x, self.y + i*self.size)
        self.add(self.x + self.size, self.y + self.size*2)

    def rotation(self, offset):
        """Повороты фигуры L"""
        if self.turn == 0:
            self.blocks[0].move_ip(2*self.size, 0)
            self.blocks[1].move_ip(1*self.size, -self.size)
            self.blocks[2].move_ip(0, -2*self.size)
            self.blocks[3].move_ip(-self.size, -self.size)
        elif self.turn == 1:
            self.blocks[0].move_ip(-self.size, 2*self.size)
            self.blocks[1].move_ip(0, self.size)
            self.blocks[2].move_ip(self.size, 0)
            self.blocks[3].move_ip(0, -self.size)
        elif self.turn == 2:
            self.blocks[0].move_ip(-self.size, -self.size)
            self.blocks[1].move_ip(0, 0)
            self.blocks[2].move_ip(self.size, self.size)
            self.blocks[3].move_ip(2*self.size, 0)
        elif self.turn == 3:
            self.blocks[0].move_ip(0, -self.size)
            self.blocks[1].move_ip(-self.size, 0)
            self.blocks[2].move_ip(-2*self.size, self.size)
            self.blocks[3].move_ip(-self.size, 2*self.size)
        self.turn += 1
        if self.turn > 4:
            self.turn = 0


class JTetra(Tetromino):
    """Фигура J"""
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        for i in range(3):
            self.add(self.x + self.size, self.y + i*self.size)
        self.add(self.x, self.y + self.size*2)

    def rotation(self, offset):
        """Повороты фигуры J"""
        if self.turn == 0:
            self.blocks[0].move_ip(self.size, 2*self.size)
            self.blocks[1].move_ip(0, self.size)
            self.blocks[2].move_ip(-self.size, 0)
            self.blocks[3].move_ip(0, -self.size)
        elif self.turn == 1:
            self.blocks[0].move_ip(-self.size*2, 0)
            self.blocks[1].move_ip(-self.size, -self.size)
            self.blocks[2].move_ip(0, -self.size*2)
            self.blocks[3].move_ip(self.size, -self.size)
        elif self.turn == 2:
            self.blocks[0].move_ip(0, -self.size*2)
            self.blocks[1].move_ip(self.size, -self.size)
            self.blocks[2].move_ip(self.size*2, 0)
            self.blocks[3].move_ip(self.size, self.size)
        elif self.turn == 3:
            self.blocks[0].move_ip(self.size, 0)
            self.blocks[1].move_ip(0, self.size)
            self.blocks[2].move_ip(-self.size, 2*self.size)
            self.blocks[3].move_ip(-2*self.size, self.size)
        self.turn += 1
        if self.turn > 4:
            self.turn = 0


class TTetra(Tetromino):
    """Фигура T"""
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        for i in range(3):
            self.add(self.x + i*self.size, self.y)
        self.add(self.x + self.size, self.y + self.size)

    def rotation(self, offset):
        """Повороты фигуры T"""
        if self.turn == 0:
            self.blocks[0].move_ip(self.size, 0)
            self.blocks[1].move_ip(0, self.size)
            self.blocks[2].move_ip(-self.size, 2*self.size)
            self.blocks[3].move_ip(-self.size, 0)
        elif self.turn == 1:
            self.blocks[0].move_ip(self.size, self.size)
            self.blocks[1].move_ip(0, 0)
            self.blocks[2].move_ip(-self.size, -self.size)
            self.blocks[3].move_ip(self.size, -self.size)
        elif self.turn == 2:
            self.blocks[0].move_ip(-self.size, self.size)
            self.blocks[1].move_ip(0, 0)
            self.blocks[2].move_ip(self.size, -self.size)
            self.blocks[3].move_ip(self.size, self.size)
        elif self.turn == 3:
            self.blocks[0].move_ip(-self.size, -2*self.size)
            self.blocks[1].move_ip(0, -self.size)
            self.blocks[2].move_ip(self.size, 0)
            self.blocks[3].move_ip(-self.size, 0)
        self.turn += 1
        if self.turn > 4:
            self.turn = 0


class ZTetra(Tetromino):
    """Фигура Z"""
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.add(self.x, self.y)
        self.add(self.x + self.size, self.y)
        self.add(self.x + self.size, self.y + self.size)
        self.add(self.x + 2*self.size, self.y + self.size)

    def rotation(self, offset):
        """Повороты фигуры Z"""
        if self.turn == 0:
            self.blocks[0].move_ip(self.size, 0)
            self.blocks[1].move_ip(0, self.size)
            self.blocks[2].move_ip(-self.size, 0)
            self.blocks[3].move_ip(-2*self.size, self.size)
        elif self.turn == 1:
            self.blocks[0].move_ip(-self.size, 0)
            self.blocks[1].move_ip(0, -self.size)
            self.blocks[2].move_ip(+self.size, 0)
            self.blocks[3].move_ip(2*self.size, -self.size)
        self.turn += 1
        if self.turn > 1:
            self.turn = 0


class STetra(Tetromino):
    """Фигура S"""
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.add(self.x + self.size*2, self.y)
        self.add(self.x + self.size, self.y)
        self.add(self.x + self.size, self.y + self.size)
        self.add(self.x, self.y + self.size)

    def rotation(self, offset):
        """Повороты фигуры S"""
        if self.turn == 0:
            self.blocks[0].move_ip(-self.size, self.size*2)
            self.blocks[1].move_ip(0, self.size)
            self.blocks[2].move_ip(-self.size, 0)
            self.blocks[3].move_ip(0, -self.size)
        elif self.turn == 1:
            self.blocks[0].move_ip(self.size, -self.size*2)
            self.blocks[1].move_ip(0, -self.size)
            self.blocks[2].move_ip(self.size, 0)
            self.blocks[3].move_ip(0, self.size)
        self.turn += 1
        if self.turn > 1:
            self.turn = 0
