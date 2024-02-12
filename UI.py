import pygame
import sys

# Определение класса DraggableEllipse
from DraggableEllipse import DraggableEllipse

# Определение функции отрисовки кораблей
def getShip(size, x, y, count):
    ellipses = []
    for i in range(count):
        ellipses.append(DraggableEllipse(x, y, size, (0, 0, 0)))
        x += size * 40
    return ellipses


# Определение функции создания списка кораблей
def getShips():
    ships = getShip(4, 100, 180, 1)
    ships.extend(getShip(3, 100, 230, 2))
    ships.extend(getShip(2, 100, 280, 3))
    ships.extend(getShip(1, 100, 330, 4))
    return ships


# Инициализация списка кораблей
ships = getShips()

# Инициализация Pygame
pygame.init()

# Определение констант
WIDTH, HEIGHT = 1200, 700
BUTTON_SIZE = 40
GRID_OFFSET = 250
BUTTON_WIDTH_FIRST_SCENE = 350
BUTTON_HEIGHT_FIRST_SCENE = 250
BUTTON_SIZE_FIRST_SCENE = (BUTTON_WIDTH_FIRST_SCENE, BUTTON_HEIGHT_FIRST_SCENE)
EXIT_BUTTON_WIDTH = 100
EXIT_BUTTON_HEIGHT = 50
CELLS_TEXT = 'ADCDEFGHIJ'

# ... (остальные константы)

# Создание окна Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battleship game")

# Инициализация переменных
currentScene = 1
buttonWithFriend = pygame.Rect(170, 200, BUTTON_WIDTH_FIRST_SCENE, BUTTON_HEIGHT_FIRST_SCENE)
buttonWithComputer = pygame.Rect(630, 200, BUTTON_WIDTH_FIRST_SCENE, BUTTON_HEIGHT_FIRST_SCENE)
buttonExit = pygame.Rect(WIDTH - 110, 10, 100, 50)
randomButton = pygame.Rect(450, 535, 140, 30)
buttonImageFriend = pygame.image.load("images/buttonFriend.jpg")
buttonImageFriend = pygame.transform.scale(buttonImageFriend, BUTTON_SIZE_FIRST_SCENE)
buttonImageComputer = pygame.image.load("images/buttonComputer.jpg")
buttonImageComputer = pygame.transform.scale(buttonImageComputer, BUTTON_SIZE_FIRST_SCENE)

text = ''


# Определение функции отрисовки кнопки
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

        if text == 'Random placement':
            font = pygame.font.Font(None, 20)
        else:
            font = pygame.font.Font(None, 35)

        text = font.render(text, True, (0, 0, 0))
        screen.blit(text, (rect.x + (rect.width - text.get_width()) // 2,
                               rect.y + (rect.height - text.get_height()) // 2))

# Определение функций отрисовки сцен
def drawFirstScene():
    drawButton(buttonExit, None, "Вийти")
    drawButton(buttonWithFriend, buttonImageFriend, None)
    drawButton(buttonWithComputer, buttonImageComputer, None)

# Определение функции обработки событий
def handleEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif pygame.mouse.get_pressed()[0]:
            handleMouseButtonDown(event)
        elif not pygame.mouse.get_pressed()[0]:
            handleMouseButtonUp()


# Определение функции обработки нажатия кнопки мыши
def handleMouseButtonDown(event):
    global currentScene
    if buttonExit.collidepoint(event.pos):
        if currentScene == 1:
            pygame.quit()
            sys.exit()
        else:
            currentScene -= 1
    if currentScene == 1:
        handleMouseButtonDownScene1(event)


# Определение функции обработки нажатия кнопки мыши на первой сцене
def handleMouseButtonDownScene1(event):
    global currentScene
    global text
    if buttonWithFriend.collidepoint(event.pos):
        currentScene = 2
        text = "With friend"
    elif buttonWithComputer.collidepoint(event.pos):
        currentScene = 2
        text = "With computer"

# Определение функции обработки отпускания кнопки мыши
def handleMouseButtonUp():
    return None


# Определение функции обновления экрана
def updateScreen():
    global currentScene
    screen.fill((255, 255, 255))
    if currentScene == 1:
        drawFirstScene()
    pygame.display.flip()


# Основной цикл игры
while True:
    handleEvents()
    updateScreen()
