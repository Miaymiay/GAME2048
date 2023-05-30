# установки через терминал:
# pip install -r requirements.txt

# подключение библиотек
import sqlite3
import pygame
import random
import numpy as np

# библиотека для диалогового окна
from tkinter import Tk
from tkinter import messagebox

from pygame import Surface
from pygame.font import Font


# СОЗДАНИЕ КЛАССА С ИГРОЙ 2048
class Game2048:

    # конструктор класса
    def __init__(self) -> None:
        self.state: str = "menu"
        # установка значений для полей класса
        self.size = 4  # колво строк/столбцов ячеек
        self.cellSize = 150  # размер клетки
        self.borderWidth = 3  # ширина рамки
        # цвет фона окна (рамки сетки)
        self.windowBgColor = (187, 173, 160)
        # размер игрового поля
        self.fieldSize = self.cellSize + self.borderWidth * 2
        # размеры окна
        self.windowWidth = self.fieldSize * 4
        self.windowHeight = self.windowWidth + 100

        # цветовая палитра игрового поля
        self.colors = {
            0: (205, 193, 181),  # цвет пустой клетки
            2: (240, 228, 218),  # цвет клетки со значением 2
            4: (236, 224, 200),  # цвет клетки со значением 4
            8: (241, 177, 121),  # цвет клетки со значением 8
            16: (244, 149, 103),  # цвет клетки со значением 16
            32: (245, 124, 97),  # цвет клетки со значением 32
            64: (247, 95, 59),  # цвет клетки со значением 64
            128: (237, 204, 112),  # цвет клетки со значением 128
            256: (237, 204, 100),  # цвет клетки со значением 256
            512: (237, 201, 85),  # цвет клетки со значением 512
            1024: (237, 190, 70),  # цвет клетки со значением 1024
            2048: (237, 182, 38)  # цвет клетки со значением 2048
        }

        # инициализация окна программы
        pygame.init()
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.Font = pygame.font.SysFont("Sans serif", 75)
        self.TextFont = pygame.font.SysFont("Sans serif", 45)
        pygame.display.set_caption("My game: 2048")
        self.cells = None

    def drawPanel(self):  # Отрисовка верхней панели
        textSurface = self.TextFont.render(f"Счёт: {int(self.cells.sum())}", True, (0, 0, 0))
        self.window.blit(textSurface, (260, 40))

    # отрисовка игрового поля
    def drawField(self):

        # обход каждой ячеки на поле для ее отрисовки по строкам и столбцам
        for row in range(self.size):
            rectY = self.fieldSize * row + self.borderWidth
            for col in range(self.size):
                rectX = self.fieldSize * col + self.borderWidth
                # получение значения из массива ячеек для отрисовки
                cellValue = int(self.cells[row][col])
                # рисуем клетку заданного цвета, в заданном месте, заданного размера
                pygame.draw.rect(
                    self.window,
                    self.colors[cellValue],
                    pygame.Rect(rectX, rectY + 100, self.cellSize, self.cellSize)
                )

                # если есть цифра в ячейке, вывести ее
                if cellValue != 0:
                    textSurface = self.Font.render(f"{cellValue}", True, (0, 0, 0))
                    textRect = textSurface.get_rect(
                        center=(rectX + self.fieldSize / 2, rectY + 100 + self.fieldSize / 2))
                    self.window.blit(textSurface, textRect)

    # добавление значение в пустую ячейку
    def addValueToCell(self):
        # получение списка свободных ячеек для установки значения 2
        position = zip(*np.where(self.cells == 0))
        position = list(position)
        for pos in random.sample(position, k=1):
            self.cells[pos] = 2

    # умножение подходящих значений в массиве на 2
    def multiplyingValues(self, data):
        result = [0]
        # поиск в массиве значений, не равных нулю
        data = [x for x in data if x != 0]
        # обход всех элементов массива
        for element in data:
            # если значения совпадают, умножим значение на 2
            if element == result[len(result) - 1]:
                result[len(result) - 1] *= 2
                # одну ячейку обнулить
                result.append(0)
            else:
                result.append(element)

        result = [x for x in result if x != 0]
        return result

    # смещение значений в ячейках
    def move(self, direction):
        # смещение в четыре направления: up, down, left, right
        for i in range(self.size):

            # смещение вверх или низ
            if direction in "UD":
                data = self.cells[:, i]
            else:
                data = self.cells[i, :]

            flip = False
            # если смещение вправо или низ, сделаем разворот значений
            if direction in "RD":
                flip = True
                data = data[::-1]

            # выполнение умножения подходящих значений в массиве на 2
            data = self.multiplyingValues(data)
            data = data + (self.size - len(data)) * [0]

            if flip: data = data[::-1]

            # смещение вверх или низ
            if direction in "UD":
                self.cells[:, i] = data
            else:
                self.cells[i, :] = data

    # проверка окончания игры
    def isGameOver(self):
        # создание копии массива значений ячеек
        backupCells = self.cells.copy()
        # выполнение смещения
        for _dir in "UDLR":
            self.move(_dir)
            # игра будет закончена, если ячейки не поменя свое расположение
            # и все ячейки заполнены значениями
            if not (self.cells == backupCells).all():
                self.cells = backupCells
                return False
        return True  # игра будет завершена

    def enter(self):
        self.state = "play"
        # инициализация массива ячеек игрового поля из нулей
        self.cells = np.zeros((self.size, self.size))
        # добавление значения в пустою ячейку
        self.addValueToCell()

    def history(self):
        self.state = "history"

    def drawMenu(self):
        if self.cells is not None:
            textSurface = self.TextFont.render(f"Счёт: {int(self.cells.sum())}", True, (0, 0, 0))
        else:
            textSurface = self.TextFont.render(f"Счёт: {0}", True, (0, 0, 0))
        self.window.blit(textSurface, (self.windowWidth // 2 - 50, self.windowHeight // 2 - 200))
        Button(self.windowWidth // 2 - 65, self.windowHeight // 2 - 100, 150, 50, self.colors, self.window, "Играть",
               self.enter, self.TextFont)
        Button(self.windowWidth // 2 - 65, self.windowHeight // 2, 150, 50, self.colors, self.window, "История",
               self.history, self.TextFont)

    def drawHistory(self):
        rectX = self.windowWidth / 2 - 65
        pygame.draw.rect(
            self.window,
            self.colors[0],
            pygame.Rect(rectX - 110, 20, 400, 120)
        )
        textSurface = self.Font.render(f"История игр", True, (0, 0, 0))
        textRect = textSurface.get_rect(center=(rectX + self.fieldSize / 2, 50))
        self.window.blit(textSurface, textRect)
        textSurface = self.Font.render(f"последние 10", True, (0, 0, 0))
        textRect = textSurface.get_rect(center=(rectX + self.fieldSize / 2, 100))
        self.window.blit(textSurface, textRect)

        rows = self.get_history()

        for i, (_id, amount) in enumerate(rows):
            rectY = 100 + 60 * (i + 1)
            # рисуем клетку заданного цвета, в заданном месте, заданного размера
            pygame.draw.rect(
                self.window,
                self.colors[0],
                pygame.Rect(rectX, rectY, 200, 50)
            )
            textSurface = self.Font.render(f"{_id}) {amount}", True, (0, 0, 0))
            textRect = textSurface.get_rect(center=(rectX + self.fieldSize / 2, rectY + 25))
            self.window.blit(textSurface, textRect)

    def save(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO points (amount) VALUES (?)", [int(self.cells.sum())])
        conn.commit()
        conn.close()

    @staticmethod
    def get_history() -> list[tuple[int, int]]:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, amount FROM points ORDER BY id DESC LIMIT 10")
        rows = cursor.fetchall()
        conn.close()
        return rows

    # работа игры
    def play(self):
        # установка флага для постоянной работы игры
        while True:
            # закрашивание окна заданным цветом
            self.window.fill(self.windowBgColor)
            # отрисовка игрового поля
            if self.state == "play":
                self.drawPanel()
                self.drawField()
            elif self.state == "menu":
                self.drawMenu()
            elif self.state == "history":
                self.drawHistory()
            elif self.state == "exit":
                break

            # обновление данных
            pygame.display.update()

            # обработка событий
            for event in pygame.event.get():
                if self.state == "play":
                    oldCells = self.cells.copy()

                    # выход из бесконечного цикла
                    if event.type == pygame.QUIT:
                        self.state = "exit"
                        break
                    # обработка нажатия клавиш
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.move("U")
                        elif event.key == pygame.K_DOWN:
                            self.move("D")
                        elif event.key == pygame.K_LEFT:
                            self.move("L")
                        elif event.key == pygame.K_RIGHT:
                            self.move("R")
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "menu"
                            break

                        # проверка окончания игры
                        if self.isGameOver():
                            self.save()
                            self.drawMenu()
                            self.state = "menu"
                            break

                        # добавление значение в ячейку
                        elif not (self.cells == oldCells).all():
                            self.addValueToCell()
                elif self.state == "menu":
                    if event.type == pygame.QUIT:
                        self.state = "exit"
                        break
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "exit"
                        break
                elif self.state == "history":
                    if event.type == pygame.QUIT:
                        self.state = "menu"
                        break
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                        break
            if self.state == "exit":
                break
            for _object in objects:
                _object.process()


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, colors, window: Surface, buttonText, onclickFunction,
                 TextFont: Font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.colors = colors
        self.window = window

        self.buttonRect = pygame.draw.rect(
            self.window,
            self.colors[0],
            pygame.Rect(self.x, self.y, self.width, self.height)
        )

        self.buttonSurface = TextFont.render(buttonText, True, (0, 0, 0))
        self.textRect = self.buttonSurface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        self.window.blit(self.buttonSurface, self.textRect)

        self.alreadyPressed = False

        objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.colors[2])
        self.window.blit(self.buttonSurface, self.textRect)
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.colors[4])
            self.window.blit(self.buttonSurface, self.textRect)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.colors[8])
                self.window.blit(self.buttonSurface, self.textRect)
                if not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurface, [
            self.buttonRect.width / 2 - self.buttonSurface.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurface.get_rect().height / 2
        ])
        self.window.blit(self.buttonSurface, self.buttonRect)


# главная функция программы
if __name__ == "__main__":
    objects: list[Button] = list()
    Tk().wm_withdraw()  # to hide the main window
    messagebox.showinfo("Игра - 2048", "Для управления, используйте клавиши: up,down,left,right.\n"
                                       "Для выхода нажмите: Esc.\n"
                                       "Приятной игры!")
    # инициализация объекта класса
    game = Game2048()
    # вызов метода класса, для работы игры
    game.play()
