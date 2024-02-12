import pygame
import sys
from DraggableEllipse import DraggableEllipse

# Визначення класу DraggableEllipse міститься у файлі DraggableEllipse.py
# і використовується для створення та відображення кораблів.


# Функція для отримання кораблів
def getShip(size, x, y, count):
    ellipses = []
    for i in range(count):
        ellipses.append(DraggableEllipse(x, y, size, (0, 0, 0)))
        x += size * 40
    return ellipses


# Функція для створення списку кораблів
def getShips():
    ships = getShip(4, 100, 180, 1)
    ships.extend(getShip(3, 100, 230, 2))
    ships.extend(getShip(2, 100, 280, 3))
    ships.extend(getShip(1, 100, 330, 4))
    return ships

# Ініціалізація списку кораблів
ships = getShips()

# Ініціалізація Pygame
pygame.init()

# Ініціалізація констант
WIDTH, HEIGHT = 1200, 700
BUTTON_SIZE = 40
GRID_OFFSET = 250
BUTTON_WIDTH_FIRST_SCENE = 350
BUTTON_HEIGHT_FIRST_SCENE = 250
BUTTON_SIZE_FIRST_SCENE = (BUTTON_WIDTH_FIRST_SCENE, BUTTON_HEIGHT_FIRST_SCENE)
EXIT_BUTTON_WIDTH = 100
EXIT_BUTTON_HEIGHT = 50
CELLS_TEXT = 'ADCDEFGHIJ'
# ... (інші константи)

# Створення вікна Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гра у кораблі")

# Ініціалізація змінних
currentScene = 1
buttonWithFriend = pygame.Rect(170, 200, BUTTON_WIDTH_FIRST_SCENE, BUTTON_HEIGHT_FIRST_SCENE)
buttonWithComputer = pygame.Rect(630, 200, BUTTON_WIDTH_FIRST_SCENE, BUTTON_HEIGHT_FIRST_SCENE)
buttonExit = pygame.Rect(WIDTH - 110, 10, 100, 50)
randomButton = pygame.Rect(450, 535, 140, 30)
buttonImageFriend = pygame.image.load("images/buttonFriend.jpg")
buttonImageFriend = pygame.transform.scale(buttonImageFriend, BUTTON_SIZE_FIRST_SCENE)
buttonImageComputer = pygame.image.load("images/buttonComputer.jpg")
buttonImageComputer = pygame.transform.scale(buttonImageComputer, BUTTON_SIZE_FIRST_SCENE)

# Ігровий параметр, який відповідає за гру з другом чи комп'ютером
gameParam = 0


# Функція для створення та відображення кнопки
def drawButton(rect, image, text):
    color1 = (184, 184, 184)
    color2 = (184, 184, 184)

    if image is not None:
        screen.blit(image, (rect.x, rect.y))

    if text is not None:
        if rect.collidepoint(pygame.mouse.get_pos()):
            color1 = (184, 184, 184)
        else:
            color1 = (201, 201, 201)

        if rect.collidepoint(pygame.mouse.get_pos()):
            color2 = (184, 184, 184)
        else:
            color2 = (201, 201, 201)

        pygame.draw.rect(screen, color1, rect, border_radius=10)

        if text == 'Випадкове розташування':
            font = pygame.font.Font(None, 20)
        else:
            font = pygame.font.Font(None, 35)

        text = font.render(text, True, (0, 0, 0))
        screen.blit(text, (rect.x + (rect.width - text.get_width()) // 2,
                           rect.y + (rect.height - text.get_height()) // 2))


# Функція для відображення сітки
def drawGrid(offset, buttonSize):
    for i in range(11):
        for j in range(11):
            if i == 0 or j == 0:
                if i == 0 and j == 0:
                    continue
                rect = drawGridCell(offset, buttonSize, i, j)
                if i == 0:
                    text = CELLS_TEXT[j - 1]
                elif j == 0:
                    text = str(i)
                font = pygame.font.Font(None, 30)
                text_surface = font.render(text, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=rect.center)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)
                screen.blit(text_surface, text_rect)
            else:
                pygame.draw.rect(screen, (0, 0, 0), drawGridCell(offset, buttonSize, i, j), 1)


# Функція для відображення клітинки сітки
def drawGridCell(offset, buttonSize, i, j):
    return pygame.Rect((offset + j * (buttonSize) + (WIDTH - buttonSize * 11) / 2,
                        i * (buttonSize) + (WIDTH / 2 - buttonSize * 11) / 2 + buttonExit.height,
                        buttonSize, buttonSize))


# Функція  для відображення сцен
# Перша сцена
def drawFirstScene():
    drawButton(buttonExit, None, "Вийти")
    drawButton(buttonWithFriend, buttonImageFriend, None)
    drawButton(buttonWithComputer, buttonImageComputer, None)


# Друга сцена
def drawSecondScene(param):
    global ships

    drawButton(buttonExit, None, "Назад")
    drawButton(randomButton, None, "Випадкове розташування")

    drawGrid(GRID_OFFSET, BUTTON_SIZE)

    updateShips()


# Функція для обробки подій
def handleEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif pygame.mouse.get_pressed()[0]:
            handleMouseLeftButtonDown(event)
        elif not pygame.mouse.get_pressed()[0]:
            handleMouseLeftButtonUp()
        elif pygame.mouse.get_pressed()[2]:
            handleMouseRightButtonDown()


# Функція для обробки натискання лівої кнопки миші
def handleMouseLeftButtonDown(event):
    global currentScene
    if buttonExit.collidepoint(event.pos):
        if currentScene == 1:
            pygame.quit()
            sys.exit()
        else:
            currentScene -= 1
    if currentScene == 1:
        handleMouseLeftButtonDownScene1(event)
    elif currentScene == 2:
        handleMouseLeftButtonDownScene2()


# Функція для обробки натискання лівої кнопки миші на першій сцені
def handleMouseLeftButtonDownScene1(event):
    global currentScene
    global gameParam
    if buttonWithFriend.collidepoint(event.pos):
        currentScene = 2
        gameParam = 2
    elif buttonWithComputer.collidepoint(event.pos):
        currentScene = 2
        gameParam = 1


# Функція для обробки натискання лівої кнопки миші на другій сцені
def handleMouseLeftButtonDownScene2():
    global ships
    for ship in ships:
        if ship.rect.collidepoint(pygame.mouse.get_pos()):
            ship.dragging = True


# Функція для обробки ненатискання лівої кнопки миші на другій сцені
def handleMouseLeftButtonUp():
    global ships
    global currentScene

    if currentScene == 2:
        for ship in ships:
            ship.dragging = False


# Функція для обробки натискання правої кнопки миші
def handleMouseRightButtonDown():
    if currentScene == 2:
        handleMouseRightButtonDownScene2()


# Функція для обробки натискання правої кнопки миші на другій сцені
def handleMouseRightButtonDownScene2():
    if pygame.mouse.get_pressed()[2]:
        for ship in ships:
            if ship.rect.collidepoint(pygame.mouse.get_pos()):
                ship.rotateShip()


# Функція для оновлення кораблів
def updateShips():
    global ships

    for ship in ships:
        ship.update()
        ship.draw(screen)


# Функція для оновлення екрана
def updateScreen():
    global currentScene
    screen.fill((255, 255, 255))
    if currentScene == 1:
        drawFirstScene()
    elif currentScene == 2:
        drawSecondScene(gameParam)
    pygame.display.flip()


# Основний цикл гри
while True:
    handleEvents()
    updateScreen()
