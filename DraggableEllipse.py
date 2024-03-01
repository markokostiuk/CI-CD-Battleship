import pygame
import copy

# Приклад класу корабля
class DraggableEllipse:

    # Ініціалізація
    def __init__(self, x, y, size, color, user):
        # Координати голови корабля (для правильного спавну на початковому екрані та правильного розрахунку всіх точок)
        self.x = x
        self.y = y
        self.start_x = copy.deepcopy(x)
        self.start_y = copy.deepcopy(y)
        self.rotate = 0
        self.position = []
        self.size = size
        self.number_of_hits = 0
        # Створення прямокутника для малювання в ньому еліпса
        self.rect = pygame.Rect(x, y, size * 40 - 10, 40)
        self.color = color
        self.dragging = False
        self.status = ""
        self.user = user

    def get_ship_position(self):
        return self.position

    # Малювання еліпса
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect, 3)


    # Знаходження координат на сітці
    def updateShipPosition(self):
        position = []
        for point in range(self.size):
            if self.rotate == 0:
                position.append((self.x, self.y + point))
            elif self.rotate == 90:
                position.append((self.x + point, self.y))

        # Перевірка, щоб корабель був у межах сітки 10x10
        if all(0 <= point[0] <= 9 and 0 <= point[1] <= 9 for point in position):
            self.position = position
        else:
            self.position = []


    # Поворот корябля
    def rotateShip(self):
        if len(self.position) != 0:
            self.user.deleteShip(self.position, self.rotate)

        if self.rotate == 0:
            self.rotate = 90
            self.rect = pygame.Rect(self.rect.x, self.rect.y, 40, self.size * 40 - 10)
        elif self.rotate == 90:
            self.rotate = 0
            self.rect = pygame.Rect(self.rect.x, self.rect.y, self.size * 40 - 10, 40)

        self.updateShipPosition()

        if len(self.position) != 0:
            self.user.placeShip(self.position, self.rotate)


    # Оновлення положення корабля при перетаскуванні
    def update(self):
        # if self.random:
        #     return

        if self.dragging:
            self.random = False

            if self.status == "the ship is placed on the playing field":
                field, self.status = self.user.deleteShip(self.position, self.rotate)
                if self.status == "the ship was deleted":
                    self.status = ""

            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Окргулення координат для вирівнювання на полі
            self.rect.x = round(mouse_x / 5) * 5
            self.rect.y = round(mouse_y / 5) * 5
            # 650 та 150 - це координати першої комірки на полі. Таким чином встановлюються точки від 0 до 9
            self.x = (self.rect.x - 650) // 40
            self.y = (self.rect.y - 150) // 40
            self.updateShipPosition()
        else:
            if self.status == "the ship is placed on the playing field":
                return

            if len(self.position) == 0:
                self.rect.x = self.start_x
                self.rect.y = self.start_y
                self.updateShipPosition()
                self.status = ""
                return

            field, self.status = self.user.placeShip(self.position, self.rotate)

            if self.status != "the ship is placed on the playing field":
                self.rect.x = self.start_x
                self.rect.y = self.start_y
                self.updateShipPosition()
                self.status = ""
                return
            self.updateShipPosition()
