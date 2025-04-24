import pygame
from cell import Cell
from sudoku_generator import generate_sudoku

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.selected_cell = None

        if difficulty == "easy":
            removed = 30
        elif difficulty == "medium":
            removed = 40
        elif difficulty == "hard":
            removed = 50
        else:
            removed = 40

        self.original_board = generate_sudoku(9, removed)
        self.cells = [[Cell(self.original_board[row][col], row, col, screen) for col in range(9)] for row in range(9)]

    def draw(self):
        for i in range(10):
            line_width = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * 60), (540, i * 60), line_width)
            pygame.draw.line(self.screen, (0, 0, 0), (i * 60, 0), (i * 60, 540), line_width)

        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        if self.selected_cell:
            self.selected_cell.selected = False
        self.selected_cell = self.cells[row][col]
        self.selected_cell.selected = True

    def click(self, x, y):
        if 0 <= x < 540 and 0 <= y < 540:
            col = x // 60
            row = y // 60
            return (row, col)
        return None

    def clear(self):
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_cell_value(value)
            self.selected_cell.set_sketched_value(0)

    def reset_to_original(self):
        for row in range(9):
            for col in range(9):
                val = self.original_board[row][col]
                self.cells[row][col].set_cell_value(val)
                self.cells[row][col].set_sketched_value(0)

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        self.board = [[self.cells[row][col].value for col in range(9)] for row in range(9)]

    def find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value == 0:
                    return (row, col)
        return None

    def check_board(self):
        self.update_board()
        for i in range(9):
            row = self.board[i]
            col = [self.board[r][i] for r in range(9)]
            if len(set(row)) != 9 or len(set(col)) != 9:
                return False

        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                box = []
                for r in range(3):
                    for c in range(3):
                        box.append(self.board[i + r][j + c])
                if len(set(box)) != 9:
                    return False
        return True
