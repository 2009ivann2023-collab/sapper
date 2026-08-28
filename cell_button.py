import customtkinter as ctk


class CellButton(ctk.CTkButton):
    def __init__(self, master, row, col, left_click_callback, right_click_callback, **kwargs):
        super().__init__(master, text="", width=35, height=35, fg_color="#3a3a3a", font=("Arial", 14, "bold"), **kwargs)
        self.row = row
        self.col = col

        # Прив'язка кліків
        self.configure(command=lambda: left_click_callback(self.row, self.col))
        self.bind("<Button-3>", lambda event: right_click_callback(self.row, self.col))  # Правий клік (Прапорець)

    def set_number(self, value):
        self.configure(state="disabled", fg_color="#2b2b2b")
        if value > 0:
            colors = {1: "#1f77b4", 2: "#2ca02c", 3: "#d62728", 4: "#9467bd", 5: "#8c564b"}
            text_color = colors.get(value, "#e377c2")
            self.configure(text=str(value), text_color_disabled=text_color)
        else:
            self.configure(text="")

    def set_flag(self, has_flag):
        if has_flag:
            self.configure(text="🚩", fg_color="#555555")
        else:
            self.configure(text="", fg_color="#3a3a3a")

    def set_mine(self, exploded=False):
        bg = "#ff4444" if exploded else "#555555"
        self.configure(text="💣", fg_color=bg, state="disabled")