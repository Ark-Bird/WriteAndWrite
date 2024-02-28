import os.path
import tkinter as tk
from tkinter import messagebox

import extend_exception
import inmemory_module.ram_memo
from keybind import keybind


class Memory(inmemory_module.ram_memo.RamMemo):
    def __init__(self, page):
        super().__init__()
        self.page: tk.Text = page

    def set_text(self, event=None) -> None:
        """
        Ctrl-mでアプリ終了、もしくは新規記録時までメモリ上にテキストメモを保存
        :param event:
        :return:
        """
        try:
            self.new_memo(self.page.get(tk.SEL_FIRST, tk.SEL_LAST))
        except tk.TclError:
            pass
        except Exception:
            raise extend_exception.FatalError
        return

    def show_memory(self, event=None) -> str:
        """
        Ctrl-oでメモリ上に保存されたテキストを表示
        :param event:
        :return:
        """
        messagebox.showinfo("Memory", self.remember())
        return "break"


class FontChange:
    def __init__(self, now_font_size, page):
        self.now_font_size = now_font_size
        self.page = page
        self.now_font_size = 13
        if os.path.exists("conf/font-size.txt"):
            try:
                with open("conf/font-size.txt") as fs:
                    enable_font, font_size = fs.read().split()
                if enable_font == "True":
                    self.now_font_size = int(font_size)
            except FileNotFoundError:
                messagebox.showinfo("File Not Found", "ファイルが見つかりません")
            except TypeError:
                messagebox.showinfo("ファイルのフォーマットが正しくありません", "新規作成します")
                with open("conf/font-size.txt", "w") as fs:
                    fs.write("False 13")
            except Exception:
                messagebox.showerror("Error", "致命的なエラーです")
                raise extend_exception.FatalError
        else:
            os.makedirs("./conf/", exist_ok=True)
            with open("conf/font-size.txt", "w") as fs:
                fs.write("False 10")
        self.page.configure(font=("", self.now_font_size))

    def font_size_big(self, event=None) -> None:
        """
        フォントサイズを拡大する
        対象は__init__で渡されたself.page
        :param event:
        :return:
        """
        self.now_font_size = self.now_font_size + 5
        if self.now_font_size >= 50:
            self.now_font_size = 50
        self.page.configure(font=("", self.now_font_size))
        return

    def font_size_small(self, event=None) -> None:
        """
        フォントサイズを縮小する
        対象は__init__で渡されたself.page
        :param event:
        :return:
        """
        self.now_font_size = self.now_font_size - 5
        if self.now_font_size <= 6:
            self.now_font_size = 6
        self.page.configure(font=("", self.now_font_size))
        return


def page_scroll_set(root, page) -> None:
    """
    tk.Scrollbarで縦と横のスクロールバーをrootウインドウに付けて、
    それでテキストエリアがスクロールするように設定
    :param root:スクロールバーを憑けるウインドウ
    :param page: スクロールバーでスクロールする要素
    :return: 無し
    """
    # テキストエリアを配置し、スクロールバーを付ける
    horizontal_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=page.xview)
    vertical_scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=page.yview)
    vertical_scrollbar.pack(side=tk.RIGHT, fill="y")
    horizontal_scrollbar.pack(side=tk.BOTTOM, fill="x")
    page.pack(fill="both", expand=True)
    page["yscrollcommand"] = vertical_scrollbar.set
    page["xscrollcommand"] = horizontal_scrollbar.set
    return


def vi_mode_change(page) -> None:
    """
    カーソル移動をCtrl-h,j,k,lに変更
    :param page:
    :return:
    """
    original_key_bind = keybind.ViMode(page)
    original_key_bind.edit_key_bind()
    return


def emacs_mode_change(page) -> None:
    """
    カーソル移動をCtrl-f,b,n,pに変更
    :param page:
    :return:
    """
    original_key_bind = keybind.EmacsMode(page)
    original_key_bind.edit_key_bind()
    return


def init_textarea(root, author, page, decorate, indent, font_change) -> None:
    """
    テキストエリアの初期設定とキーバインドの設定を行う
    初期化処理なので一度だけ呼ばれる
    :param root:ウインドウ
    :param author:　メインインスタンス
    :param page: テキストエリア
    :param decorate: 文字の装飾モジュール
    :param indent: インデントの有無と半角全角を決定
    :param font_change:フォントのサイズ変更
    :return: 無し
    """
    font = font_change
    page_scroll_set(root, page)
    # ファイルを保存
    page.bind("<Control-s>", author.save_file)
    # コピペ＆カット
    # page.bind("<Control-c>", author.text_copy)
    # page.bind('<Control-v>', author.text_paste)
    # page.bind("<Control-x>", author.text_cut)
    # 三点リーダー二つ組挿入
    page.bind("<Control-t>", decorate.three_point)
    # ダッシュの挿入
    page.bind("<Control-d>", decorate.double_dash)
    # ルビを振る
    page.bind("<Control-r>", decorate.ruby)
    # 傍点をつける
    page.bind("<Control-.>", decorate.dot_mark)
    # オートインデント
    # 半角全角切り替え
    page.bind("<Control-w>", indent.toggle_half_or_full)
    # オートインデントのオン・オフ
    page.bind("<Control-q>", indent.toggle_auto_indent)
    # オートセーブ
    page.bind("<Control-e>", author.toggle_autosave_flag)
    # エンターが押された場合、IMEの変換で押したものか改行をしたのかを判断してオートインデントを行う
    page.bind("<KeyPress-Return>", indent.ime_check)
    page.bind(
        "<KeyRelease-Return>",
        indent.indent_system
    )
    # インメモリメモ
    memo = Memory(page)
    page.bind("<Control-m>", memo.set_text)
    page.bind("<Control-o>", memo.show_memory)
    # 文字カウント
    page.bind("<Any-KeyPress>", author.logger)
    # 現在のファイルパス
    page.bind("<Control-0>", author.file_full_name_show)
    # フォントの拡大縮小
    page.bind("<Control-L>", font.font_size_big)
    page.bind("<Control-S>", font.font_size_small)
    # キーバインド設定
    original_key_bind = keybind.ViMode(author)
    original_key_bind.edit_key_bind()
    return


class ModeChange:
    def __init__(self, author):
        self.author = author

    def change_vi_mode(self) -> None:
        """
        カーソル移動をViライクなモードに変更
        :return:
        """
        my_key_bind = keybind.ViMode(self.author)
        my_key_bind.edit_key_bind()
        self.author.change_vi_mode_flag()
        return

    def change_emacs_mode(self) -> None:
        """
        カーソル移動をEmacs方式に変更
        :return:
        """
        my_key_bind = keybind.EmacsMode(self.author)
        my_key_bind.edit_key_bind()
        self.author.change_emacs_mode_flag()
        return
