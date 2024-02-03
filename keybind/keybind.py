class KeyBind:
    def __init__(self, page):
        self.page = page

    def edit_key_bind(self):
        self.page.bind("<Control-n>", self.cursor_move_forward)
        self.page.bind("<Control-p>", self.cursor_move_back)

    def cursor_move_forward(self, event=None):
        self.page.mark_set("insert", "insert+1c")

    def cursor_move_back(self, event=None):
        self.page.mark_set("insert", "insert-1c")