#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 20:47:33 2017
@author: hiro
"""
import tkinter
import tkinter.font
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
import version

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

    def __init__(self):
        """
        変数初期化
        file:ファイル名
        cliptext:クリップボードのテキスト
        pstxt:ペースとするテキスト
        self.indent:オートインデントのフラグ
        half_space:オートインデントの全角/半角切り替え
        hit_return:IMEの文字決定と改行の区別フラグ
        is_save:セーブ済みフラグ
        is_exit:終了可能フラグ
        is_autosave_flag:オートセーブフラグ
        txtc:クリップボードのクリア
        theme:現在のテーマ
        theme_f:テーマが変更フラグ
        blank_line:空行かどうかのフラグ
        self.cursor_move_mode:カーソル移動のモード、デフォルトでviスタイルライク
        """
        self.file: str = ""
        self.ftext: str = ""
        self.is_changed: bool = False
        self.clipped_text: str = ""
        self.pasting_text: str = ""
        self.is_save: bool = True
        self.is_exit: bool = False
        self.is_init: bool = True
        self.is_autosave_flag: bool = False
        self.title_var_string: str = ""
        self.copied_text = ""
        self.page: tk.Text = None
        self.root: tk.Tk = None
        self.init: bool = True
        self.indent: indent_insert.Indent = None
        self.before_text: str = "\n"
        self.prev_save_dir: str = ""
        self.cursor_move_mode: str = "vi"
        self.is_wrap: bool = True
        self.app_name: version.ShowInfo = version.ShowInfo()
        try:
            self.theme: str = self.read_theme()
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
            with open("conf/color.bin", "r") as f:
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
        引数themeで渡されたテーマをファイルに書き込んでテーマの変更
        :param theme: 変更するテーマ、デフォルトでnormal
        """
        independent_method.write_theme_string(theme)
        theme_mod.change_theme(self.page, theme=theme)
        return

    def logger(self, event=None) -> None:
        """
        テキストの変更を検知して変更フラグを立てる
        終了時にセーブするか訊ねるようにする
        文字カウントの変更
        Ctrlとの組み合わせに対応
        基本的に何かのキーが押された時に呼ばれる
        """
        self.change_titlebar()
        self.is_save = False
        self.is_text_changed()
        self.is_init = False
        return

    def counter(self) -> int:
        """
        文字カウント
        テキストエリアから全文を読んで空白をトリムした長さを返す
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
        text_length_without_whitespace: int = len(vt)
        return text_length_without_whitespace

    def erase_newline(self) -> None:
        """
        連続した空行を削除する
        :return: None
        """
        if messagebox.askyesno("空行を削除しますか？", "テキストの空行を削除しますか？"):
            s: str = self.page.get("0.0", "end")
            s = s.replace('\n\n', '\n')
            self.page.delete("0.0", "end")
            self.page.insert("0.0", s)
        return

    def text_is_save(self) -> None:
        """
        テキストが初期状態、もしくは未保存か保存済みかを書き換えるメソッド
        :return: None
        """
        if self.file == "" and self.page.get("0.0", "end") == "\n":
            self.title_var_string += ":無題:"
        # 保存の有無
        elif not self.is_save:
            self.title_var_string += "*未保存*:"
        elif self.is_save and not self.init:
            self.title_var_string += ":保存済み:"
        else:
            self.init = False

    def cursor_move_vi_or_emacs(self) -> str:
        """
        現在のカーソル移動モードを文字列で返す
        :return: 現在の移動モードの文字列
        """
        # カーソル移動の方法
        if self.cursor_move_mode == "vi":
            return "Vi mode:"
        elif self.cursor_move_mode == "emacs":
            return "Emacs mode:"

    def change_titlebar(self) -> None:
        """
        タイトルバーの文字列を変更
        """
        auto_indent, half_space = self.indent.auto_indent_enable_and_half_space_checker()
        self.title_var_string = str(self.counter()) + ":  文字"
        # インデントの半角/全角
        self.text_is_save()
        self.title_var_string = self.app_name.return_app_name_for_now() + self.title_var_string
        # オートインデントの半角/全角状態の表示
        if auto_indent:
            if half_space:
                self.title_var_string += "*AI半角*"
            else:
                self.title_var_string += "*AI全角*"
        else:
            self.title_var_string += "*AI無効"
        # オートセーブは有効か
        if self.is_autosave_flag:
            self.title_var_string += ":auto_save_enable:"
        else:
            self.title_var_string += ":auto_save_disable:"
        # カーソル移動の方法
        self.title_var_string += self.cursor_move_vi_or_emacs()
        self.title_var_string += self.path_to_filename(self.file)
        self.root.title(self.title_var_string)
        return

    def repeat_save_file(self) -> None:
        """
        オートセーブ
        ファイルパスはユニコードであること
        """
        if self.prev_save_dir == "" and self.is_autosave_flag:
            self.prev_save_dir = filedialog.asksaveasfilename(filetypes=[("txt files", "*.txt")],
                                                              initialdir=self.prev_save_dir)
            independent_method.write_filename_string(self.prev_save_dir)
        try:
            with open("conf/path.bin", "r", encoding="utf-8") as text_filename:
                self.prev_save_dir = os.path.abspath(text_filename.readline())
        except UnicodeDecodeError:
            print("パスがユニコードではありません")
            self.prev_save_dir = os.path.abspath(os.path.dirname(__file__))
        except FileNotFoundError:
            independent_method.write_filename_string(__file__)
            print("パスファイルを作成します")
        except extend_exception.NotOpenPathException:
            print("パスが無効です")
            self.prev_save_dir = os.path.abspath(os.path.dirname(__file__))
        if self.prev_save_dir == "/":
            print("assert!")
            independent_method.write_filename_string(self.prev_save_dir)
        try:
            independent_method.write_filename_string(self.prev_save_dir)
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

    def toggle_autosave_flag(self, event=None) -> None:
        """
        オートセーブフラグのトグル
        self.is_autosave_flag:オートセーブのフラグ
        :return:None
        """
        if self.is_autosave_flag:
            self.change_auto_save_disable()
        else:
            self.change_auto_save_enable()
        self.change_titlebar()
        return

    def change_auto_save_enable(self) -> None:
        """
        オートセーフのフラグを有効にする
        :return:None
        """
        self.is_autosave_flag = True
        return

    def change_auto_save_disable(self) -> None:
        """
        オートセーブ機能の無効化
        :return:None
        """
        self.is_autosave_flag = False
        return

    def save_as(self) -> None:
        """
        clear file name
        名前をつけて保存
        :return:None
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
            if not os.path.exists("conf/path.bin"):
                raise extend_exception.NotOpenPathException
            with open("conf/path.bin", mode="r", encoding="utf-8") as f:
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
        with open("conf/path.bin", mode="w", encoding="utf-8") as f:
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
        s = self.page.get("0.0", "end")
        if not self.is_save:
            save_exit = messagebox.askyesno("ファイルが変更されています", "ファイルを保存しますか？")
            if save_exit:
                self.save_as()
            if messagebox.askyesno("終了しますか？", "終了しますか？"):
                self.is_exit = True
        if self.is_exit or self.is_save or s == "\n":
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
        self.prev_save_dir = ""
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
        self.init = True
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
            if not os.path.exists("conf/path.bin"):
                raise extend_exception.NotOpenPathException
            with open("conf/path.bin", mode="r", encoding="utf-8") as f:
                directory_before_saved = f.readline()
        except extend_exception.NotOpenPathException:
            directory_before_saved = os.path.abspath(os.path.dirname(__file__))
        self.file = tk.filedialog.askopenfilename(initialdir=directory_before_saved)
        if self.file == "":
            return
        self.prev_save_dir = self.file
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

    def path_to_filename(self, filepath) -> None:
        """
        ファイルパスのファイル名を抜き出してself.basenameに代入
        :param filepath:
        :return:ファイル名
        """
        basename = os.path.basename(filepath)
        return basename

    def text_copy(self, event=None) -> None:
        """
        copy text
        テキストの範囲が選択されていなかった場合例外を投げ、握りつぶす
        """
        try:
            # 選択範囲をクリップボードにコピー
            self.clipped_text = self.page.get(tk.SEL_FIRST, tk.SEL_LAST)
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
            self.page.insert("insert", self.clipped_text)
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
        :return:None
        """
        self.is_changed = False
        return

    def set_page(self, page) -> None:
        """
        テキストエリアの参照pageをインスタンス変数に参照渡し
        :param page:テキストエリアの参照
        :return:None
        """
        self.page = page
        return

    def set_indent(self, indent) -> None:
        """
        インデントの詳細指定をするクラスをフィールドに渡す
        :param indent:
        :return:None
        """
        self.indent = indent
        return

    def change_vi_mode_flag(self) -> None:
        """
        カーソル移動をViライクに変更
        :return:None
        """
        self.cursor_move_mode = "vi"
        return

    def change_emacs_mode_flag(self) -> None:
        """
        カーソル移動をEmacsライクに変更
        :return:None
        """
        self.cursor_move_mode = "emacs"
        return

    def file_full_name_show(self, event=None) -> str:
        if self.file == "":
            messagebox.showinfo("Not open", "現在ファイルを開いていません")
            return "break"
        messagebox.showinfo("現在のファイル", self.file)
        return "break"

    def wrap_enable(self) -> None:
        """
        テキストエリアの橋で自動で折り返すように設定する
        :return:
        """
        self.is_wrap = True
        self.page.configure(wrap=tk.CHAR)
        return

    def wrap_disable(self) -> None:
        """
        テキストエリアの折り返しを無効化する
        :return:
        """
        self.is_wrap = False
        self.page.configure(wrap=tk.NONE)
        return


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
    conf_exist: bool = os.path.isdir("conf")
    if not conf_exist:
        os.makedirs("conf", exist_ok=True)
    author: WillBeAuthor = WillBeAuthor()
    root: tk.Tk = tk.Tk()
    author.setroot(root)
    font: tk.font.Font = tk.font.Font(root, family="IPAexゴシック")
    full_screen: full_mode.FullMode = full_mode.FullMode()
    full_screen.set_root_full_mode(root)
    root.geometry("640x640")
    page: tk.Text = tk.Text(root, undo=True, wrap=tkinter.CHAR)
    font_size: int = 13
    font_change = textarea_config.FontChange(font_size, page)
    decorate, pk1vin = init_page(page)
    indent: indent_insert.Indent = indent_insert.Indent(author, page)
    author.set_indent(indent)
    author.set_page(page)
    # 動いているOSの判別
    # このif節をコメントアウトしてからバイナリ化すればアイコンファイルをコピーせずに実行可能,その場合アイコンはPythonのデフォルトになります
    # アイコンファイルが見つからない場合はデフォルトアイコンで起動
    try:
        if pf == "Windows":
            icon: str = "res/wbe.ico"
            root.iconbitmap(icon)
        else:
            root.wm_iconbitmap("@./res/wbe.xbm")
    except tkinter.TclError:
        ignore()

    # オートインデントの設定
    try:
        with open("conf/auto_indent.txt", "r") as default_indent:
            indent_flag = default_indent.read()
            if indent_flag == "True":
                indent.toggle_auto_indent()
    except FileNotFoundError:
        with open("conf/auto_indent.txt", "w") as default:
            default.write("False")
    except Exception:
        raise extend_exception.FatalError
    theme: str = author.read_theme()
    author.set_theme(theme=theme)
    root.minsize(32, 32)
    menubar: tk.Menu = tk.Menu(root, font=font)

    menu_init.menu_init(author, menubar, pk1vin, indent, full_screen, font_change)

    # タイトル
    root.config(menu=menubar)
    root.title("インクの跡は全て文字")
    author.change_titlebar()
    root.configure(background="gray")

    textarea_config.init_textarea(root, author, page, decorate, indent, font_change)

    root.protocol("WM_DELETE_WINDOW", author.exit_as_save)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    # オートセーブその他の再帰呼び出し
    root.after(1000, author.repeat_save_file)
    root.mainloop()


if __name__ == "__main__":
    main()
