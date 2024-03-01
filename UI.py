import pygame
import sys
from User import User
import random
import time
import numpy as np

class BattleshipGame:
    def __init__(self):
        # Ініціалізація Pygame
        pygame.init()

        # Константи
        self.WIDTH, self.HEIGHT = 1200, 700
        self.BUTTON_SIZE = 40
        self.GRID_OFFSET = 250
        self.BUTTON_WIDTH_FIRST_SCENE = 350
        self.BUTTON_HEIGHT_FIRST_SCENE = 250
        self.BUTTON_SIZE_FIRST_SCENE = (self.BUTTON_WIDTH_FIRST_SCENE, self.BUTTON_HEIGHT_FIRST_SCENE)
        self.EXIT_BUTTON_WIDTH = 100
        self.EXIT_BUTTON_HEIGHT = 50
        self.CELLS_TEXT = 'ADCDEFGHIJ'

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # ... (інші константи)

        # Створення вікна для гри
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Гра у кораблі")

        # Змінні
        self.currentScene = 1                                                                                           # сцена яка відображається зараз
        self.attacking_player = 0
        # кнопки
        self.buttonWithFriend = pygame.Rect(170, 200, self.BUTTON_WIDTH_FIRST_SCENE, self.BUTTON_HEIGHT_FIRST_SCENE)    # кнопка "Грати з другом"
        self.buttonWithComputer = pygame.Rect(630, 200, self.BUTTON_WIDTH_FIRST_SCENE, self.BUTTON_HEIGHT_FIRST_SCENE)  # кнопка "Грати з комп'ютером"
        self.buttonExit = pygame.Rect(self.WIDTH - 110, 10, 100, 50)                                                    # кнопка виходу
        self.randomButton = pygame.Rect(450, 535, 140, 30)                                                              # кнопка рандомного розставлення кораблів
        self.clearButton = pygame.Rect(450, 490, 140, 30)                                                               # кнопка для очищення поля
        self.startButton = pygame.Rect(self.WIDTH - 160, self.HEIGHT - 60, 150, 50)                                     # кнопка початку гри
        self.buttonImageFriend = pygame.image.load("images/buttonFriend.jpg")                                           # задання фону для кнопки "Грати з другом"
        self.damagedCellImage = pygame.image.load("images/damaged_cell.png")
        self.destroyedCellImage = pygame.image.load("images/destroyed_cell.png")
        self.missedCellImage = pygame.image.load("images/missed_cell.png")
        self.buttonImageFriend = pygame.transform.scale(self.buttonImageFriend, self.BUTTON_SIZE_FIRST_SCENE)           # задання розмірів
        self.buttonImageComputer = pygame.image.load("images/buttonComputer.jpg")                                       # задання фону для кнопки "Грати з комп'ютером"
        self.buttonImageComputer = pygame.transform.scale(self.buttonImageComputer, self.BUTTON_SIZE_FIRST_SCENE)       # задання розмірів

        self.font = pygame.font.Font(None, 36)                                                               # шрифт для поля з іменем гравця
        self.userNameSurface = self.font.render('', True, (201, 201, 201))                            # поле для імені гравця
        self.userNameRect = pygame.Rect((self.WIDTH - 300) // 2, self.HEIGHT // 10, 300, 100)                           # поле для імені гравця
        self.text = ''                                                                                                  # для збереження імені гравця

        # стрілка для позначення ходу
        self.arrow1Image = pygame.image.load("images/arrow1.png")
        self.arrow2Image = pygame.image.load("images/arrow2.png")
        self.arrow1ImageRect = self.arrow1Image.get_rect()
        self.arrow1ImageRect.x = self.WIDTH // 2 - 60
        self.arrow1ImageRect.y = 320
        self.arrow1Image = pygame.transform.scale(self.arrow1Image, (100, 100))

        self.arrow2ImageRect = self.arrow1Image.get_rect()
        self.arrow2ImageRect.x = self.WIDTH // 2 - 60
        self.arrow2ImageRect.y = 320
        self.arrow2Image = pygame.transform.scale(self.arrow2Image, (100, 100))

        # параметр для налашування грати з другом чи з ПК
        self.gameParam = 0

        # список з гравців в якому за замовчуванням один гравець
        self.users = [User("user")]

        # ініціалізація корабів
        self.ships = None

        self.init_ships()



    def init_ships(self):
        self.ships = self.users[-1].getShips()
    # функція для малювання кнопки згідно отриманих параметрів
    def draw_button(self, rect, image, text):
        if image is not None:
            self.screen.blit(image, (rect.x, rect.y))

        if text is not None:
            if rect.collidepoint(pygame.mouse.get_pos()):
                color = (184, 184, 184)
            else:
                color = (201, 201, 201)

            pygame.draw.rect(self.screen, color, rect, border_radius=10)

            if text == 'Random':
                font = pygame.font.Font(None, 28)
            else:
                font = pygame.font.Font(None, 35)

            text = font.render(text, True, self.BLACK)
            self.screen.blit(text, (rect.x + (rect.width - text.get_width()) // 2,
                                    rect.y + (rect.height - text.get_height()) // 2))

    # функція для малювання поля
    def draw_grid(self, offset, button_size):
        for i in range(11):
            for j in range(11):
                if i == 0 or j == 0:
                    if i == 0 and j == 0:
                        continue
                    rect = self.draw_grid_cell(offset, button_size, i, j)
                    if i == 0:
                        text = self.CELLS_TEXT[j - 1]
                    elif j == 0:
                        text = str(i)
                    font = pygame.font.Font(None, 30)
                    text_surface = font.render(text, True, self.BLACK)
                    text_rect = text_surface.get_rect(center=rect.center)
                    pygame.draw.rect(self.screen, self.WHITE, rect, 1)
                    self.screen.blit(text_surface, text_rect)
                else:
                    pygame.draw.rect(self.screen, self.BLACK, self.draw_grid_cell(offset, button_size, i, j), 1)

    # функція для малювання комірки поля згідно параметрів
    def draw_grid_cell(self, offset, button_size, i, j):
        return pygame.Rect((offset + j * (button_size) + (self.WIDTH - button_size * 11) / 2,
                            i * (button_size) + (self.WIDTH / 2 - button_size * 11) / 2 + self.buttonExit.height,
                            button_size, button_size))

    # функція для отримання координат точки куди був постріл
    def get_grid_cell_location(self, mouse_position):
        if 110 <= mouse_position[0] <= 510 and 170 <= mouse_position[1] <= 570:
            return (mouse_position[1] - 170) // 40, (mouse_position[0] - 110) // 40, "left field"
        elif 690 <= mouse_position[0] <= 1190 and 170 <= mouse_position[1] <= 570:
            return (mouse_position[1] - 170) // 40, (mouse_position[0] - 690) // 40, "right field"
        else:
            return None, None, 'out'
    def draw_opponent_fields(self):
        field1 = self.users[0].getHiddenField()
        field2 = self.users[1].getHiddenField()

        for i in range(10):
            for j in range(10):
                if field1[i][j] == 10:
                    self.screen.blit(self.missedCellImage, (j * 40 + 110, i * 40 + 170))
                if field2[i][j] == 10:
                    self.screen.blit(self.missedCellImage, (j * 40 + 690, i * 40 + 170))
                if field1[i][j] == 1:
                    self.screen.blit(self.damagedCellImage, (j * 40 + 110, i * 40 + 170))
                if field2[i][j] == 1:
                    self.screen.blit(self.damagedCellImage, (j * 40 + 690, i * 40 + 170))
                if field1[i][j] == 2:
                    self.screen.blit(self.destroyedCellImage, (j * 40 + 110, i * 40 + 170))
                if field2[i][j] == 2:
                    self.screen.blit(self.destroyedCellImage, (j * 40 + 690, i * 40 + 170))


    # малювання першої сцени
    def draw_first_scene(self):
        self.draw_button(self.buttonExit, None, "Exit")
        self.draw_button(self.buttonWithFriend, self.buttonImageFriend, None)
        self.draw_button(self.buttonWithComputer, self.buttonImageComputer, None)

    # малювання другої сцени
    def draw_second_scene(self):
        self.text = self.users[-1].getName()
        self.draw_button(self.buttonExit, None, "Back")
        self.draw_button(self.randomButton, None, "Random")
        self.draw_button(self.clearButton, None, "Clear")
        self.draw_button(self.startButton, None, "Start")
        font = pygame.font.Font(None, 27)
        user_text_plane_text = 'Input user name'
        text_surface = font.render(user_text_plane_text, True, self.BLACK)
        text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 17))
        self.screen.blit(text_surface, text_rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (201, 201, 201))
        text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 10))
        self.screen.blit(text_surface, text_rect)
        self.draw_grid(self.GRID_OFFSET, self.BUTTON_SIZE)
        self.update_ships()

    # малювання третьї сцени
    def draw_third_scene(self):
        self.draw_button(self.buttonExit, None, "Exit")
        self.draw_grid(-self.GRID_OFFSET - 60, self.BUTTON_SIZE)
        self.draw_grid(self.GRID_OFFSET + 20, self.BUTTON_SIZE)
        font = pygame.font.Font(None, 40)
        text_surface = font.render(self.users[0].getName(), True, self.BLACK)
        text_rect = text_surface.get_rect(center=(self.WIDTH // 2 - 310, self.HEIGHT // 2 - 250))
        self.screen.blit(text_surface, text_rect)
        text_surface = font.render(self.users[1].getName(), True, self.BLACK)
        text_rect = text_surface.get_rect(center=(self.WIDTH // 2 + 310, self.HEIGHT // 2 - 250))
        self.screen.blit(text_surface, text_rect)

        if self.attacking_player == 1:
            self.screen.blit(self.arrow1Image, self.arrow1ImageRect.topleft)
        elif self.attacking_player == 2:
            self.screen.blit(self.arrow2Image, self.arrow2ImageRect.topleft)

        self.draw_opponent_fields()

    def draw_fourth_scene(self):
        font = pygame.font.Font(None, 100)
        text_surface = font.render(f"{self.users[0 if self.attacking_player == 1 else 1].getName()} is winner!",
                                   True, self.BLACK)
        text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)
        self.draw_button(self.buttonExit, None, "Exit")


    # події користувача
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif pygame.mouse.get_pressed()[0]:
                self.handle_mouse_left_button_down(event)
            elif pygame.mouse.get_pressed()[2]:
                self.handle_mouse_right_button_down()
            elif not pygame.mouse.get_pressed()[0]:
                self.handle_mouse_left_button_up(event)

    # натискання ЛКМ
    def handle_mouse_left_button_down(self, event):
        if self.buttonExit.collidepoint(event.pos):
            if self.currentScene == 1 or self.currentScene == 3 or self.currentScene == 4:
                pygame.quit()
                sys.exit()
            else:
                self.currentScene -= 1
        if self.currentScene == 1:
            self.handle_mouse_left_button_down_scene1(event)
        elif self.currentScene == 2:
            self.handle_mouse_left_button_down_scene2()
        elif self.currentScene == 3:
            self.handle_mouse_left_button_down_scene3()

    # натискання ЛКМ на першій сцені
    def handle_mouse_left_button_down_scene1(self, event):
        if self.buttonWithFriend.collidepoint(event.pos):
            self.currentScene = 2
            self.gameParam = 2
        elif self.buttonWithComputer.collidepoint(event.pos):
            self.currentScene = 2
            self.gameParam = 1

    # натискання ЛКМ на другій сцені
    def handle_mouse_left_button_down_scene2(self):
        if self.randomButton.collidepoint(pygame.mouse.get_pos()):
            self.users[-1].randomPlacement()

        if self.clearButton.collidepoint(pygame.mouse.get_pos()):
            self.users[-1].clearField()

        if self.startButton.collidepoint(pygame.mouse.get_pos()):
            if self.gameParam == 3:
                for ship in self.users[1].getShips():
                    if len(ship.position) == 0:
                        return

                self.currentScene = 3
            if self.gameParam == 1:
                self.users.append(User("comp"))
                self.users[-1].randomPlacement()
                self.attacking_player = 1
                # зберегти данні гравця в списку
                # додати комп'ютер як другого гравця в список. Комп'ютер має наслідувати клас Гравця
                self.currentScene = 3
            if self.gameParam == 2:
                for ship in self.users[0].getShips():
                    if len(ship.position) == 0:
                        return

                self.users.append(User("user"))
                # зберегти данні гравця в списку
                # створити нового гравця, нові кораблі та все ініціалізуквати для нього
                self.attacking_player = random.choice([1, 2])
                self.init_ships()
                self.gameParam = 3
        for ship in self.ships:
            if ship.rect.collidepoint(pygame.mouse.get_pos()):
                ship.dragging = True

    # натискання ЛКМ на третій сцені
    def handle_mouse_left_button_down_scene3(self):
        status = ""
        x, y, side = self.get_grid_cell_location(pygame.mouse.get_pos())
        if side == 'out':
            return

        if self.attacking_player == 1:
            if side == 'left field':
                return

            status = self.users[1].shoot(x, y, False)

        elif self.attacking_player == 2:
            if self.gameParam == 1:
                return

            if side == 'right field':
                return

            status = self.users[0].shoot(x, y, False)

        if status == "loose":
            self.currentScene = 4
            return

        if status == "missed":
            if self.attacking_player == 1:
                self.attacking_player = 2

                if self.gameParam == 1:
                    while True:
                        status = self.users[0].shoot(None, None, True)

                        if status == "loose":
                            self.currentScene = 4
                            return

                        if status == "missed":
                            self.attacking_player = 1
                            break
            else:
                self.attacking_player = 1




    # не натискання кнопок
    def handle_mouse_left_button_up(self, event):
        if self.currentScene == 2:
            if self.userNameRect.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.users[-1].setName(self.users[-1].getName()[:-1])
                    else:
                        self.users[-1].setName(self.users[-1].getName() + event.unicode)
        for ship in self.ships:
            ship.dragging = False

    # натискання ПКМ
    def handle_mouse_right_button_down(self):
        if self.currentScene == 2:
            self.handle_mouse_right_button_down_scene2()

    # натискання ПКМ на другій сцені
    def handle_mouse_right_button_down_scene2(self):
        for ship in self.ships:
            if ship.rect.collidepoint(pygame.mouse.get_pos()):
                ship.rotateShip()

    # оновлення кораблів
    def update_ships(self):
        for ship in self.ships:
            ship.update()
            ship.draw(self.screen)

    # оновлення екрану
    def update_screen(self):
        self.screen.fill(self.WHITE)
        if self.currentScene == 1:
            self.draw_first_scene()
        elif self.currentScene == 2:
            self.draw_second_scene()
        elif self.currentScene == 3:
            self.draw_third_scene()
        elif self.currentScene == 4:
            self.draw_fourth_scene()
        pygame.display.flip()
