import ctypes
import tkinter.messagebox

class KeyBindMode:
    def __init__(self, author):
        self.author = author
        self.vi_insert_mode = None
        self.vi_command_mode = None
        self.is_windows = False
        self.is_windows_flag = False


    def check_windows(self):
        try:
            with open("conf/platforms.txt", "r", encoding=self.author.code) as bindtype:
                self.is_windows_flag = bindtype.read()
            if self.is_windows_flag == "Windows":
                self.is_windows = True
                return self.is_windows
            else:
                self.is_windows = False
                return self.is_windows
        except FileNotFoundError:
            pfask = tkinter.messagebox.askyesno("win or No win", "Windowsを使用していますか？")
            if pfask:
                with open("conf/platforms.txt", "w", encoding=self.author.code) as bindtype:
                    bindtype.write("Windows")
                    self.is_windows = True
                    return self.is_windows
            else:
                with open("conf/platforms.txt", "w", encoding=self.author.code) as bindtype:
                    bindtype.write("AnotherOS")
                    self.is_windows = False
                    tkinter.messagebox.showwarning("このアプリを再起動してください", "Windows以外で使用する場合、初期設定のために再起動をしてください")
                    self.author.exit_as_save()
                    return self.is_windows
        except:
            raise Exception

    def cursor_move_forward(self, event=None) -> str | None:
        if not self.check_windows():
            return "break"
        if self.if_enable_ime():
            return "break"
        self.author.page.mark_set("insert", "insert+1c")
        return "break"

    def cursor_move_next_line(self, event=None) -> str | None:
        if not self.check_windows():
            return "break"
        if self.if_enable_ime():
            return "break"
        self.author.page.mark_set("insert", "insert+1lines")
        return "break"

    def cursor_move_prev_line(self, event=None) -> str | None:
        if not self.check_windows():
            return "break"
        if self.if_enable_ime():
            return "break"
        self.author.page.mark_set("insert", "insert-1lines")
        return "break"

    def cursor_move_backward(self, event=None) -> str | None:
        if not self.check_windows():
            return "break"
        if self.if_enable_ime():
            return "break"
        self.author.page.mark_set("insert", "insert-1c")
        return "break"

    def bind_free(self, event=None) -> None:
        pass

    def insert_mode(self, event=None) -> str:
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
        self.author.page.bind("<Control-h>", self.bind_free)
        self.author.page.bind("<Control-j>", self.bind_free)
        self.author.page.bind("<Control-k>", self.bind_free)
        self.author.page.bind("<Control-l>", self.bind_free)
        return "break"

    def set_vi_mode(self) -> str | None:
        self.author.page.bind("<h>",self.cursor_move_backward)
        self.author.page.bind("<j>", self.cursor_move_next_line)
        self.author.page.bind("<k>", self.cursor_move_prev_line)
        self.author.page.bind("<l>", self.cursor_move_forward)
        self.author.page.bind("<x>", self.erase_char)
        return "break"

    def set_insert_vi_ime_enable(self) -> None:
        self.author.page.bind("<Control-h>", self.cursor_move_backward)
        self.author.page.bind("<Control-j>", self.cursor_move_next_line)
        self.author.page.bind("<Control-k>", self.cursor_move_prev_line)
        self.author.page.bind("<Control-l>", self.cursor_move_forward)

    def insert_ignor(self, event=None) -> None:
        pass

    def command_mode(self, event=None) -> None:
        self.vi_command_mode = ViCommandMode(self.author)
        self.vi_command_mode.edit_key_bind()

    def if_enable_ime(self) -> bool | None:
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

    def erase_char(self, event=None) -> str:
        self.author.page.delete("insert")
        return "break"


class ViCommandMode(KeyBindMode):
    def edit_key_bind(self) -> None:
        self.disable_emacs_mode()
        if not self.check_windows():
            self.insert_mode()
            return
        self.set_vi_mode()
        self.author.vi_mode_now = "command mode"
        self.author.page.bind("<i>", self.insert_mode)
        return


class ViInsertMode(KeyBindMode):
    def edit_key_bind(self) -> None:
        self.disable_vi_mode()
        self.author.vi_mode_now = "insert mode"
        self.author.page.bind("<i>", self.insert_ignor)
        self.author.page.bind("<Escape>", self.command_mode)
        self.author.page.bind("<Control-[>", self.command_mode)

class EmacsMode(KeyBindMode):
    def edit_key_bind(self) -> None:
        self.author.vi_mode_now = ""
        self.disable_vi_mode()
        self.author.page.bind("<Control-b>", self.cursor_move_backward)
        self.author.page.bind("<Control-n>", self.cursor_move_next_line)
        self.author.page.bind("<Control-p>", self.cursor_move_prev_line)
        self.author.page.bind("<Control-f>", self.cursor_move_forward)
        return
