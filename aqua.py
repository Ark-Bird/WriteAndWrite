#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 20:47:33 2017
@author: hiro
"""

"""
Copyright 2020 hiro

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pyperclip
import sys
import platform


class NotOpenPathException(Exception):
    """
    ファイルを開くのに失敗した時の例外
    基本的に握りつぶしてデフォルトを適用して続行する目的
    """
    pass


class UnrecoveredError(Exception):
    """
    復旧不能なエラーの発生時に投げる
    """
    pass

class WillBeAuthor:
    """
    mod string class
    """
    clip = {}
    doing = []
    path = ''
    ftext = ''
    is_save = True

    def __init__(self):
        """
        変数初期化
        """
        self.len = 0
        self.file = ""
        self.is_changed = False
        self.cliptext = ""
        self.pstxt = ""
        self.auto_indent = False
        self.half_space = False
        self.hit_return = False
        self.is_save = True
        self.is_exit = False
        self.ASFLAG = False
        self.dark_mode = False
        self.col = ""
        self.nowcolor = "normal"
        self.textc = ""
        try:
            with open('color.bin', mode='r', encoding='utf-8') as f:
                self.col = f.read()
        except FileNotFoundError:
            pass
        if self.col == "dark":
            self.dark_mode = True

    def ignore(self):
        """
        何もしない
        例外を握りつぶす時等に使用
        passではなく明示的に握りつぶす
        """
        pass

    def logger(self, event):
        """
        テキストの変更を検知してフラグを立てる
        Ctrlとの組み合わせに対応
        基本的に何かのキーが押された時に呼ばれる
        """
        self.counter()
        self.is_save = False
        self.is_changed = True


    def counter(self):
        """
        文字カウント
        loggerから呼ばれる
        カウントした文字はタイトルバーに表示
        """
        s = page.get('0.0', 'end')
        self.len = len(s)
        # messagebox.showinfo('文字数(改行、スペース込み)', self.leng)
        #vt = " a \t b\r\n\tc\t\n"
        vt = ''.join(s.split())
        vanillal = len(vt)
        self.textc = str(vanillal) + ':  文字'

        if not self.is_save:
            self.textc += "*未保存*:"
        self.textc = "I want Be... :" + self.textc
        if self.auto_indent:
            if self.half_space:
                self.textc += "*AI半角"
            else:
                self.textc += "*AI全角"
        if self.ASFLAG:
            self.textc += ":auto_save_enable:"
        else:
            self.textc += ":auto_save_disable:"

        root.title(self.textc)
        return self.textc

    def autosave(self):
        """
        オートセーブ
        """
        if self.file == '':
            pass
        if self.ASFLAG:
            self.save_file('file')
            self.autosaveflag()

    def autosaveflag(self):
        """
        オートセーブフラグが有効ならオートセーブを毎秒呼び出し
        フラグが立っていない場合無視
        :return:無し
        """
        if self.ASFLAG:
            self.autosave()
            root.after(1000, self.autosaveflag)
        else:
            root.after(1000, self.autosaveflag)
        self.change_theme()
        return

    def toggle_as_flag(self):
        """
        オートセーブフラグのトグル
        self.ASFLAG:オートセーブのフラグ
        :return:無し
        """
        if self.ASFLAG:
            self.ASFLAG = False
        else:
            self.ASFLAG = True
            self.autosaveflag()

    def saveas(self, types):
        """
        clear file name
        名前をつけて保存
        返り値なし
        """
        if types == 'file':
            self.file = ''
        self.save_file(types)
        self.is_save = True

    def save_file(self, types):
        """
        SAVE file with dialog
        ファイルの保存処理
        path.binを開いて前回のファイル保存先を開く
        存在しなければNotOpenPathException例外を投げる
        失敗時Falseをリターン
        """
        #前回の保存場所を参照
        try:
            if not os.path.exists("path.bin"):
                raise NotOpenPathException
            with open("path.bin", mode='r', encoding="utf-8") as f:
                iDir = os.path.abspath(os.path.dirname(f.readline()))
        except NotOpenPathException:
            iDir = os.path.abspath(os.path.dirname(__file__))
        if types == '':
            return
        if self.file == '':
            self.file = tk.filedialog.asksaveasfilename(filetypes=[("txt files", "*.txt")], initialdir=iDir)
        if self.file == '':
            self.ASFLAG = False
            return
        if not self.file:
            self.file = ''
            return
        if types == 'file':
            self.ftext = page.get('0.0', 'end')
            self.ftext = self.ftext[0:-1]
        if self.file[-4:] != ".txt":
            self.file += ".txt"
        with open(self.file, mode='w', encoding='utf-8') as f:
            f.write(self.ftext)
        with open("./path.bin", mode='w', encoding='utf-8') as f:
            f.write(self.file)
            # if types == 'file':
            #     self.file = self.file
        self.is_changed = False
        self.is_save = True
        self.counter()

    def exit_as_save(self):
        """
        終了時の保存処理
        保存されていなければ確認ダイアログを表示
        :return:終了時ウインドウの破棄、キャンセル時、空のリターン
        """
        if not self.is_save:
            save_exit = messagebox.askyesno("ファイルが変更されています", "ファイルを保存しますか？")
            if save_exit:
                self.saveas("file")
            if messagebox.askyesno("終了しますか？", "終了しますか？"):
                self.is_exit = True
        if self.is_exit or self.is_save:
            root.destroy()
        else:
            return

    def new_blank_file(self, types):
        """
        clear text field
        テキストをクリアして新しいファイルにする
        変更フラグを降ろす
        保存フラグを立てる
        """
        self.ftext = page.get('0.0', 'end')
        if self.ftext != "\n" or self.is_save:
            if messagebox.askyesno("保存しますか?", "ファイルが変更されています、保存しますか?"):
                self.saveas("file")
            if not messagebox.askyesno("破棄しますか？", "文書を破棄しますか？"):
                return
        if types == 'file':
            page.delete('0.0', 'end')
            self.file = ''
        self.is_changed = False
        self.file = ""
        self.is_save = True

    def fpopen(self, types):
        """
        FILE OPEN dialog
        ファイルを開く
        変更されていたらチェック
        存在しないディレクとをを指定していたらスクリプトのディレクトリを開く
        """
        if page.get('0.0', 'end') != '\n' and self.is_changed:
            if not messagebox.askyesno("注意", "ファイルが変更されています、破棄しますか？"):
                return
        fTyp = [("", "*")]
        try:
            if not os.path.exists("path.bin"):
                raise NotOpenPathException
            with open("path.bin", mode='r', encoding="utf-8") as f:
                iDir = f.readline()
        except NotOpenPathException:
            iDir = os.path.abspath(os.path.dirname(__file__))
        self.file = tk.filedialog.askopenfilename(initialdir=iDir)
        if self.file == '':
            return
        with open(self.file, encoding="utf-8_sig") as f:
            readed = f.read()
        page.delete('0.0', 'end')
        page.insert('0.0', readed)
        self.t_change()

    def txtcpy(self):
        """
        copy text
        テキストの範囲が選択されていなかった場合例外を投げ、握りつぶす
        """
        try:
            #選択範囲をクリップボードにコピー
            self.cliptext = page.get(tk.SEL_FIRST, tk.SEL_LAST)
            pyperclip.copy(self.cliptext)
        except tk.TclError:
            #問題の無い例外は握りつぶす
            pass
        except Exception:
            raise UnrecoveredError


    def txtpst(self):
        """
        paste text
        範囲を選択していなかった場合の例外は握りつぶす
        tk.TclError以外のエラーが出ると落ちる
        返り値無し
        """
        try:
            #pyperclip.pasteを使うと文字化けする
            #self.pstxt = pyperclip.paste()
            self.pstxt = self.cliptext
            page.insert('insert', self.pstxt)
        #選択範囲がない場合例外が投げられる
        except tk.TclError:
            pass
        except Exception:
            raise UnrecoveredError

    def txtcut(self):
        """
        cut text
        返り値無し
        """
        try:
            self.cliptext = page.get(tk.SEL_FIRST, tk.SEL_LAST)
            pyperclip.copy(self.cliptext)
            page.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            #選択範囲がない場合例を投げられるので握りつぶす
            pass


    def start_cmode(self):
        """
        START AUTHOR MODE
        集中モード開始（フルスクリーンになる）
        返り値無し
        """
        root.attributes("-fullscreen", True)
        return

    def end_cmode(self):
        """
        END AUTHOR MODE
        集中モード終了（フルスクリーンは解除されるがウィンドウからフォーカスが外れない場合があるので注意
        返り値無し
        """
        root.attributes("-fullscreen", False)
        root.geometry("640x640")
        return

    def ruby(self):
        """
        テキストを選択してルビを振る
        選択範囲が十文字より多ければ警告を表示
        ルビの書式は小説家になろう及びカクヨム、及びその互換書式に対応しています
        返り値無し
        """
        b = tk.SEL_FIRST
        i = tk.SEL_FIRST
        try:
            tmpstr = page.get('sel.first', 'sel.last')
            if len(tmpstr) > 10:
                messagebox.showinfo('over', '10文字以上にルビは非対応の可能性があります')
            tmpstr = "|" + tmpstr + "《》"

            page.delete('sel.first', 'sel.last')
            page.insert('insert', tmpstr)
            page.mark_set('insert', 'insert-1c')
        except tk.TclError:
            pass
        except Exception:
            raise UnrecoveredError
        return

    def threepoint(self):
        """
        三点リーダの挿入
        全角で二つ一組で挿入
        """
        page.insert('insert', "……")
        pass

    def threedash(self):
        """
        ダッシュの挿入
        全角で二つ一組で挿入
        """
        page.insert('insert', "――")

    def t_change(self):
        """
        テキストの変更フラグを立てる
        :return:無し
        """
        self.is_changed = True

    def toggle_auto_indent(self):
        """
        オートインデント機能のオン・オフ
        返り値は無し
        挿入されるインデントは全角・半角はtoggle_half_or_full関数でトグルする
        デフォルトは全角スペース
        """
        self.auto_indent = not self.auto_indent
        self.counter()

    def toggle_half_or_full(self):
        """
        オートインデントの半角全角切り替え
        """
        if self.half_space:
            self.half_space = False
        else:
            self.half_space = True

    def insert_space(self):
        """
        オートインデント
        self.half_spaceがTrueのとき半角スペース、Falseの時全角スペースのインデントを挿入
        """
        if self.hit_return:
            index = tk.INSERT
            if self.half_space:
                page.insert(index, ' ')
            else:
                page.insert(index, '　')
            self.hit_return = False

    def ime_check(self):
        """
        IMEのリターンか、改行かの判断
        改行ならばインスタンス変数のhit_returnを立てる
        返り値無し
        """
        self.hit_return = True

    def toggle_dark_mode(self):
        """
        ダークモードと通常モードのトグル
        """
        if self.dark_mode:
            self.dark_mode = False
        else:
            self.dark_mode = True

    def change_theme(self):
        """
        テーマの変更
        モード名をcolor.binに書き込む
        該当ファイルはプレーンテキストでありマニュアルでの編集が可能
        color.binの内容がdarkだとダークモード、存在しない、もしくはそれ以外の場合通常モード
        ストレージへの負荷軽減のためモード変更のない場合ファイルへ書き込まずリターン
        """
        #テーマが変更されていなければ即リターン
        if not self.is_modify():
            return

        if self.dark_mode:
            with open('color.bin', mode='w', encoding='utf-8') as f:
                f.write("dark")
            page.configure(bg='gray16', fg='azure')
        else:
            with open('color.bin', mode='w', encoding='utf-8') as f:
                f.write("normal")
            page.configure(bg='ghost white', fg='black')

    def is_modify(self):
        """
        color.binを読み込み現在のモードと同じならFalseを返す
        変更されている場合はTrueを返す
        ファイルが見つからなかった場合はnormalで開く、それ以外の例外なら終了
        """
        try:
            with open('color.bin', mode='r', encoding='utf-8') as f:
                mode = f.read()
                if self.dark_mode and mode != "dark":
                    if mode == "dark":
                        return False
                else:
                    if mode == "normal":
                        return False
        #ファイルが何らかの理由で存在しない場合normalを書き込んで作成
        except FileNotFoundError:
            with open('color.bin', mode='w', encoding='utf-8') as f:
                f.write("normal")
            return True
        except Exception:
            raise UnrecoveredError
        return True



def res_path(rel):
    """
    Windowsの場合、アイコンへのパスを返す
    他のOSの場合は呼ばれることはない
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel)
    return os.path.join(os.path.abspath("."), rel)


if __name__ == '__main__':
    textcount = 0
    #Windowsもしくはそれ以外を判別
    pf = platform.system()
    #明示的に使わない変数としてdummyを使う
    dummy = []
    author = WillBeAuthor()
    mainstory = 'file'
    root = tk.Tk()
    root.geometry("640x640")
    #動いているOSの判別
    if pf == 'Windows':
        icon = res_path('./res/wbe.ico')
        root.iconbitmap(icon)
    else:
        root.wm_iconbitmap('@./res/wbe.xbm')
    root.minsize(32, 32)
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    #ファイルメニュー、渡している'file'引数はダミー
    filemenu.add_command(label='New', command=lambda: author.new_blank_file('file'))
    filemenu.add_command(label='Open', command=lambda: author.fpopen('file'))
    filemenu.add_command(label='Save', command=lambda: author.save_file('file'))
    filemenu.add_command(label='Save As', command=lambda: author.saveas('file'))
    filemenu.add_command(label='Auto Save', command=lambda: author.toggle_as_flag())
    menubar.add_cascade(label='File', menu=filemenu)

    #編集メニュー、カット、コピー、ペーストをラムダ式で呼び出し
    editmenu = tk.Menu(menubar, tearoff=0)
    editmenu.add_command(label='Copy', command=lambda: author.txtcpy())
    editmenu.add_command(label='Cut', command=lambda: author.txtcut())
    editmenu.add_command(label='Paste', command=lambda: author.txtpst())
    menubar.add_cascade(label='Edit', menu=editmenu)
    pclipmenu = tk.Menu(menubar, tearoff=0)

    # メニューバー作成
    #集中モード
    c_mode = tk.Menu(menubar, tearoff=0)
    c_mode.add_command(label="START", command=lambda: author.start_cmode())
    c_mode.add_command(label="END", command=lambda: author.end_cmode())
    menubar.add_cascade(label='C-MODE', menu=c_mode)
    #ColorMode Change
    color_mode = tk.Menu(menubar, tearoff=0)
    color_mode.add_command(label="Color Change!", command=lambda: author.toggle_dark_mode())
    menubar.add_cascade(label="Color Change!", menu=color_mode)
    #オートインデント/オン・オフ
    auto_indent = tk.Menu(menubar, tearoff=0)
    auto_indent.add_command(label="Toggle(Ctrl-Q)", command=lambda: author.toggle_auto_indent())
    menubar.add_cascade(label="Auto_Indent", menu=auto_indent)
    #タイトル
    root.config(menu=menubar)
    root.title('I Want Be...')
    root.configure(background="gray")
    #スクロールバー
    yScrollbar = tk.Scrollbar(root)
    yScrollbar.pack(side=tk.RIGHT, fill="y")
    xScrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
    xScrollbar.pack(side=tk.BOTTOM, fill='x')
    psbar = tk.Scrollbar(root)
    # テキストエリア作成
    page = tk.Text(root, undo=True, wrap=tk.NONE)
    # カラーコンフィグ
    page.configure(bg='ghost white', fg='black')

    # スクロールバー追加
    page.config(
        xscrollcommand=xScrollbar.set,
        yscrollcommand=yScrollbar.set)
    page.pack(fill='both', side=tk.LEFT, expand=True)
    # ファイルを保存
    page.bind('<Control-s>', lambda self: author.save_file('file'))
    #コピペ＆カット
    page.bind('<Control-c>', lambda self: author.txtcpy())
    page.bind('<Control-v>', lambda self: author.txtpst())
    page.bind('<Control-x>', lambda self: author.txtcut())
    #三点リーダー二つ組挿入
    page.bind('<Control-t>', lambda self: author.threepoint())
    #ダッシュの挿入
    page.bind('<Control-d>', lambda self: author.threedash())
    # ルビを振る
    page.bind('<Control-r>', lambda self: author.ruby())
    # オートインデント
    #　半角全角切り替え
    page.bind('<Control-w>', lambda self: author.toggle_half_or_full())
    #オートインデントのオン・オフ
    page.bind('<Control-q>', lambda self: author.toggle_auto_indent())
    #オートセーブ
    page.bind('<Control-e>', lambda self: author.toggle_as_flag())
    #エンターが押された場合、IMEの変換で押したものか改行をしたのかを判断してオートインデントを行う
    page.bind('<KeyPress-Return>', lambda self: author.ime_check())
    page.bind('<KeyRelease-Return>', lambda self: author.insert_space() if author.hit_return and author.auto_indent else author.ignore())
    # 文字カウント
    page.bind('<Any-KeyPress>', author.logger)

    root.protocol("WM_DELETE_WINDOW", author.exit_as_save)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    #オートセーブその他の再帰呼び出し
    root.after(1000, author.autosaveflag)
    root.mainloop()
