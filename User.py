from Field import Field
from DraggableEllipse import DraggableEllipse
import random
import pygame
import numpy as np


class User:
    def __init__(self, name):
        # Initialize User object with a name, player and hidden fields, ships, and computer play mode variables
        self.__name = name

        self.__playerField = Field()
        self.__hiddenField = Field()

        self.__ships = self.create_ships()

        self.__comp_killMode = False

        self.__comp_startDamagedPoints = None

        self.__comp_extremeDamagedPoints = []

        self.__comp_lastDamagedRotate = None


    # Create a ship with specified size, starting position (x, y), and count
    def create_ship(self, size, x, y, count):
        ellipses = []
        for i in range(count):
            ellipses.append(DraggableEllipse(x, y, size, (0, 0, 0), self))
            x += size * 40
        return ellipses


    # Create a set of ships with different sizes and starting positions
    def create_ships(self):
        ships = self.create_ship(4, 100, 180, 1)
        ships.extend(self.create_ship(3, 100, 230, 2))
        ships.extend(self.create_ship(2, 100, 280, 3))
        ships.extend(self.create_ship(1, 100, 330, 4))
        return ships


    def get_name(self):
        return self.__name


    def set_name(self, name):
        self.__name = name


    # Place a ship on the player's field based on the given position and rotation
    def place_ship(self, position, rotate):
        field = self.__playerField.get_field()

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

        self.__playerField.set_field(field)
        return field, "the ship is placed on the playing field"


    # Delete a ship from the player's field based on the given position and rotation
    def delete_ship(self, position, rotate):
        field = self.__playerField.get_field()

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

        self.__playerField.set_field(field)
        return field, "the ship was deleted"


    # Reset the player's field and ship positions
    def clear_field(self):
        for ship in self.get_ships():
            ship.rect.x = ship.start_x
            ship.rect.y = ship.start_y
            ship.rotate = 90
            ship.rotate_ship()
            ship.update_ship_position()
            ship.status = ""
            ship.x = ship.start_x
            ship.y = ship.start_y

        self.__playerField.clear_field()


    # Randomly place ships on the player's field
    def random_placement(self):
        self.clear_field()

        field = self.__playerField.get_field()

        for ship in self.get_ships():
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

                field, status = self.place_ship(position, rotate)

                if status == "the ship is placed on the playing field":
                    ship.status = status
                    ship.rotate = rotate
                    ship.x = row
                    ship.y = col

                    # ship.update_ship_position()
                    ship.position = position

                    if rotate == 90:
                        ship.rect = pygame.Rect((ship.y * 40) + 670, (ship.x * 40) + 170, 40, ship.size * 40 - 10)

                    if rotate == 0:
                        ship.rect = pygame.Rect((ship.y * 40) + 670, (ship.x * 40) + 170, ship.size * 40 - 10, 40)


    def get_ships(self):
        """Returns all ships as a dictionary"""
        return self.__ships


    def get_hidden_field(self):
        return self.__hiddenField.get_field()


    # Check the result of a shot at the specified row and column
    def check_ship(self, row, col, field):
        print(f"in {self.get_name()} shoot to ({row}, {col})")
        status = ""
        # If missed, mark the cell with 10
        if self.__playerField.get_field()[row][col] != 1:
            print("miss\n")
            field[row][col] = 10
            status = "missed"
        # If hit
        else:
            for ship in self.get_ships():
                if (row, col) in ship.position:
                    ship.number_of_hits += 1

                    # Check if the ship is destroyed
                    # If destroyed, turn off the destruction mode, mark it as destroyed, and mark an empty zone around it
                    if ship.number_of_hits == ship.size:
                        print("destroy\n")
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
                    # If the player only damaged the current ship, remember the last damaged point, mark it as damaged
                    else:
                        print("hit")
                        # If the player hit but did not destroy the ship, turn on the destruction mode and remember the last hit point
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


    # Perform a shot at the specified coordinates
    def shoot(self, x, y, is_comp):
        field = self.__hiddenField.get_field()
        status = ""

        # If a human is shooting
        if is_comp is False:
            # If the shot is at a cell that has already been shot, end the function
            if field[x][y] != 0:
                return "none"
            else:
                field, status = self.check_ship(x, y, field)

        # If the computer is shooting
        elif is_comp is True:
            # If in search mode, select cells where the computer has not shot yet and shoot randomly
            if self.__comp_killMode is False:
                empty_cells_raw = np.where(field == 0)
                empty_cells = []

                for i in range(len(empty_cells_raw[0])):
                    empty_cells.append((empty_cells_raw[0][i], empty_cells_raw[1][i]))

                print(empty_cells)
                cell = random.choice(empty_cells)
                row, col = cell[0], cell[1]

                field, status = self.check_ship(row, col, field)

            # If in destruction mode, it means the computer needs to "finish off" the ship
            else:
                # If the computer does not know the direction of the ship yet, it discovers available cells to attack and shoots randomly at one of them
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
                    print(f"the computer will shoot randomly around the cell:\n{available_cells}")

                    field, status = self.check_ship(row, col, field)

                # If the computer has already dealt enough hits to determine the direction of the ship:
                # If the direction is horizontal:
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
                    print(f"the computer will shoot randomly around the cell\n{available_cells}")

                    field, status = self.check_ship(row, col, field)

                # If the direction is vertical:
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
                    print(f"the computer will shoot randomly around the cell:\n{available_cells}")

                    field, status = self.check_ship(row, col, field)

        self.__hiddenField.set_field(field)

        bool_field = (field == 2)
        if np.count_nonzero(bool_field) == 20:
            status = "loose"

        return status
