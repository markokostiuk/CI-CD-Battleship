import pygame


# Приклад класу корабля
class DraggableEllipse:

    # Ініціалізація
    def __init__(self, x, y, size, color):
        # Координати голови корабля (для правильного спавну на початковому екрані та правильного розрахунку всіх точок)
        self.x = x
        self.y = y
        self.rotate = 0
        self.position = []
        self.size = size
        # Створення прямокутника для малювання в ньому еліпса
        self.rect = pygame.Rect(x, y, size * 40 - 10, 40)
        self.color = color
        self.dragging = False


    # Малювання еліпса
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect, 3)


    # Знаходження координат на сітці
    def getShipPosition(self):
        position = []
        for point in range(self.size):
            if self.rotate == 0:
                position.append((self.x + point, self.y))
            elif self.rotate == 90:
                position.append((self.x, self.y + point))

        # Перевірка, щоб корабель був у межах сітки 10x10
        if all(0 <= point[0] <= 9 and 0 <= point[1] <= 9 for point in position):
            self.position = position
        else:
            self.position = []


    # Поворот корябля
    def rotateShip(self):
        if self.rotate == 0:
            self.rotate = 90
            self.rect = pygame.Rect(self.rect.x, self.rect.y, 40, self.size * 40 - 10)
        elif self.rotate == 90:
            self.rotate = 0
            self.rect = pygame.Rect(self.rect.x, self.rect.y, self.size * 40 - 10, 40)
        self.getShipPosition()


    # Оновлення положення корабля при перетаскуванні
    def update(self):
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Окргулення координат для вирівнювання на полі
            self.rect.x = round(mouse_x / 5) * 5
            self.rect.y = round(mouse_y / 5) * 5
            # 650 та 150 - це координати першої комірки на полі. Таким чином встановлюються точки від 0 до 9
            self.x = (self.rect.x - 650) // 40
            self.y = (self.rect.y - 150) // 40
            self.getShipPosition()
            print(self.position)
