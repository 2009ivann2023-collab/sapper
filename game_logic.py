import random


class MinesweeperEngine:
    def __init__(self, rows=10, cols=10, mines=15):
        self.rows = rows
        self.cols = cols
        self.mines_count = mines

        # Матриці для стану гри
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]  # Кількість мін навколо (-1 = міна)
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]  # Чи відкрита клітинка
        self.flags = [[False for _ in range(cols)] for _ in range(rows)]  # Чи стоїть прапорець

        self.first_click = True
        self.game_over = False
        self.won = False

    def generate_board(self, start_row, start_col):
        """Генерує міни, оминаючи місце першого кліку гравця"""
        mines_placed = 0
        while mines_placed < self.mines_count:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)

            # Не ставимо міну туди, де вже є міна, або на клітину першого ходу
            if self.board[r][c] == -1 or (r == start_row and c == start_col):
                continue

            self.board[r][c] = -1
            mines_placed += 1

        # Підраховуємо цифри навколо мін
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    continue
                self.board[r][c] = self._count_adjacent_mines(r, c)

    def _count_adjacent_mines(self, row, col):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.board[nr][nc] == -1:
                        count += 1
        return count

    def reveal_cell(self, row, col):
        """Відкриває клітинку. Повертає список змінених клітинок (row, col, value)"""
        if self.game_over or self.revealed[row][col] or self.flags[row][col]:
            return []

        if self.first_click:
            self.generate_board(row, col)
            self.first_click = False

        changes = []

        # Якщо підірвався на міні
        if self.board[row][col] == -1:
            self.game_over = True
            return [("LOSE", row, col)]

        # Рекурсивне відкриття порожніх клітинок (ефект хвилі)
        def flood_fill(r, c):
            if not (0 <= r < self.rows and 0 <= c < self.cols) or self.revealed[r][c] or self.flags[r][c]:
                return
            self.revealed[r][c] = True
            changes.append((r, c, self.board[r][c]))

            if self.board[r][c] == 0:
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        flood_fill(r + dr, c + dc)

        flood_fill(row, col)
        self._check_win_condition()
        return changes

    def toggle_flag(self, row, col):
        """Ставить або знімає прапорець"""
        if self.game_over or self.revealed[row][col]:
            return None
        self.flags[row][col] = not self.flags[row][col]
        return self.flags[row][col]

    def _check_win_condition(self):
        """Гра виграна, якщо всі безпечні клітинки відкриті"""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != -1 and not self.revealed[r][c]:
                    return
        self.won = True
        self.game_over = True

