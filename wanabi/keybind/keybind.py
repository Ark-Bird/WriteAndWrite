import ctypes


class KeyBindMode:
    def __init__(self, author):
        self.author = author
        self.vi_insert_mode = None
        self.vi_command_mode = None

    def cursor_move_forward(self, event=None) -> str | None:
        if self.if_enable_ime():
            return
        self.author.page.mark_set("insert", "insert+1c")
        return "break"

    def cursor_move_next_line(self, event=None) -> str | None:
        if self.if_enable_ime():
            return
        self.author.page.mark_set("insert", "insert+1lines")
        return "break"

    def cursor_move_prev_line(self, event=None) -> str | None:
        if self.if_enable_ime():
            return
        self.author.page.mark_set("insert", "insert-1lines")
        return "break"

    def cursor_move_backward(self, event=None) -> str | None:
        if self.if_enable_ime():
            return
        self.author.page.mark_set("insert", "insert-1c")
        return "break"

    def bind_free(self, event=None) -> None:
        pass

    def insert_mode(self, event=None) -> str:
        self.vi_insert_mode = True
        self.vi_insert_mode = ViInsertMode(self.author)
        self.vi_insert_mode.edit_key_bind()
        return "break"

    def disable_emacs_mode(self) -> str:
        self.author.page.bind("<Control-b>", self.bind_free)
        self.author.page.bind("<Control-n>", self.bind_free)
        self.author.page.bind("<Control-p>", self.bind_free)
        self.author.page.bind("<Control-f>", self.bind_free)
        return "break"

    def disable_vi_mode(self) -> str:
        self.author.page.bind("<h>", self.bind_free)
        self.author.page.bind("<j>", self.bind_free)
        self.author.page.bind("<k>", self.bind_free)
        self.author.page.bind("<l>", self.bind_free)
        return "break"

    def set_vi_mode(self) -> str:
        self.author.page.bind("<h>", self.bind_free)
        self.author.page.bind("<j>", self.bind_free)
        self.author.page.bind("<k>", self.bind_free)
        self.author.page.bind("<l>", self.bind_free)
        return "break"

    def insert_ignor(self, event=None) -> None:
        pass

    def command_mode(self, event=None) -> None:
        self.vi_command_mode = ViCommandMode(self.author)
        self.vi_command_mode.edit_key_bind()

    def if_enable_ime(self) -> False:
        wnd = ctypes.WinDLL(name="user32")
        himc = ctypes.WinDLL(name="imm32")
        ime_handle = wnd.GetForegroundWindow()
        h_im = himc.ImmGetContext(ime_handle)
        stat = himc.ImmGetOpenStatus(h_im)
        if stat:
            ctypes.windll.imm32.ImmReleaseContext(ime_handle, h_im)
            return True
        ctypes.windll.imm32.ImmReleaseContext(ime_handle, h_im)
        return False


class ViCommandMode(KeyBindMode):
    def edit_key_bind(self) -> None:
        self.disable_emacs_mode()
        self.author.page.bind("<h>", self.cursor_move_backward)
        self.author.page.bind("<j>", self.cursor_move_next_line)
        self.author.page.bind("<k>", self.cursor_move_prev_line)
        self.author.page.bind("<l>", self.cursor_move_forward)
        self.author.page.bind("<i>", self.insert_mode)
        return


class ViInsertMode(KeyBindMode):
    def edit_key_bind(self) -> None:
        self.author.page.bind("<i>", self.insert_ignor)
        self.author.page.bind("<Escape>", self.command_mode)

class EmacsMode(KeyBindMode):
    def edit_key_bind(self) -> None:
        self.disable_vi_mode()
        self.author.page.bind("<Control-b>", self.cursor_move_backward)
        self.author.page.bind("<Control-n>", self.cursor_move_next_line)
        self.author.page.bind("<Control-p>", self.cursor_move_prev_line)
        self.author.page.bind("<Control-f>", self.cursor_move_forward)
        return
