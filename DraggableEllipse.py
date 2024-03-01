import pygame
import copy


class DraggableEllipse:

    # Initialization
    def __init__(self, x, y, size, color, user):
        # Coordinates of the ship's head (for proper spawning on the initial screen and correct calculation of all points)
        self.x = x
        self.y = y
        self.start_x = copy.deepcopy(x)
        self.start_y = copy.deepcopy(y)
        self.rotate = 0
        self.position = []
        self.size = size
        self.number_of_hits = 0
        # Create a rectangle for drawing the ellipse
        self.rect = pygame.Rect(x, y, size * 40 - 10, 40)
        self.color = color
        self.dragging = False
        self.status = ""
        self.user = user


    def get_ship_position(self):
        return self.position


    # Draw the ellipse
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect, 3)


    # Update ship position on the grid
    def update_ship_position(self):
        position = []
        for point in range(self.size):
            if self.rotate == 0:
                position.append((self.x, self.y + point))
            elif self.rotate == 90:
                position.append((self.x + point, self.y))

        # Check that the ship is within the 10x10 grid
        if all(0 <= point[0] <= 9 and 0 <= point[1] <= 9 for point in position):
            self.position = position
        else:
            self.position = []


    # Rotate the ship
    def rotate_ship(self):
        if len(self.position) != 0:
            self.user.delete_ship(self.position, self.rotate)

        if self.rotate == 0:
            self.rotate = 90
            self.rect = pygame.Rect(self.rect.x, self.rect.y, 40, self.size * 40 - 10)
        elif self.rotate == 90:
            self.rotate = 0
            self.rect = pygame.Rect(self.rect.x, self.rect.y, self.size * 40 - 10, 40)

        self.update_ship_position()

        if len(self.position) != 0:
            self.user.place_ship(self.position, self.rotate)


    # Update ship position during dragging
    def update(self):
        # if self.random:
        #     return

        if self.dragging:

            if self.status == "the ship is placed on the playing field":
                field, self.status = self.user.delete_ship(self.position, self.rotate)
                if self.status == "the ship was deleted":
                    self.status = ""

            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Round coordinates for alignment on the grid
            self.rect.x = round(mouse_x / 5) * 5
            self.rect.y = round(mouse_y / 5) * 5
            # 650 and 150 are the coordinates of the first cell on the grid, setting points from 0 to 9
            self.x = (self.rect.x - 650) // 40
            self.y = (self.rect.y - 150) // 40
            self.update_ship_position()
        else:
            if self.status == "the ship is placed on the playing field":
                return

            if len(self.position) == 0:
                self.rect.x = self.start_x
                self.rect.y = self.start_y
                self.update_ship_position()
                self.status = ""
                return

            field, self.status = self.user.place_ship(self.position, self.rotate)

            if self.status != "the ship is placed on the playing field":
                self.rect.x = self.start_x
                self.rect.y = self.start_y
                self.update_ship_position()
                self.status = ""
                return
            self.update_ship_position()
