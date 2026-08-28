import customtkinter as ctk
from game_logic import MinesweeperEngine
from cell_button import CellButton

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MinesweeperGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Сапер на Python")
        self.geometry("450x550")
        self.resizable(False, False)

        # Параметри поля
        self.rows = 10
        self.cols = 10
        self.mines = 12

        # Ініціалізація логіки
        self.engine = MinesweeperEngine(self.rows, self.cols, self.mines)

        # Верхня панель з інформацією
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(pady=15, padx=20, fill="x")

        self.status_label = ctk.CTkLabel(self.top_frame, text=f"Міни: {self.mines}", font=("Arial", 16, "bold"))
        self.status_label.pack(side="left", padx=20, pady=10)

        self.restart_btn = ctk.CTkButton(self.top_frame, text="🔄 Нова гра", width=100, command=self.restart_game)
        self.restart_btn.pack(side="right", padx=20, pady=10)

        # Ігрове поле
        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(pady=5, padx=20)

        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.create_grid()

    def create_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = CellButton(self.grid_frame, r, c, self.on_left_click, self.on_right_click)
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[r][c] = btn

    def on_left_click(self, r, c):
        results = self.engine.reveal_cell(r, c)

        for item in results:
            if item[0] == "LOSE":
                self.game_over_screen(r, c)
                return

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
        # Відкриваємо всі міни на полі
        for r in range(self.rows):
            for c in range(self.cols):
                if self.engine.board[r][c] == -1:
                    is_exploded = (r == exploded_r and c == exploded_c)
                    self.buttons[r][c].set_mine(exploded=is_exploded)
                else:
                    self.buttons[r][c].configure(state="disabled")

    def restart_game(self):
        # Очищення старого інтерфейсу
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # Скидання логіки та створення нового поля
        self.engine = MinesweeperEngine(self.rows, self.cols, self.mines)
        self.status_label.configure(text=f"Міни: {self.mines}", text_color="#ffffff")
        self.create_grid()


if __name__ == "__main__":
    app = MinesweeperGUI()
    app.mainloop()