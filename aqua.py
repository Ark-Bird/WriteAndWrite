#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 20:47:33 2017
@author: hiro
"""
import pickle
import tkinter
import tkinter.font as tkfont
import const
"""
Copyright 2020 hiro

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import os
import platform
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import independent_method
import pyperclip
import vinegar

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
        dark_mode:テーマがダークモードか
        col:現在のテーマ
        nowcolor:保存されたテーマ
        txtc:クリップボードのクリア
        theme:現在のテーマ
        theme_f:テーマが変更フラグ
        blank_line:空行かどうかのフラグ
        """
        self.file: str = ""
        self.is_changed: bool = False
        self.clipped_text: str = ""
        self.pasting_text: str = ""
        self.auto_indent: bool = False
        self.half_space: bool = False
        self.hit_return: bool = False
        self.is_save: bool = True
        self.is_exit: bool = False
        self.is_autosave_flag: bool = False
        self.dark_mode: bool = False
        self.col: str = ""
        self.title_var_string: str = ""
        self.theme: str = "normal"
        self.theme_f: bool = False
        if self.hit_return:
            self.blank_line = True
        else:
            self.blank_line = False
        try:
            with open("color.bin", mode="r", encoding="utf-8") as f:
                self.col = f.read()
                self.theme = f.read()
        except FileNotFoundError:
            ignore()
        if self.col == "dark":
            self.dark_mode = True
        self.MIT_LICENSE: str = """
Copyright 2020 hiro

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

    def logger(self, event) -> None:
        """
        テキストの変更を検知して変更フラグを立てる
        終了時にセーブするか訊ねるようにする
        文字カウントの変更
        Ctrlとの組み合わせに対応
        基本的に何かのキーが押された時に呼ばれる
        テキストの変更時、アンドゥ用のスタックに現在のテキストを積む
        """
        self.counter()
        self.is_save = False
        self.is_changed = True

    def counter(self) -> str:
        """
        文字カウント
        loggerから呼ばれる
        カウントした文字はタイトルバーに表示
        オートインデント有効の場合タイトルバーに表示
        自動セーブの有効無効をタイトルバーに表示
        """
        s: str = page.get("0.0", "end")
        # messagebox.showinfo('文字数(改行、スペース込み)', self.leng)
        # vt = " a \t b\r\n\tc\t\n"
        s = s.replace(' ', '')
        s = s.replace('　', '')
        s = s.replace('\n', '')
        s = s.replace('\r', '')
        vt = "".join(s.split())
        vanillal = len(vt)
        self.title_var_string = str(vanillal) + ":  文字"

        if not self.is_save:
            self.title_var_string += "*未保存*:"
        self.title_var_string = "I want Be... :" + self.title_var_string
        if self.auto_indent:
            if self.half_space:
                self.title_var_string += "*AI半角"
            else:
                self.title_var_string += "*AI全角"
        if self.is_autosave_flag:
            self.title_var_string += ":auto_save_enable:"
        else:
            self.title_var_string += ":auto_save_disable:"
        self.blank_line = False
        root.title(self.title_var_string)
        return self.title_var_string

    def autosave(self) -> None:
        """
        オートセーブ
        """
        if self.file == "":
            ignore()
        if self.is_autosave_flag:
            self.is_save = True
            self.save_file("file")
            root.after(1000, self.autosave)
        return

    def is_auto_save_enable(self) -> None:
        """
        オートセーブフラグが有効ならオートセーブを毎秒呼び出し
        フラグが立っていない場合無視
        テーマの変更が無い場合Falseを送って変更しない
        :return:無し
        """
        if self.is_autosave_flag:
            self.autosave()
        else:
            pass
        self.change_theme(False, self.theme)
        return

    def toggle_as_flag(self) -> None:
        """
        オートセーブフラグのトグル
        self.ASFLAG:オートセーブのフラグ
        :return:無し
        """
        if self.is_autosave_flag:
            self.is_autosave_flag = False
        else:
            self.is_autosave_flag = True
            self.is_auto_save_enable()
        return

    def save_as(self, types: str) -> None:
        """
        clear file name
        名前をつけて保存
        返り値なし
        """
        if types == "file":
            self.file = ""
        self.save_file(types)
        self.is_save = True
        return

    def save_file(self, types: str):
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
                raise independent_method.NotOpenPathException
            with open("path.bin", mode="r", encoding="utf-8") as f:
                iDir = os.path.abspath(os.path.dirname(f.readline()))
        except independent_method.NotOpenPathException:
            iDir = os.path.abspath(os.path.dirname(__file__))
        if types == "":
            return
        if self.file == "":
            self.file = tk.filedialog.asksaveasfilename(
                filetypes=[("txt files", "*.txt")], initialdir=iDir
            )
        if self.file == "":
            self.is_autosave_flag = False
            return
        if not self.file:
            self.file = ""
            return
        if types == "file":
            self.ftext = page.get("0.0", "end")
            self.ftext = self.ftext[0:-1]
        if self.file[-4:] != ".txt":
            self.file += ".txt"
        with open(self.file, mode="w", encoding="utf-8") as f:
            f.write(self.ftext)
        with open("./path.bin", mode="w", encoding="utf-8") as f:
            f.write(self.file)
            # if types == 'file':
            #     self.file = self.file
        self.is_changed = False
        self.is_save = True
        self.counter()
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
                self.save_as("file")
            if messagebox.askyesno("終了しますか？", "終了しますか？"):
                self.is_exit = True
        if self.is_exit or self.is_save:
            root.destroy()
        else:
            return

    def new_blank_file(self, types: str) -> None:
        """
        clear text field
        テキストをクリアして新しいファイルにする
        変更フラグを降ろす
        保存フラグを立てる
        """
        self.ftext = page.get("0.0", "end")
        if not self.is_save:
            if messagebox.askyesno("保存しますか?", "ファイルが変更されています、保存しますか?"):
                self.save_as("file")
            if not messagebox.askyesno("破棄しますか？", "文書を破棄しますか？"):
                return
        if types == "file":
            page.delete("0.0", "end")
            self.file = ""
        self.is_changed = False
        self.file = ""
        self.is_save = True
        return

    def open_text_file(self, types: str) -> None:
        """
        FILE OPEN dialog
        ファイルを開く
        変更されていたらチェック
        存在しないディレクトリをを指定していたらスクリプトのディレクトリを開く
        """
        if page.get("0.0", "end") != "\n" and self.is_changed:
            if not messagebox.askyesno("注意", "ファイルが変更されています、破棄しますか？"):
                return
        fTyp = [("", "*")]
        # paht.binは前回保存したディレクトリが書き込まれている
        try:
            if not os.path.exists("path.bin"):
                raise independent_method.NotOpenPathException
            with open("path.bin", mode="r", encoding="utf-8") as f:
                iDir = f.readline()
        except independent_method.NotOpenPathException:
            iDir = os.path.abspath(os.path.dirname(__file__))
        self.file = tk.filedialog.askopenfilename(initialdir=iDir)
        if self.file == "":
            return
        try:
            with open(self.file, encoding="utf-8_sig") as f:
                readed = f.read()
        except UnicodeDecodeError:
            messagebox.showerror("文字コードエラー", "ファイルがUTF-8ではありません")
            return
        page.delete("0.0", "end")
        page.insert("0.0", readed)
        self.t_change()
        return

    def text_copy(self) -> None:
        """
        copy text
        テキストの範囲が選択されていなかった場合例外を投げ、握りつぶす
        """
        try:
            # 選択範囲をクリップボードにコピー
            self.clipped_text = page.get(tk.SEL_FIRST, tk.SEL_LAST)
            pyperclip.copy(self.clipped_text)
        except tk.TclError:
            # 問題の無い例外は握りつぶす
            ignore()
        except Exception:
            # どうしようもない例外でエラーをレイズ
            raise independent_method.FatalError
        return

    def text_paste(self) -> None:
        """
        paste text
        範囲を選択していなかった場合の例外は握りつぶす
        tk.TclError以外のエラーが出ると落ちる
        返り値無し
        """
        try:
            # pyperclip.pasteを使うと文字化けする
            self.pasting_text = pyperclip.paste()
            # self.pstxt = self.cliptext
            page.insert("insert", self.pasting_text)
        # 選択範囲がない場合例外が投げられる
        except tk.TclError:
            # 問題の無いエラー（握りつぶす）
            ignore()
        except Exception:
            # 致命的なエラー
            raise independent_method.FatalError
        return

    def text_cut(self) -> None:
        """
        cut text
        返り値無し
        TclError以外の例外が投げられると落ちる
        """
        try:
            # ローカル変数とクリップボードにコピー
            # アプリ内で完結するならpyperclipは不要
            self.clipped_text = page.get(tk.SEL_FIRST, tk.SEL_LAST)
            pyperclip.copy(self.clipped_text)
            page.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            # 選択範囲がない場合例を投げられるので握りつぶす
            ignore()
        except Exception:
            print("致命的なエラー")
            raise independent_method.FatalError
        return

    def ruby(self) -> None:
        """
        テキストを選択してルビを振る
        選択範囲が十文字より多ければ警告を表示、十文字の基準は一般的なWEB小説投稿サイトの最長文字数、
        これ以上でも問題無く表示できるサイトもある、その場合該当業をコメントアウトすればよい
        ルビの書式は小説家になろう及びカクヨム、及びその互換書式に対応しています
        返り値無し
        """
        b = tk.SEL_FIRST
        i = tk.SEL_FIRST
        try:
            temp_str = page.get("sel.first", "sel.last")
            # 投稿サイトが10文字以上のルビに対応の場合、以下二行をコメントアウトしてください
            if len(temp_str) > 10:
                messagebox.showinfo("over", "10文字以上にルビは非対応の可能性があります")
            temp_str = "|" + temp_str + "《》"

            page.delete("sel.first", "sel.last")
            page.insert("insert", temp_str)
            page.mark_set("insert", "insert-1c")
        except tk.TclError:
            ignore()
        except Exception:
            raise independent_method.FatalError
        return

    def t_change(self) -> None:
        """
        テキストの変更フラグを立てる
        :return:無し
        """
        self.is_changed = True
        return

    def toggle_auto_indent(self) -> None:
        """
        オートインデント機能のオン・オフ
        返り値は無し
        挿入されるインデントは全角・半角はtoggle_half_or_full関数でトグルする
        デフォルトは全角スペース
        """
        self.auto_indent = not self.auto_indent
        self.counter()
        return

    def toggle_half_or_full(self) -> None:
        """
        オートインデントの半角全角切り替え
        """
        if self.half_space:
            self.half_space = False
        else:
            self.half_space = True
        return

    def insert_space(self) -> None:
        """
        オートインデント
        self.half_spaceがTrueのとき半角スペース、Falseの時全角スペースのインデントを挿入
        カーソルを移動して前の文字を調べ、空行と判断すればインデントを削除する
        """
        if self.hit_return:
            index = tk.INSERT
            if self.blank_line:
                prev = page.get("insert -3c")
                d = page.get("insert -2c")
                if (d == " " or d == "　") and prev == "\n":
                    page.delete("insert -2c")
                if self.half_space:
                    page.insert(index, " ")
                else:
                    page.insert(index, "　")
            self.hit_return = False
        return

    def ime_check(self) -> None:
        """
        IMEのリターンか、改行かの判断
        改行ならばインスタンス変数のhit_returnを立てる
        返り値無し
        """
        self.blank_line = True
        self.hit_return = True
        return

    def change_theme(self, theme_f, new_theme) -> None:
        """
        テーマの変更
        theme_fはテーマが変更されているかのフラグ、Falseの時即時リターン
        new_themeは変更するテーマ
        モード名をcolor.binに書き込む
        color.binに存在しないテーマ名が書き込まれていた場合標準テーマに変更
        該当ファイルはプレーンテキストでありマニュアルでの編集が可能
        ストレージへの負荷軽減のためモード変更のない場合ファイルへ書き込まずリターン
        """
        try:
            self.theme = new_theme
            # テーマが変更されていなければ即リターン
            self.theme_f = theme_f
        except FileNotFoundError:
            with open("color.bin", mode="w", encoding="utf-8") as f:
                self.theme = f.write("normal")
                return
        if not self.theme_f:
            return
        try:
            with open("color.bin", mode="r", encoding="utf-8") as f:
                self.theme = f.read()
            if self.theme_f:
                if self.theme == "normal":
                    self.theme = new_theme
                elif self.theme == "paper":
                    self.theme = new_theme
                elif self.theme == "dark":
                    self.theme = new_theme
                elif self.theme == "terminal":
                    self.theme = new_theme
                else:
                    self.theme = "normal"
        except FileNotFoundError:
            with open("color.bin", mode="w", encoding="utf-8") as f:
                self.theme = f.write("normal")
        if self.theme == "dark":
            self.write_theme("dark")
            page.configure(bg="gray16", fg="azure", insertbackground="white")
        elif self.theme == "paper":
            self.write_theme("paper")
            page.configure(bg="azure", fg="blueviolet", insertbackground="blueviolet")
        elif self.theme == "terminal":
            self.write_theme("terminal")
            page.configure(bg="black", fg="springgreen3", insertbackground="green")
        elif self.theme == "normal":
            self.write_theme("normal")
            page.configure(bg="ghost white", fg="black", insertbackground="black")
        self.theme_f = False
        return

    def write_theme(self, change_theme) -> None:
        with open("color.bin", mode="w", encoding="utf-8") as f:
            f.write(change_theme)
        return

    def is_modify(self) -> bool:
        """
        color.binを読み込み現在のモードと同じならFalseを返す
        変更されていない場合はTrueを返す
        ファイルが見つからなかった場合はnormalで開く、それ以外の例外なら終了
        returnは起こらず、その場合例外を投げる
        """
        try:
            with open("color.bin", mode="r", encoding="utf-8") as f:
                mode: str = f.read()
            if mode == self.theme:
                return True
            else:
                return False

        # ファイルが何らかの理由で存在しない場合normalを書き込んで作成
        except FileNotFoundError:
            with open("color.bin", mode="w", encoding="utf-8") as f:
                f.write("normal")
            return True
        except Exception:
            raise independent_method.FatalError
        # ここには到達しないはず
        raise independent_method.FatalError



    def show_license(self) -> None:
        tk.messagebox.showinfo("LICENSE", self.MIT_LICENSE)
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


def ignore() -> None:
    """
    何もしない
    例外を握りつぶす時等に使用
    passではなく明示的に握りつぶす
    """
    pass
    return


def theme_init()-> None:
    """
    カラーコンフィグ
    """
    try:
        with open("color.bin", mode="r", encoding="utf-8") as f:
            initialize_color: str = f.read()
        if initialize_color == "dark":
            page.configure(bg="gray16", fg="azure", insertbackground="white")
        elif initialize_color == "paper":
            page.configure(
                bg="azure", fg="blueviolet", insertbackground="blueviolet"
            )
        elif initialize_color == "terminal":
            page.configure(bg="black", fg="springgreen3", insertbackground="green")
        else:
            page.configure(bg="ghost white", fg="black", insertbackground="black")
    except FileNotFoundError:
        print("Error!")
        page.configure(bg="ghost white", fg="black", insertbackground="black")
    return

def view_version()->None:
    tk.messagebox.showinfo("バージョン情報:", version.get_const())
    return


if __name__ == "__main__":
    version: const = const.Const("0.1.6_β")
    # Windowsもしくはそれ以外を判別
    pf: str = platform.system()
    author: WillBeAuthor = WillBeAuthor()
    root = tk.Tk()
    root.geometry("640x640")
    page = tk.Text(root, undo=False, wrap=tkinter.NONE)
    pkvin = vinegar.Vinegar(page)
    # 動いているOSの判別
    # このif節をコメントアウトしてからバイナリ化すればアイコンファイルをコピーせずに実行可能,その場合アイコンはPythonのデフォルトになります
    # アイコンファイルが見つからない場合はデフォルトアイコンで起動
    try:
        if pf == "Windows":
            # icon = res_path('./res/wbe.ico')
            icon = "./res/wbe.ico"
            root.iconbitmap(icon)
        else:
            root.wm_iconbitmap("@./res/wbe.xbm")
    except tkinter.TclError:
        pass
    root.minsize(32, 32)
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    # ファイルメニュー、渡している'file'引数はダミー
    filemenu.add_command(label="新規ファイル", command=lambda: author.new_blank_file("file"))
    filemenu.add_command(label="開く", command=lambda: author.open_text_file("file"))
    filemenu.add_command(label="保存 (Ctrl-s)", command=lambda: author.save_file("file"))
    filemenu.add_command(label="名前をつけて保存", command=lambda: author.save_as("file"))
    filemenu.add_command(label="シリアライズして保存", command=lambda: pkvin.umeboshi())
    filemenu.add_command(label="デシリアライズして開く", command=lambda: pkvin.sunuki())
    filemenu.add_command(
        label="オートセーブ (Ctrl-e)", command=lambda: author.toggle_as_flag()
    )
    filemenu.add_command(label="終了", command=lambda: author.exit_as_save())
    menubar.add_cascade(label="ファイル", menu=filemenu)

    # 編集メニュー、カット、コピー、ペーストをラムダ式で呼び出し
    editmenu = tk.Menu(menubar, tearoff=0)
    editmenu.add_command(label="コピー (Ctrl-c)", command=lambda: author.text_copy())
    editmenu.add_command(label="カット (Ctrl-x)", command=lambda: author.text_cut())
    editmenu.add_command(label="貼り付け (Ctrl-v)", command=lambda: author.text_paste())
    menubar.add_cascade(label="編集", menu=editmenu)

    # メニューバー作成
    # 集中モード
    c_mode = tk.Menu(menubar, tearoff=0)
    c_mode.add_command(
        label="スタート", command=lambda: independent_method.start_c_mode(root)
    )
    c_mode.add_command(label="終了", command=lambda: independent_method.end_c_mode(root))
    menubar.add_cascade(label="集中モード", menu=c_mode)
    # ColorMode Change
    color_mode = tk.Menu(menubar, tearoff=False)
    color_select = tk.Menu(color_mode, tearoff=False)
    color_select.add_command(
        label="normal", command=lambda: author.change_theme(True, "normal")
    )
    color_select.add_command(
        label="dark", command=lambda: author.change_theme(True, "dark")
    )
    color_select.add_command(
        label="paper", command=lambda: author.change_theme(True, "paper")
    )
    color_select.add_command(
        label="terminal", command=lambda: author.change_theme(True, "terminal")
    )
    color_mode.add_cascade(label="テーマ切り替え", menu=color_select)
    menubar.add_cascade(label="テーマ", menu=color_mode)
    # オートインデント/オン・オフ
    auto_indent = tk.Menu(menubar, tearoff=0)
    auto_indent.add_command(
        label="オン/オフ (Ctrl-q)", command=lambda: author.toggle_auto_indent()
    )
    menubar.add_cascade(label="オートインデント", menu=auto_indent)
    #ヘルプメニューの表示
    Help_Menu = tk.Menu(menubar, tearoff=0)
    Help_Menu.add_command(
        label="LICENSE", command=lambda: author.show_license()
    )
    # バージョン情報
    Help_Menu.add_command(label="VERSION", command=lambda: view_version())
    menubar.add_cascade(label="HELP", menu=Help_Menu)

    # タイトル
    root.config(menu=menubar)
    root.title("I Want Be...")
    root.configure(background="gray")
    # テキストエリア作成
    # フォントは游ゴシックを想定
    #ysc = tk.Text(page)
    # page = tk.Text(root, undo=False, wrap=tkinter.NONE)
    # pkvin = vinegar.Vinegar(page)
    page.configure(bg="ghost white", fg="black")
    defont = tkfont.Font(family="Yu Gothic", size=14)
    # スクロールバー

    xscrollbar = tkinter.Scrollbar(root, orient=tkinter.HORIZONTAL, command=page.xview)
    yscrollbar = tkinter.Scrollbar(root,orient=tkinter.VERTICAL, command=page.yview)
    xscrollbar.pack(side=tkinter.BOTTOM)
    yscrollbar.pack(side=tkinter.RIGHT)
    page.pack(fill="both", expand=True)
    yscrollbar.pack(side=tk.RIGHT, fill="y", )
    xscrollbar.pack(side=tk.BOTTOM, fill="x")
    # xsc = tk.Text(root)
    #psbar = tk.Scrollbar(root)?
    page["yscrollcommand"] = yscrollbar.set
    page["xscrollcommand"] = xscrollbar.set

    #テーマ初期化
    theme_init()

    # ファイルを保存
    page.bind("<Control-s>", lambda self: author.save_file("file"))
    # コピペ＆カット
    page.bind("<Control-c>", lambda self: author.text_copy())
    # page.bind('<Control-v>', lambda self: author.txtpst())
    page.bind("<Control-x>", lambda self: author.text_cut())
    # 三点リーダー二つ組挿入
    page.bind("<Control-t>", lambda self: independent_method.three_point(page))
    # ダッシュの挿入
    page.bind("<Control-d>", lambda self: independent_method.double_dash(page))
    # ルビを振る
    page.bind("<Control-r>", lambda self: author.ruby())
    # 傍点をつける
    page.bind("<Control-b>", lambda self: independent_method.dot_mark(page))
    # オートインデント
    # 半角全角切り替え
    page.bind("<Control-w>", lambda self: author.toggle_half_or_full())
    # オートインデントのオン・オフ
    page.bind("<Control-q>", lambda self: author.toggle_auto_indent())
    # オートセーブ
    page.bind("<Control-e>", lambda self: author.toggle_as_flag())
    # エンターが押された場合、IMEの変換で押したものか改行をしたのかを判断してオートインデントを行う
    page.bind("<KeyPress-Return>", lambda self: author.ime_check())
    page.bind(
        "<KeyRelease-Return>",
        lambda self: author.insert_space()
        if author.hit_return and author.auto_indent
        else ignore(),
    )
    # 文字カウント
    page.bind("<Any-KeyPress>", author.logger)

    root.protocol("WM_DELETE_WINDOW", author.exit_as_save)

    # color.binの読み込み
    try:
        with open("color.bin", "r") as theme_file:
            theme = theme_file.read()
    # ファイルが見つからない場合通常テーマで開く
    except FileNotFoundError:
        theme: str = "normal"
    # 潰せない例外の場合終了
    except Exception as e:
        tk.messagebox.showinfo("ERROR!", "致命的なエラーが発生しました:" + str(e))
        sys.exit()
    author.change_theme(True, theme)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    # オートセーブその他の再帰呼び出し
    root.after(1000, author.is_auto_save_enable)
    root.mainloop()
