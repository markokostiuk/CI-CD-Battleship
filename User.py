from Field import Field
from DraggableEllipse import DraggableEllipse
import random
import pygame
import numpy as np

class User:
    def __init__(self, name):
        self.name = name
        self.playerField = Field()
        self.hiddenField = Field()
        self.ships = self.create_ships()


    def create_ship(self, size, x, y, count):
        ellipses = []
        for i in range(count):
            ellipses.append(DraggableEllipse(x, y, size, (0, 0, 0), self))
            x += size * 40
        return ellipses

    # отримання усього набору кораблів
    def create_ships(self):
        ships = self.create_ship(4, 100, 180, 1)
        ships.extend(self.create_ship(3, 100, 230, 2))
        ships.extend(self.create_ship(2, 100, 280, 3))
        ships.extend(self.create_ship(1, 100, 330, 4))
        return ships

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def placeShip(self, position, rotate):
        field = self.playerField.getField()

        for dot in position:
            if field[dot[0]][dot[1]] != 0:
                return field, "the ship is intersect with another ship"

        for dot in position:
            field[dot[0]][dot[1]] = 1

        if rotate == 0:
            for i in range(position[0][0] - 1, position[0][0] + 2):
                for j in range(position[0][1] - 1, position[-1][1] + 2):
                    if 0 <= i <= 9 and 0 <= j <= 9:
                        if field[i][j] != 1:
                            field[i][j] -= 1
        elif rotate == 90:
            for i in range(position[0][0] - 1, position[-1][0] + 2):
                for j in range(position[0][1] - 1, position[0][1] + 2):
                    if 0 <= i <= 9 and 0 <= j <= 9:
                        if field[i][j] != 1:
                            field[i][j] -= 1

        self.playerField.setField(field)
        print(field, "ADDED")
        return field, "the ship is placed on the playing field"

    def deleteShip(self, position, rotate):
        field = self.playerField.getField()

        for dot in position:
            if field[dot[0]][dot[1]] != 1:
                return field, "there is no ship"

        for dot in position:
            field[dot[0]][dot[1]] = 0

        if rotate == 0:
            for i in range(position[0][0] - 1, position[0][0] + 2):
                for j in range(position[0][1] - 1, position[-1][1] + 2):
                    if 0 <= i <= 9 and 0 <= j <= 9:
                        if field[i][j] != 0:
                            field[i][j] += 1
        elif rotate == 90:
            for i in range(position[0][0] - 1, position[-1][0] + 2):
                for j in range(position[0][1] - 1, position[0][1] + 2):
                    if 0 <= i <= 9 and 0 <= j <= 9:
                        if field[i][j] != 0:
                            field[i][j] += 1

        self.playerField.setField(field)
        print(field, "DELETED")
        return self.playerField, "the ship was deleted"

    def clearField(self):
        for ship in self.ships:
            ship.rect.x = ship.start_x
            ship.rect.y = ship.start_y
            ship.rotate = 90
            ship.rotateShip()
            ship.updateShipPosition()
            ship.status = ""
            ship.x = ship.start_x
            ship.y = ship.start_y

        self.playerField.clearField()

    def randomPlacement(self):
        self.clearField()

        field = self.playerField.getField()

        for ship in self.ships:
            status = ""

            while status != "the ship is placed on the playing field":
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                rotate = random.choice([0, 90])

                position = []

                if rotate == 0:
                    if col + ship.size - 1 > 9:
                        continue
                if rotate == 90:
                    if row + ship.size - 1 > 9:
                        continue

                for i in range(ship.size):
                    if rotate == 0:
                        position.append((row, col + i))
                    if rotate == 90:
                        position.append((row + i, col))

                field, status = self.placeShip(position, rotate)

                if status == "the ship is placed on the playing field":
                    ship.status = status
                    ship.rotate = rotate
                    ship.x = row
                    ship.y = col

                    # ship.updateShipPosition()
                    ship.position = position

                    if rotate == 90:
                        ship.rect = pygame.Rect((ship.y * 40) + 670, (ship.x * 40) + 170, 40, ship.size * 40 - 10)

                    if rotate == 0:
                        ship.rect = pygame.Rect((ship.y * 40) + 670, (ship.x * 40) + 170, ship.size * 40 - 10, 40)

    def shoot(self, x, y):
        field = self.hiddenField.getField()

        if self.playerField.getField()[x][y] != 1:
            field[x][y] = 10
            self.hiddenField.setField(field)
            return

        for ship in self.ships:
            if (x, y) in ship.position:
                ship.number_of_hits += 1

                if ship.number_of_hits == ship.size:
                    for dot in ship.position:
                        field[dot[0]][dot[1]] = 2

                    if ship.rotate == 0:
                        for i in range(ship.x - 1, ship.x + 2):
                            for j in range(ship.y - 1, ship.position[-1][1] + 2):
                                if 0 <= i <= 9 and 0 <= j <= 9:
                                    if field[i][j] != 2:
                                        field[i][j] = 10
                    elif ship.rotate == 90:
                        for i in range(ship.x - 1, ship.position[-1][0] + 2):
                            for j in range(ship.y - 1, ship.y + 2):
                                if 0 <= i <= 9 and 0 <= j <= 9:
                                    if field[i][j] != 2:
                                        field[i][j] = 10
                else:
                    field[x][y] = 1

                self.hiddenField.setField(field)

                bool_arr = (field == 2)
                if np.count_nonzero(bool_arr) == 20:
                    return "loose"
                return







    def getShips(self):
        """повертає усі кораблі: dict"""
        return self.ships
