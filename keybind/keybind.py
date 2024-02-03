import tkinter as tk


class KeyBind:
    def __init__(self, page):
        self.page = page

    def edit_key_bind(self):
        self.page.bind("<Control-b>", self.cursor_move_back)
        self.page.bind("<Control-n>", self.cursor_move_next_line)
        self.page.bind("<Control-p>", self.cursor_move_prev_line)
        self.page.bind("<Control-f>", self.cursor_move_forward)

    def cursor_move_forward(self, event=None):
        self.page.mark_set("insert", "insert+1c")

    def cursor_move_next_line(self, event=None):
        self.page.mark_set("insert", "insert+1lines")

    def cursor_move_prev_line(self, event=None):
        self.page.mark_set("insert", "insert-1lines")

    def cursor_move_back(self, event=None):
        self.page.mark_set("insert", "insert-1c")

