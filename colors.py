

class Color:
    """Цвета, используемые в игровом процессе"""
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)
        self.light_blue = (0, 255, 255)
        self.purple = (153, 51, 251)
        self.orange = (255, 128, 0)
        self.color = {0: self.black, 1: self.white, 2: self.red, 3: self.green, 4: self.blue, 5: self.yellow,
                      6: self.light_blue, 7: self.purple, 8: self.orange}
