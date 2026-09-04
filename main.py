import customtkinter as ctk
from game_logic import MinesweeperEngine
from cell_button import CellButton

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MinesweeperGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Сапер на Python")
        # Розмір вікна з запасом для великих рівнів
        self.geometry("700x750")
        self.resizable(True, True)

        # Конфігурація поля за замовчуванням (Легкий рівень)
        self.rows = 10
        self.cols = 10
        self.mines = 12

        # Ініціалізація логіки
        self.engine = MinesweeperEngine(self.rows, self.cols, self.mines)

        # Верхня панель з інформацією
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(pady=15, padx=20, fill="x")

        # 1. Вибір складності
        self.difficulty_label = ctk.CTkLabel(self.top_frame, text="Складність:", font=("Arial", 12))
        self.difficulty_label.pack(side="left", padx=10, pady=10)

        self.difficulty_menu = ctk.CTkOptionMenu(
            self.top_frame,
            values=["Легкий (10x10)", "Середній (14x14)", "Важкий (18x18)"],
            width=140,
            command=self.change_difficulty
        )
        self.difficulty_menu.pack(side="left", padx=5, pady=10)

        # 2. Статус-лейбл (кількість мін або результат)
        self.status_label = ctk.CTkLabel(self.top_frame, text=f"Міни: {self.mines}", font=("Arial", 14, "bold"))
        self.status_label.pack(side="left", padx=20, pady=10)

        # 3. Кнопка перезапуску
        self.restart_btn = ctk.CTkButton(self.top_frame, text="🔄 Нова гра", width=100, command=self.restart_game)
        self.restart_btn.pack(side="right", padx=20, pady=10)

        # Ігрове поле
        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(pady=10, padx=20, expand=True)

        self.buttons = []
        self.start_new_session()

    def start_new_session(self):
        """Побудова нової ігрової сесії під обрані розміри"""
        self.engine = MinesweeperEngine(self.rows, self.cols, self.mines)
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.create_grid()

    def create_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = CellButton(self.grid_frame, r, c, self.on_left_click, self.on_right_click)
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[r][c] = btn

    def change_difficulty(self, choice):
        """Перемикач параметрів при виборі зі списку"""
        if choice == "Легкий (10x10)":
            self.rows, self.cols, self.mines = 10, 10, 12
        elif choice == "Середній (14x14)":
            self.rows, self.cols, self.mines = 14, 14, 25
        elif choice == "Важкий (18x18)":
            self.rows, self.cols, self.mines = 18, 18, 45

        self.restart_game()

    def on_left_click(self, r, c):
        results = self.engine.reveal_cell(r, c)

        for item in results:
            # ПЕРЕВІРКА: якщо перший елемент це рядок "LOSE"
            if isinstance(item, tuple) and item[0] == "LOSE":
                self.game_over_screen(r, c)
                return
            elif isinstance(item, str) and item == "LOSE":
                self.game_over_screen(r, c)
                return

            # Якщо це звичайна клітинка, розпаковуємо числа
            row, col, value = item
            self.buttons[row][col].set_number(value)

        if self.engine.won:
            self.status_label.configure(text="Ви перемогли! 🎉", text_color="#4BB543")

    def on_right_click(self, r, c):
        has_flag = self.engine.toggle_flag(r, c)
        if has_flag is not None:
            self.buttons[r][c].set_flag(has_flag)

    def game_over_screen(self, exploded_r, exploded_c):
        self.status_label.configure(text="Гра закінчена! 💥", text_color="#ff4444")
        # Показуємо всі міни на полі
        for r in range(self.rows):
            for c in range(self.cols):
                if self.engine.board[r][c] == -1:
                    is_exploded = (r == exploded_r and c == exploded_c)
                    self.buttons[r][c].set_mine(exploded=is_exploded)
                else:
                    self.buttons[r][c].configure(state="disabled")

    def restart_game(self):
        self.status_label.configure(text=f"Міни: {self.mines}", text_color="#ffffff")

        # Видаляємо старі віджети кнопок з екрану
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # Створюємо поле заново
        self.start_new_session()


if __name__ == "__main__":
    app = MinesweeperGUI()
    app.mainloop()