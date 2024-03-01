import numpy as np

class Field():
    """class Field - when initialized, creates a 10*10 matrix filled with zeros - empty"""

    def __init__(self):
        # Create a matrix (playing field), fill it with zeros, which will mean an empty field
        self.field = np.full((10, 10), 0, dtype=int)

    def get_field(self):
        """returns the current field"""
        return self.field

    def set_field(self, field):
        """updates the field"""
        self.field = field

    def clear_field(self):
        self.set_field(np.full((10, 10), 0, dtype=int))
