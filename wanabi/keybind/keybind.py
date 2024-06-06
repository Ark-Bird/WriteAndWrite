class KeyBindMode:
    def __init__(self, author):
        self.author = author

    def cursor_move_forward(self, event=None) -> str:
        self.author.page.mark_set("insert", "insert+1c")
        return "break"

    def cursor_move_next_line(self, event=None) -> str:
        self.author.page.mark_set("insert", "insert+1lines")
        return "break"

    def cursor_move_prev_line(self, event=None) -> str:
        self.author.page.mark_set("insert", "insert-1lines")
        return "break"

    def cursor_move_backward(self, event=None) -> str:
        self.author.page.mark_set("insert", "insert-1c")
        return "break"


class ViMode(KeyBindMode):
    def edit_key_bind(self) -> None:
        self.author.page.bind("<Control-h>", self.cursor_move_backward)
        self.author.page.bind("<Control-j>", self.cursor_move_next_line)
        self.author.page.bind("<Control-k>", self.cursor_move_prev_line)
        self.author.page.bind("<Control-l>", self.cursor_move_forward)
        return


class EmacsMode(KeyBindMode):
    def edit_key_bind(self) -> None:
        self.author.page.bind("<Control-b>", self.cursor_move_backward)
        self.author.page.bind("<Control-n>", self.cursor_move_next_line)
        self.author.page.bind("<Control-p>", self.cursor_move_prev_line)
        self.author.page.bind("<Control-f>", self.cursor_move_forward)
        return
