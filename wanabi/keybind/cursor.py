import tkinter as tk

class Cursor:
    def __init__(self, page):
        self.page = page

    def line_head_move(self, event=None,) -> None:
        begin: str = self.page.search("\n", "insert-1l", stopindex="insert+1l")
        newline: int = int(begin[0])
        if begin == "":
            return None
        if newline == 1:
            self.page.mark_set("insert", "1.0")
            return None
        self.page.mark_set("insert", begin)
        self.page.mark_set("insert", "insert+1c")
        return None

    def line_tail_move(self, event=None) -> None:
        end: str = self.page.search("\n", "insert", stopindex="insert+1l")
        if end == "":
            return None
        self.page.mark_set("insert", end)
        return None