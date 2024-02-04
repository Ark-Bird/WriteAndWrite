#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 20:47:33 2017
@author: hiro
"""
import tkinter
# import tkinter.font as tkfont
import os
import platform
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import independent_method
import menu_init
import vinegar
import textarea_config
from independent_method import ignore
import string_decorate
import indent_insert
import theme_mod
import full_mode
import extend_exception

"""
Copyright 2020 hiro

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


class WillBeAuthor:
    """
    The God class
    """

    path = ""
    ftext = ""
    is_save = True

    def __init__(self):
        """
        変数初期化
        len:文字数
        file:ファイル名
        cliptext:クリップボードのテキスト
        pstxt:ペースとするテキスト
        auto_indent:オートインデントのフラグ
        half_space:オートインデントの全角/半角切り替え
        hit_return:IMEの文字決定と改行の区別フラグ
        is_save:セーブ済みフラグ
        is_exit:終了可能フラグ
        ASFLAG:オートセーブフラグ
        txtc:クリップボードのクリア
        theme:現在のテーマ
        theme_f:テーマが変更フラグ
        blank_line:空行かどうかのフラグ
        """
        self.file: str = ""
        self.basename: str = ""
        self.is_changed: bool = False
        self.clipped_text: str = ""
        self.pasting_text: str = ""
        self.is_save: bool = True
        self.is_exit: bool = False
        self.is_autosave_flag: bool = False
        self.dark_mode: bool = False
        self.title_var_string: str = ""
        self.theme: str = self.read_theme()
        self.copied_text = ""
        self.page = None
        self.root = None
        self.file = ""
        self.theme = ""
        self.init = True
        self.blank_line = False
        self.indent = None
        self.before_text = ""
        self.prev_save_file = ""
        self.prev_text = ""
        self.cursor_move_mode = "vi"

        try:
            self.theme = self.read_theme()
        except FileNotFoundError:
            ignore()
        except Exception:
            raise extend_exception.FatalError

    def setroot(self, root) -> None:
        """
        rootウインドウの参照を受け取り、クラス内で扱えるようにする
        :return:
        """
        self.root = root
        return

    def read_theme(self) -> str:
        """
        テーマファイルを読み込み、テーマ名を返す
        ファイルが存在しなければnormalでcolor.binを作成
        :return: color.binに書かれたテーマ名
        """
        try:
            with open("color.bin", "r") as f:
                self.theme = f.read()
        except FileNotFoundError:
            print("設定ファイルが存在しないためcolor.binを作成します")
            independent_method.write_theme_string("normal")
            self.theme = "normal"
        except UnicodeDecodeError:
            print("テーマにユニコード以外の文字列が含まれています")
            self.theme = "normal"
        except Exception:
            raise extend_exception.FatalError
        return self.theme

    def set_theme(self, theme="normal") -> None:
        """
        テーマをファイルから読み込みchange_theme関数に渡す
        :param theme: 変更するテーマ、デフォルトでnormal
        """
        independent_method.write_theme_string(theme)
        theme = self.read_theme()
        theme_mod.change_theme(self.page, theme=theme)
        return None

    def logger(self, event=None) -> None:
        """
        テキストの変更を検知して変更フラグを立てる
        終了時にセーブするか訊ねるようにする
        文字カウントの変更
        Ctrlとの組み合わせに対応
        基本的に何かのキーが押された時に呼ばれる
        """
        self.change_titlebar()
        if self.before_text != self.page.get("0.0", "end"):
            self.is_save = False
        elif self.before_text == self.page.get("0.0", "end"):
            self.is_save = True
        self.is_text_changed()
        return

    def counter(self) -> int:
        """
        文字カウント
        loggerから呼ばれる
        カウントした文字はタイトルバーに表示
        オートインデント有効の場合タイトルバーに表示
        自動セーブの有効無効をタイトルバーに表示
        """
        s: str = self.page.get("0.0", "end")
        # vt = " a \t b\r\n\tc\t\n"
        s = s.replace(' ', '')
        s = s.replace('　', '')
        s = s.replace('\n', '')
        s = s.replace('\r', '')
        vt = "".join(s.split())
        text_length_without_whitespace = len(vt)
        return text_length_without_whitespace

    def change_titlebar(self) -> None:
        """
        タイトルバーの文字列を変更
        """
        character_num = self.counter()
        auto_indent, half_space = self.indent.auto_indent_enable_and_half_space_checker()
        self.title_var_string = str(character_num) + ":  文字"

        if not self.is_save:
            self.title_var_string += "*未保存*:"
        elif self.is_save and not self.init:
            self.title_var_string += ":保存済み:"
        else:
            self.init = False
        self.title_var_string = "I want Be... :" + self.title_var_string
        if auto_indent:
            if half_space:
                self.title_var_string += "*AI半角*"
            else:
                self.title_var_string += "*AI全角*"
        else:
            self.title_var_string += "*AI無効"
        if self.is_autosave_flag:
            self.title_var_string += ":auto_save_enable:"
        else:
            self.title_var_string += ":auto_save_disable:"
        if self.cursor_move_mode == "vi":
            self.title_var_string += "Vi mode:"
        elif self.cursor_move_mode == "emacs":
            self.title_var_string += "Emacs mode:"
        self.blank_line = False
        self.title_var_string += os.path.basename(self.file)
        self.root.title(self.title_var_string)
        return

    def repeat_save_file(self) -> None:
        """
        オートセーブ
        """
        if self.prev_save_file == "" and self.is_autosave_flag:
            self.prev_save_file = filedialog.asksaveasfilename(filetypes=[("txt files", "*.txt")],
                                                               initialdir=self.prev_save_file)
            independent_method.write_filename_string(self.prev_save_file)
        try:
            with open("path.bin", "r", encoding="utf-8") as fname:
                # self.prev_save_dir = os.path.abspath(os.path.dirname(fname.readline()))
                self.prev_save_file = os.path.abspath(fname.readline())
        except UnicodeDecodeError:
            print("パスがユニコードではありません")
            self.prev_save_file = os.path.abspath(os.path.dirname(__file__))
        except extend_exception.NotOpenPathException:
            print("パスが無効です")
            self.prev_save_file = os.path.abspath(os.path.dirname(__file__))
        if self.prev_save_file == "":
            print("assert!")
            self.prev_save_file = tk.filedialog.asksaveasfilename(filetypes=[("txt files", "*.txt")],
                                                                  initialdir=self.prev_save_file)
        try:
            independent_method.write_filename_string(self.prev_save_file)
        except FileNotFoundError:
            independent_method.write_filename_string("")
        except Exception:
            raise extend_exception.FatalError
        self.change_titlebar()
        if self.is_autosave_flag:
            self.is_save = True
            self.save_file()
            self.before_text = self.page.get("0.0", "end")
        self.root.after(1000, self.repeat_save_file)
        return

    def toggle_as_flag(self, event=None) -> None:
        """
        オートセーブフラグのトグル
        self.ASFLAG:オートセーブのフラグ
        :return:無し
        """
        if self.is_autosave_flag:
            self.change_auto_save_disable()
        else:
            self.change_auto_save_enable()
        self.change_titlebar()
        return

    def change_auto_save_enable(self) -> None:
        """
        オートセーブフラグが有効ならオートセーブを毎秒呼び出し
        フラグが立っていない場合無視
        テーマの変更が無い場合Falseを送って変更しない
        :return:無し
        """
        self.is_autosave_flag = True

    def change_auto_save_disable(self):
        """
        オートセーブ機能の無効化
        :return:
        """
        self.is_autosave_flag = False

    def save_as(self) -> None:
        """
        clear file name
        名前をつけて保存
        返り値なし
        """
        self.file = ""
        self.save_file()
        self.is_save = True
        return

    def save_file(self, event=None) -> None:
        """
        SAVE file with dialog
        ファイルの保存処理
        path.binを開いて前回のファイル保存先を開く
        存在しなければNotOpenPathException例外を投げる
        失敗時Falseをリターン
        """
        # 前回の保存場所を参照
        try:
            if not os.path.exists("path.bin"):
                raise extend_exception.NotOpenPathException
            with open("path.bin", mode="r", encoding="utf-8") as f:
                prev_save_directory = os.path.abspath(os.path.dirname(f.readline()))
        except extend_exception.NotOpenPathException:
            prev_save_directory = os.path.abspath(os.path.dirname(__file__))

        if self.file == "":
            self.file = tk.filedialog.asksaveasfilename(
                filetypes=[("txt files", "*.txt")], initialdir=prev_save_directory
            )
        if self.file == "":
            self.change_auto_save_disable()
            return
        if not self.file:
            self.file = ""
            return
        if True:
            self.ftext = self.page.get("0.0", "end")
            self.ftext = self.ftext[0:-1]
        if self.file[-4:] != ".txt":
            self.file += ".txt"
        if self.before_text == self.page.get("0.0", "end"):
            return
        with open(self.file, mode="w", encoding="utf-8") as f:
            f.write(self.ftext)
        with open("./path.bin", mode="w", encoding="utf-8") as f:
            f.write(self.file)
        self.is_text_unchanged()
        self.is_save = True
        self.change_titlebar()
        return

    def exit_as_save(self) -> None:
        """
        終了時の保存処理
        保存されていなければ確認ダイアログを表示
        :return:終了時ウインドウの破棄、キャンセル時、空のリターン
        """
        if not self.is_save:
            save_exit = messagebox.askyesno("ファイルが変更されています", "ファイルを保存しますか？")
            if save_exit:
                self.save_as()
            if messagebox.askyesno("終了しますか？", "終了しますか？"):
                self.is_exit = True
        if self.is_exit or self.is_save:
            self.root.destroy()
        else:
            return

    def new_blank_file(self) -> None:
        """
        clear text field
        テキストをクリアして新しいファイルにする
        変更フラグを降ろす
        保存フラグを立てる
        """
        self.ftext = self.page.get("0.0", "end")
        self.prev_save_file = ""
        if not self.is_save:
            if messagebox.askyesno("保存しますか?", "ファイルが変更されています、保存しますか?"):
                self.save_as()
            if not messagebox.askyesno("破棄しますか？", "文書を破棄しますか？"):
                return
        self.page.delete("0.0", "end")
        self.file = ""
        self.is_text_unchanged()
        self.file = ""
        self.is_save = True
        self.change_auto_save_disable()
        self.change_titlebar()
        return

    def open_text_file(self) -> None:
        """
        FILE OPEN dialog
        ファイルを開く
        変更されていたらチェック
        存在しないディレクトリをを指定していたらスクリプトのディレクトリを開く
        """
        if self.page.get("0.0", "end") != "\n" and self.is_changed:
            if not messagebox.askyesno("注意", "ファイルが変更されています、破棄しますか？"):
                return
        # paht.binは前回保存したディレクトリが書き込まれている
        try:
            if not os.path.exists("path.bin"):
                raise extend_exception.NotOpenPathException
            with open("path.bin", mode="r", encoding="utf-8") as f:
                directory_before_saved = f.readline()
        except extend_exception.NotOpenPathException:
            directory_before_saved = os.path.abspath(os.path.dirname(__file__))
        self.file = tk.filedialog.askopenfilename(initialdir=directory_before_saved)
        if self.file == "":
            return
        self.prev_save_file = self.file
        try:
            with open(self.file, encoding="utf-8_sig") as f:
                loaded = f.read()
        except UnicodeDecodeError:
            messagebox.showerror("文字コードエラー", "ファイルがUTF-8ではありません")
            return
        self.page.delete("0.0", "end")
        self.page.insert("0.0", loaded)
        self.is_text_changed()
        self.change_auto_save_disable()
        self.change_titlebar()
        return

    def path_to_filename(self, filepath) -> str:
        self.basename = os.path.basename(self.file)

    def text_copy(self, event=None) -> None:
        """
        copy text
        テキストの範囲が選択されていなかった場合例外を投げ、握りつぶす
        """
        try:
            # 選択範囲をクリップボードにコピー
            self.clipped_text = self.page.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.copied_text = self.clipped_text
        except tk.TclError:
            # 問題の無い例外は握りつぶす
            ignore()
        except Exception:
            # どうしようもない例外でエラーをレイズ
            raise extend_exception.FatalError
        return

    def text_paste(self, event=None) -> None:
        """
        paste text
        範囲を選択していなかった場合の例外は握りつぶす
        tk.TclError以外のエラーが出ると落ちる
        返り値無し
        """
        try:
            # self.pstxt = self.cliptext
            self.page.insert("insert", self.copied_text)
        # 選択範囲がない場合例外が投げられる
        except tk.TclError:
            # 問題の無いエラー（握りつぶす）
            ignore()
        except Exception:
            # 致命的なエラー
            raise extend_exception.FatalError
        return

    def text_cut(self, event=None) -> None:
        """
        cut text
        返り値無し
        TclError以外の例外が投げられると落ちる
        """
        try:
            # ローカル変数とクリップボードにコピー
            self.clipped_text = self.page.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.copied_text = self.clipped_text
            self.page.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            # 選択範囲がない場合例を投げられるので握りつぶす
            ignore()
        except Exception:
            print("致命的なエラー")
            raise extend_exception.FatalError
        return

    def is_text_changed(self) -> None:
        """
        テキストの変更フラグを立てる
        テキストエリアでキーが押されると呼ばれる
        :return:無し
        """
        self.is_changed = True
        return

    def is_text_unchanged(self) -> None:
        """
        テキストが変更されていない場合呼ばれてis_changedをFalseにする
        :return:
        """
        self.is_changed = False

    def set_page(self, page) -> None:
        """
        テキストエリアの参照pageをインスタンス変数に参照渡し
        :param page:テキストエリアの参照
        :return:
        """
        self.page = page

    def set_indent(self, indent):
        """
        インデントの詳細指定をするクラスをフィールドに渡す
        :param indent:
        :return:
        """
        self.indent = indent

    def change_vi_mode_flag(self):
        self.cursor_move_mode = "vi"

    def change_emacs_mode_flag(self):
        self.cursor_move_mode = "emacs"

    def file_full_name_show(self, event=None):
        if self.file == "":
            messagebox.showinfo("Not open", "現在ファイルを開いていません")
            return "break"
        messagebox.showinfo("現在のファイル", self.file)
        return "break"


def res_path(rel: str) -> str:
    """
    Windowsの場合、アイコンへのパスを返す
    他のOSの場合は呼ばれることはない
    exe化時にバイナリのフォルダにresフォルダを作成すること
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, rel)
    return os.path.join(os.path.abspath("."), rel)


def init_page(page: tk.Text):
    """
    テキストエリアの初期化処理
    :param page:テキストエリアのインスタンス
    :return:
    """
    decorate = string_decorate.StringDecorator(page)
    pkvin = vinegar.Vinegar(page)
    return decorate, pkvin


def main() -> None:
    """
    主処理系
    if __name__ == "__main__"から呼ばれる
    グローバル変数を閉じ込めるためだけの関数
    """
    # Windowsもしくはそれ以外を判別
    pf: str = platform.system()
    author: WillBeAuthor = WillBeAuthor()
    root = tk.Tk()
    author.setroot(root)
    full_screen = full_mode.FullMode()
    full_screen.set_root_full_mode(root)
    root.geometry("640x640")
    page = tk.Text(root, undo=True, wrap=tkinter.NONE)
    decorate, pk1vin = init_page(page)
    indent = indent_insert.Indent(author, page)
    author.set_indent(indent)
    author.set_page(page)
    # 動いているOSの判別
    # このif節をコメントアウトしてからバイナリ化すればアイコンファイルをコピーせずに実行可能,その場合アイコンはPythonのデフォルトになります
    # アイコンファイルが見つからない場合はデフォルトアイコンで起動
    try:
        if pf == "Windows":
            icon = "./res/wbe.ico"
            root.iconbitmap(icon)
        else:
            root.wm_iconbitmap("@./res/wbe.xbm")
    except tkinter.TclError:
        ignore()
    theme = author.read_theme()
    author.set_theme(theme=theme)
    root.minsize(32, 32)
    menubar = tk.Menu(root)

    menu_init.menu_init(author, menubar, pk1vin, indent, full_screen)

    # タイトル
    root.config(menu=menubar)
    root.title("I Want Be...")
    author.change_titlebar()
    root.configure(background="gray")

    textarea_config.init_textarea(root, author, page, decorate, indent)

    root.protocol("WM_DELETE_WINDOW", author.exit_as_save)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    # オートセーブその他の再帰呼び出し
    root.after(1000, author.repeat_save_file)
    root.mainloop()


if __name__ == "__main__":
    main()
