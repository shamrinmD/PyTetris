

class Record:
    """Хранение рекорда"""
    def __init__(self):
        self.record = 0
        with open('save.txt', 'r') as save_file:
            self.record = int(save_file.readline())

    def check_record(self, score):
        """Проверка новых рекордов"""
        if score > self.record:
            self.record = score
            with open('save.txt', 'w') as file:
                file.write(str(self.record))
