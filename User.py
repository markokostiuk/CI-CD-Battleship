from Field import Field
from DraggableEllipse import DraggableEllipse
import random
import pygame
import numpy as np


class User:
    def __init__(self, name):
        self.__name = name

        self.__playerField = Field()
        self.__hiddenField = Field()

        self.__ships = self.create_ships()

        self.__comp_killMode = False

        self.__comp_startDamagedPoints = None

        self.__comp_extremeDamagedPoints = []

        self.__comp_lastDamagedRotate = None

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
        return self.__name

    def setName(self, name):
        self.__name = name

    def placeShip(self, position, rotate):
        field = self.__playerField.getField()

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

        self.__playerField.setField(field)
        return field, "the ship is placed on the playing field"

    def deleteShip(self, position, rotate):
        field = self.__playerField.getField()

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

        self.__playerField.setField(field)
        return field, "the ship was deleted"

    def clearField(self):
        for ship in self.getShips():
            ship.rect.x = ship.start_x
            ship.rect.y = ship.start_y
            ship.rotate = 90
            ship.rotateShip()
            ship.updateShipPosition()
            ship.status = ""
            ship.x = ship.start_x
            ship.y = ship.start_y

        self.__playerField.clearField()

    def randomPlacement(self):
        self.clearField()

        field = self.__playerField.getField()

        for ship in self.getShips():
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

    def getShips(self):
        """повертає усі кораблі: dict"""
        return self.__ships

    def getHiddenField(self):
        return self.__hiddenField.getField()


    def checkShip(self, row, col, field):
        print(f"в {self.getName()} стреляют в ({row}, {col})")
        status = ""
        # якщо промазали - позначаємо 10кою
        if self.__playerField.getField()[row][col] != 1:
            print("промазали\n")
            field[row][col] = 10
            status = "missed"
        # якщо попали
        else:
            for ship in self.getShips():
                if (row, col) in ship.position:
                    ship.number_of_hits += 1

                    # перевіряємо, чи остаточно знищили корабель
                    # якщо остаточно - вимикаємо режим знищення, позначаємо його як знищений та позначаємо навколо нього порожню зону
                    if ship.number_of_hits == ship.size:
                        print("убили\n")
                        self.__comp_killMode = False
                        self.__comp_lastDamagedRotate = None
                        self.__comp_startDamagedPoints = None
                        self.__comp_extremeDamagedPoints = []

                        for dot in ship.position:
                            field[dot[0]][dot[1]] = 2
                            status = "destroyed"

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
                    # якщо гравець лише пошкодив поточний корабель, запамп'ятовуємо останню пошкоджену точку, позначаємо точку як пошкоджену
                    else:
                        print("попали")
                        # якщо гравець попав, але не знищив корабель - вмикаємо режим знищення та запам'ятовуємо останню точку попадання
                        self.__comp_killMode = True
                        field[row][col] = 1
                        status = "damaged"

                        if self.__comp_startDamagedPoints is None:
                            self.__comp_startDamagedPoints = (row, col)

                        if self.__comp_lastDamagedRotate is None and ship.number_of_hits > 1:
                            if row == self.__comp_startDamagedPoints[0]:
                                self.__comp_lastDamagedRotate = 0
                            elif col == self.__comp_startDamagedPoints[1]:
                                self.__comp_lastDamagedRotate = 90
                        print(f"start: {self.__comp_startDamagedPoints}, rotate: {self.__comp_lastDamagedRotate}\n")

                    break

        return field, status

    def shoot(self, x, y, is_comp):
        field = self.__hiddenField.getField()
        status = ""

        # якщо стріляє людина
        if is_comp is False:
            # якщо попали туди, куди вже стріляли - завершуємо функцію
            if field[x][y] != 0:
                return "none"
            else:
                field, status = self.checkShip(x, y, field)

        # якщо стріляє комп'ютер
        elif is_comp is True:
            # якщо ми знаходимось у режимі пошуку, обираємо точки куди компьютер ще не стріляв та стріляємо туди
            if self.__comp_killMode is False:
                empty_cells_raw = np.where(field == 0)
                empty_cells = []

                for i in range(len(empty_cells_raw[0])):
                    empty_cells.append((empty_cells_raw[0][i], empty_cells_raw[1][i]))

                print(empty_cells)
                cell = random.choice(empty_cells)
                row, col = cell[0], cell[1]

                field, status = self.checkShip(row, col, field)

            # якщо режим знищення включено - означає, що комп'ютеру потрібно "добити" корабель
            else:
                # якщо комп'ютер ще не знає напрям корабля, він виявляє для себе доступні точки для удару та стріляє в одну з них випадковим чином
                if self.__comp_lastDamagedRotate is None:
                    available_cells = []
                    for i in range(self.__comp_startDamagedPoints[0] - 1, self.__comp_startDamagedPoints[0] + 2):
                        for j in range(self.__comp_startDamagedPoints[1] - 1, self.__comp_startDamagedPoints[1] + 2):
                            if 0 <= i <= 9 and 0 <= j <= 9:
                                if i == self.__comp_startDamagedPoints[0] or j == self.__comp_startDamagedPoints[1]:
                                    if field[i][j] not in [1, 10]:
                                        available_cells.append((i, j))

                    cell = random.choice(available_cells)
                    row, col = cell[0], cell[1]
                    print(f"компьютер будет стрелять наугад вокруг ячейки:\n{available_cells}")

                    field, status = self.checkShip(row, col, field)

                # якщо комп'ютер вже наніс достатню кількість ударів щоб дізнатися напрям кораблю:
                # якщо напрям горизонтальний:
                elif self.__comp_lastDamagedRotate == 0:
                    available_cells = []

                    for j in range(1, 4):
                        if 0 <= self.__comp_startDamagedPoints[1] - j:
                            if field[self.__comp_startDamagedPoints[0]][self.__comp_startDamagedPoints[1] - j] not in [1, 2, 10]:
                                available_cells.append(
                                    (self.__comp_startDamagedPoints[0], self.__comp_startDamagedPoints[1] - j))
                                break
                        else:
                            break

                    for j in range(1, 4):
                        if self.__comp_startDamagedPoints[1] + j <= 9:
                            if field[self.__comp_startDamagedPoints[0]][self.__comp_startDamagedPoints[1] + j] not in [1, 2, 10]:
                                available_cells.append(
                                    (self.__comp_startDamagedPoints[0], self.__comp_startDamagedPoints[1] + j))
                                break
                        else:
                            break

                    cell = random.choice(available_cells)
                    row, col = cell[0], cell[1]
                    print(f"компьютер будет стрелять наугад вокруг ячейки:\n{available_cells}")

                    field, status = self.checkShip(row, col, field)

                # якщо напрям вертикальний:
                elif self.__comp_lastDamagedRotate == 90:
                    available_cells = []
                    for i in range(1, 4):
                        if 0 <= self.__comp_startDamagedPoints[0] - i:
                            if field[self.__comp_startDamagedPoints[0] - i][self.__comp_startDamagedPoints[1]] not in [1, 2, 10]:
                                available_cells.append(
                                    (self.__comp_startDamagedPoints[0] - i, self.__comp_startDamagedPoints[1]))
                                break
                        else:
                            break

                    for i in range(1, 4):
                        if self.__comp_startDamagedPoints[0] + i <= 9:
                            if field[self.__comp_startDamagedPoints[0] + i][self.__comp_startDamagedPoints[1]] not in [1, 2, 10]:
                                available_cells.append(
                                    (self.__comp_startDamagedPoints[0] + i, self.__comp_startDamagedPoints[1]))
                                break
                        else:
                            break

                    cell = random.choice(available_cells)
                    row, col = cell[0], cell[1]
                    print(f"компьютер будет стрелять наугад вокруг ячейки:\n{available_cells}")

                    field, status = self.checkShip(row, col, field)

        self.__hiddenField.setField(field)

        bool_field = (field == 2)
        if np.count_nonzero(bool_field) == 20:
            status = "loose"

        return status
