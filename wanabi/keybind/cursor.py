import tkinter as tk

class CursorMove:
    def __init__(self, page):
        """
        カーソルを移動するテキストエリアを代入
        :param page: tk.Text]
        """
        self.page = page

    def line_head_move(self, event=None,) -> None:
        """
        行頭へカーソルを移動
        :param event: None
        :return: None
        """
        begin: str = self.page.index("insert")
        begin: int = int(begin[0])
        self.page.mark_set("insert", str(begin) + ".0")
        return None

    def line_tail_move(self, event=None) -> None:
        """
        行末へカーソルを移動
        :param event: None
        :return: None
        """
        end: str = self.page.search("\n", "insert", stopindex="insert+1l")
        if end == "":
            return None
        self.page.mark_set("insert", end)
        return None