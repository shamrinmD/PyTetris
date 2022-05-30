

class Button:
    """Кнопки в меню"""

    def __init__(self, x, y, text, font, color, hover_color):
        self.x = x
        self.y = y
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_input = self.font.render(self.text, True, self.color)
        self.rect_text = self.text_input.get_rect(center=(self.x, self.y))

    def update(self, screen):
        screen.blit(self.text_input, self.rect_text)

    def check_for_input(self, position):
        """Проверка на нажатие кнопки"""
        if position[0] in range(self.rect_text.left, self.rect_text.right) and position[1] in \
                range(self.rect_text.top, self.rect_text.bottom):
            return True
        return False

    def change_color(self, position):
        """Изменение цвета кнопки при наведении курсора мыши"""
        if position[0] in range(self.rect_text.left, self.rect_text.right) and position[1] in \
                range(self.rect_text.top, self.rect_text.bottom):
            self.text_input = self.font.render(self.text, True, self.hover_color)
        else:
            self.text_input = self.font.render(self.text, True, self.color)
