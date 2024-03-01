import pygame
import sys
from User import User
import random

class BattleshipGame:
    def __init__(self):
        # Pygame initialization
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 1200, 700
        self.button_size = 40
        self.GRID_OFFSET = 250
        self.BUTTON_WIDTH_FIRST_SCENE = 350
        self.BUTTON_HEIGHT_FIRST_SCENE = 250
        self.button_size_FIRST_SCENE = (self.BUTTON_WIDTH_FIRST_SCENE, self.BUTTON_HEIGHT_FIRST_SCENE)
        self.EXIT_BUTTON_WIDTH = 100
        self.EXIT_BUTTON_HEIGHT = 50
        self.CELLS_TEXT = 'ADCDEFGHIJ'
        # ...

        self.colors = {"BLACK": (0, 0, 0), "WHITE": (255, 255, 255), "RED": (255, 0, 0), "GREEN": (0, 255, 0),
              "BLUE": (0, 0, 255), "YELLOW": (255, 255, 0), "ORANGE": (255, 165, 0)}
        self.bg_color = (255, 255, 255)
        self.border_color = (0, 0, 0)

        self.console_active = False
        self.console_text = []
        self.current_input = ""
        self.toggle_counter = 0

        # Window creation for the game
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Гра у кораблі")

        # Variables
        # Scene currently being displayed
        self.current_scene = 1
        self.attacking_player = 0
        # Buttons
        self.button_with_friend = pygame.Rect(170, 200, self.BUTTON_WIDTH_FIRST_SCENE, self.BUTTON_HEIGHT_FIRST_SCENE)
        self.button_with_computer = pygame.Rect(630, 200, self.BUTTON_WIDTH_FIRST_SCENE, self.BUTTON_HEIGHT_FIRST_SCENE)
        self.button_exit = pygame.Rect(self.WIDTH - 110, 10, 100, 50)
        self.random_button = pygame.Rect(450, 535, 140, 30)
        self.clear_button = pygame.Rect(450, 490, 140, 30)
        self.start_button = pygame.Rect(self.WIDTH - 160, self.HEIGHT - 60, 150, 50)
        self.button_image_friend = pygame.image.load("images/buttonFriend.jpg")
        self.damaged_cell_image = pygame.image.load("images/damaged_cell.png")
        self.destroyed_cell_image = pygame.image.load("images/destroyed_cell.png")
        self.missed_cell_image = pygame.image.load("images/missed_cell.png")
        self.button_image_friend = pygame.transform.scale(self.button_image_friend, self.button_size_FIRST_SCENE)
        self.buttonImageComputer = pygame.image.load("images/buttonComputer.jpg")
        self.buttonImageComputer = pygame.transform.scale(self.buttonImageComputer, self.button_size_FIRST_SCENE)

        self.font = pygame.font.Font(None, 36)
        self.user_name_surface = self.font.render('', True, (201, 201, 201))
        self.user_name_rect = pygame.Rect((self.WIDTH - 300) // 2, self.HEIGHT // 10, 300, 100)
        self.text = ''

        # An arrow to indicate the course
        self.arrow1_image = pygame.image.load("images/arrow1.png")
        self.arrow2_image = pygame.image.load("images/arrow2.png")
        self.arrow1_image_rect = self.arrow1_image.get_rect()
        self.arrow1_image_rect.x = self.WIDTH // 2 - 60
        self.arrow1_image_rect.y = 320
        self.arrow1_image = pygame.transform.scale(self.arrow1_image, (100, 100))

        self.arrow2_image_rect = self.arrow1_image.get_rect()
        self.arrow2_image_rect.x = self.WIDTH // 2 - 60
        self.arrow2_image_rect.y = 320
        self.arrow2_image = pygame.transform.scale(self.arrow2_image, (100, 100))

        # Setting to play with a friend or from a PC
        self.game_param = 0

        # A list of players with one player by default
        self.users = [User("user")]

        # Initialization of ships
        self.ships = None

        self.init_ships()


    def init_ships(self):
        self.ships = self.users[-1].get_ships()

        
    # Function to draw a button based on received parameters
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

            text = font.render(text, True, self.border_color)
            self.screen.blit(text, (rect.x + (rect.width - text.get_width()) // 2,
                                    rect.y + (rect.height - text.get_height()) // 2))


    # Function to draw the grid
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
                    text_surface = font.render(text, True, self.border_color)
                    text_rect = text_surface.get_rect(center=rect.center)
                    pygame.draw.rect(self.screen, self.bg_color, rect, 1)
                    self.screen.blit(text_surface, text_rect)
                else:
                    pygame.draw.rect(self.screen, self.border_color, self.draw_grid_cell(offset, button_size, i, j), 1)


    # Function to draw a grid cell based on parameters
    def draw_grid_cell(self, offset, button_size, i, j):
        return pygame.Rect((offset + j * (button_size) + (self.WIDTH - button_size * 11) / 2,
                            i * (button_size) + (self.WIDTH / 2 - button_size * 11) / 2 + self.button_exit.height,
                            button_size, button_size))


    # Function to get the coordinates of the cell where the shot was fired
    def get_grid_cell_location(self, mouse_position):
        if 110 <= mouse_position[0] <= 510 and 170 <= mouse_position[1] <= 570:
            return (mouse_position[1] - 170) // 40, (mouse_position[0] - 110) // 40, "left field"
        elif 690 <= mouse_position[0] <= 1190 and 170 <= mouse_position[1] <= 570:
            return (mouse_position[1] - 170) // 40, (mouse_position[0] - 690) // 40, "right field"
        else:
            return None, None, 'out'


    # Function to draw opponent's fields
    def draw_opponent_fields(self):
        field1 = self.users[0].get_hidden_field()
        field2 = self.users[1].get_hidden_field()

        for i in range(10):
            for j in range(10):
                if field1[i][j] == 10:
                    self.screen.blit(self.missed_cell_image, (j * 40 + 110, i * 40 + 170))
                if field2[i][j] == 10:
                    self.screen.blit(self.missed_cell_image, (j * 40 + 690, i * 40 + 170))
                if field1[i][j] == 1:
                    self.screen.blit(self.damaged_cell_image, (j * 40 + 110, i * 40 + 170))
                if field2[i][j] == 1:
                    self.screen.blit(self.damaged_cell_image, (j * 40 + 690, i * 40 + 170))
                if field1[i][j] == 2:
                    self.screen.blit(self.destroyed_cell_image, (j * 40 + 110, i * 40 + 170))
                if field2[i][j] == 2:
                    self.screen.blit(self.destroyed_cell_image, (j * 40 + 690, i * 40 + 170))


    # Drawing the first scene
    def draw_first_scene(self):
        self.draw_button(self.button_exit, None, "Exit")
        self.draw_button(self.button_with_friend, self.button_image_friend, None)
        self.draw_button(self.button_with_computer, self.buttonImageComputer, None)


    # Drawing the second scene
    def draw_second_scene(self):
        self.text = self.users[-1].get_name()
        self.draw_button(self.button_exit, None, "Back")
        self.draw_button(self.random_button, None, "Random")
        self.draw_button(self.clear_button, None, "Clear")
        self.draw_button(self.start_button, None, "Start")

        font = pygame.font.Font(None, 27)
        user_text_plane = 'Input user name'
        text_surface = font.render(user_text_plane, True, self.border_color)
        text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 17))
        self.screen.blit(text_surface, text_rect)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, self.border_color)
        text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 10))
        self.screen.blit(text_surface, text_rect)

        self.draw_grid(self.GRID_OFFSET, self.button_size)

        self.update_ships()


    # Drawing the third scene
    def draw_third_scene(self):
        self.draw_button(self.button_exit, None, "Exit")

        self.draw_grid(-self.GRID_OFFSET - 60, self.button_size)
        self.draw_grid(self.GRID_OFFSET + 20, self.button_size)

        font = pygame.font.Font(None, 40)

        text_surface = font.render(self.users[0].get_name(), True, self.border_color)
        text_rect = text_surface.get_rect(center=(self.WIDTH // 2 - 310, self.HEIGHT // 2 - 250))
        self.screen.blit(text_surface, text_rect)

        text_surface = font.render(self.users[1].get_name(), True, self.border_color)
        text_rect = text_surface.get_rect(center=(self.WIDTH // 2 + 310, self.HEIGHT // 2 - 250))
        self.screen.blit(text_surface, text_rect)

        if self.attacking_player == 1:
            self.screen.blit(self.arrow1_image, self.arrow1_image_rect.topleft)
        elif self.attacking_player == 2:
            self.screen.blit(self.arrow2_image, self.arrow2_image_rect.topleft)

        self.draw_opponent_fields()


    # Drawing the fourth scene
    def draw_fourth_scene(self):
        font = pygame.font.Font(None, 100)
        text_surface = font.render(f"{self.users[0 if self.attacking_player == 1 else 1].get_name()} is winner!",
                                   True, self.border_color)
        text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)
        self.draw_button(self.button_exit, None, "Exit")


    # Console logic
    def console(self, event):
        if event.key == pygame.K_BACKQUOTE:
            self.toggle_counter += 1
            if self.toggle_counter % 2 == 1:
                self.console_active = True
            else:
                self.console_active = False
                self.console_text.append("Console: " + self.current_input)
                self.current_input = ""
        elif self.console_active:
            if event.key == pygame.K_RETURN:
                self.console_text.append("Console: " + self.current_input)
                if self.current_input == "commands ?":
                    self.console_text.append("get colors")
                    self.console_text.append("set bg color <COLOR>")
                    self.console_text.append("set border color <COLOR>")
                if self.current_input.startswith("get colors"):
                    self.console_text.append("List of colors: " + ", ".join(self.colors.keys()))
                elif self.current_input.startswith("set bg color "):
                    color_name = self.current_input.split(" ")[-1]
                    if color_name in self.colors:
                        self.console_text.append(f"Setting background color to {color_name}")
                        self.bg_color = self.colors[color_name]
                    else:
                        self.console_text.append("Unknown color")
                elif self.current_input.startswith("set border color "):
                    color_name = self.current_input.split(" ")[-1]
                    if color_name in self.colors:
                        self.console_text.append(f"Setting border color to {color_name}")
                        self.border_color = self.colors[color_name]
                    else:
                        self.console_text.append("Unknown color")
                else:
                    self.console_text.append("Unknown command")
                self.current_input = ""
            elif event.key == pygame.K_BACKSPACE:
                self.current_input = self.current_input[:-1]
            else:
                self.current_input += event.unicode


    # Handling user events
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # activate console
            elif event.type == pygame.KEYDOWN:
                self.console(event)
            elif pygame.mouse.get_pressed()[0]:
                self.handle_mouse_left_button_down(event)
            elif pygame.mouse.get_pressed()[2]:
                self.handle_mouse_right_button_down()
            elif not pygame.mouse.get_pressed()[0]:
                self.handle_mouse_left_button_up(event)


    # Handling left mouse button down events
    def handle_mouse_left_button_down(self, event):
        if self.button_exit.collidepoint(event.pos):
            if self.current_scene == 1 or self.current_scene == 3 or self.current_scene == 4:
                pygame.quit()
                sys.exit()
            else:
                self.current_scene -= 1
        if self.current_scene == 1:
            self.handle_mouse_left_button_down_scene1(event)
        elif self.current_scene == 2:
            self.handle_mouse_left_button_down_scene2()
        elif self.current_scene == 3:
            self.handle_mouse_left_button_down_scene3()


    # Handling left mouse button down events on the first scene
    def handle_mouse_left_button_down_scene1(self, event):
        if self.button_with_friend.collidepoint(event.pos):
            self.current_scene = 2
            self.game_param = 2
        elif self.button_with_computer.collidepoint(event.pos):
            self.current_scene = 2
            self.game_param = 1


    # Handling left mouse button down events on the second scene
    def handle_mouse_left_button_down_scene2(self):
        if self.random_button.collidepoint(pygame.mouse.get_pos()):
            self.users[-1].random_placement()

        if self.clear_button.collidepoint(pygame.mouse.get_pos()):
            self.users[-1].clear_field()

        if self.start_button.collidepoint(pygame.mouse.get_pos()):
            if self.game_param == 3:
                for ship in self.users[1].get_ships():
                    if len(ship.position) == 0:
                        return

                self.current_scene = 3
            if self.game_param == 1:
                self.users.append(User("comp"))
                self.users[-1].random_placement()
                self.attacking_player = 1
                self.current_scene = 3
            if self.game_param == 2:
                for ship in self.users[0].get_ships():
                    if len(ship.position) == 0:
                        return

                self.users.append(User("user"))
                self.attacking_player = random.choice([1, 2])
                self.init_ships()
                self.game_param = 3
        for ship in self.ships:
            if ship.rect.collidepoint(pygame.mouse.get_pos()):
                ship.dragging = True


    # Handling left mouse button down events on the third scene
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
            if self.game_param == 1:
                return

            if side == 'right field':
                return

            status = self.users[0].shoot(x, y, False)

        if status == "loose":
            self.current_scene = 4
            return

        if status == "missed":
            if self.attacking_player == 1:
                self.attacking_player = 2

                if self.game_param == 1:
                    while True:
                        status = self.users[0].shoot(None, None, True)

                        if status == "loose":
                            self.current_scene = 4
                            return

                        if status == "missed":
                            self.attacking_player = 1
                            break
            else:
                self.attacking_player = 1


    # Handling left mouse button up events
    def handle_mouse_left_button_up(self, event):
        if self.current_scene == 2:
            if self.user_name_rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.users[-1].set_name(self.users[-1].get_name()[:-1])
                    else:
                        self.users[-1].set_name(self.users[-1].get_name() + event.unicode)
        for ship in self.ships:
            ship.dragging = False


    # Handling right mouse button down events
    def handle_mouse_right_button_down(self):
        if self.current_scene == 2:
            self.handle_mouse_right_button_down_scene2()


    # Handling right mouse button down events on the second scene
    def handle_mouse_right_button_down_scene2(self):
        for ship in self.ships:
            if ship.rect.collidepoint(pygame.mouse.get_pos()):
                ship.rotate_ship()


    # Updating the positions of the ships on the grid
    def update_ships(self):
        for ship in self.ships:
            ship.update()
            ship.draw(self.screen)


    # Draw console function
    def draw_console(self):
        if self.console_active:
            self.screen.fill(self.colors["BLACK"])
            for i, line in enumerate(reversed(self.console_text)):
                console_surface = self.font.render(line, True, self.colors["GREEN"])
                self.screen.blit(console_surface, (10, self.HEIGHT - 65 - i * 30))

            input_surface = self.font.render("> " + self.current_input, True, self.colors["GREEN"])
            self.screen.blit(input_surface, (10, self.HEIGHT - 35))


    # Update screen function
    def update_screen(self):
        self.screen.fill(self.bg_color)
        if self.console_active:
            self.draw_console()
        elif self.current_scene == 1:
            self.draw_first_scene()
        elif self.current_scene == 2:
            self.draw_second_scene()
        elif self.current_scene == 3:
            self.draw_third_scene()
        elif self.current_scene == 4:
            self.draw_fourth_scene()
        pygame.display.flip()
