import pygame

class DraggableEllipse:
    def __init__(self, x, y, size, color):
        # Инициализация объекта
        self.x = x
        self.y = y
        self.rotate = 0
        self.position = []
        self.size = size
        # Создание прямоугольника для отрисовки эллипса
        self.rect = pygame.Rect(x, y, size * 40 - 10, 40)
        self.color = color
        self.dragging = False

    def draw(self, screen):
        # Отрисовка эллипса
        pygame.draw.ellipse(screen, self.color, self.rect, 3)

    def getShipPosition(self):
        # Вычисление координат корабля на сетке
        position = []
        for point in range(self.size):
            if self.rotate == 0:
                position.append((self.x + point, self.y))
            elif self.rotate == 90:
                position.append((self.x, self.y + point))

        # Проверка, чтобы корабль не выходил за пределы поля 10x10
        if all(0 <= point[0] <= 9 and 0 <= point[1] <= 9 for point in position):
            self.position = position
        else:
            self.position = []

    def rotateShip(self):
        # Поворот корабля и обновление его положения
        if self.rotate == 0:
            self.rotate = 90
            self.rect = pygame.Rect(self.rect.x, self.rect.y, 40, self.size * 40 - 10)
        elif self.rotate == 90:
            self.rotate = 0
            self.rect = pygame.Rect(self.rect.x, self.rect.y, self.size * 40 - 10, 40)
        self.getShipPosition()

    def update(self):
        # Обновление положения корабля при перетаскивании
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Огругление координат для выравнивания по сетке
            self.rect.x = round(mouse_x / 5) * 5
            self.rect.y = round(mouse_y / 5) * 5
            self.x = (self.rect.x - 650) // 40
            self.y = (self.rect.y - 150) // 40
            self.getShipPosition()
            print(self.position)
