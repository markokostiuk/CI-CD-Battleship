import numpy as np

class Field():
    """клас Поле - при ініціалізації створює матрицю 10*10 заповнену нулями - пустотою"""

    def __init__(self):
        # створюємо матрицю (ігрове поле), заповнюємо нулями, що означатимуть порожнє поле
        self.field = np.full((10, 10), 0, dtype=int)

    def getField(self):
        """повертає поточне поле"""
        return self.field

    def setField(self, field):
        """оновлює поле"""
        self.field = field

    def clearField(self):
        self.setField(np.full((10, 10), 0, dtype=int))
