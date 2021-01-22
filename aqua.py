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
from tkinter import filedialog, ttk
from tkinter import messagebox
import pyperclip
import sys


class not_open_path_exception(Exception):
    pass


class WillBeAuthor:
    """
    mod string class
    """
    clip = {}
    #pclip = {}
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
        self.hit_return = False
        self.is_save = True
        self.is_exit = False

    def ignore(self):
        pass

    def logger(self, event):
        """
        テキストの変更を検知してフラグを立てる
        """

        self.counter()
        self.is_save = False
        self.is_changed = True


    def counter(self):
        """
        counting letter
        """
        s = page.get('0.0', 'end')
        self.len = len(s)
        # messagebox.showinfo('文字数(改行、スペース込み)', self.leng)
        vt = " a \t b\r\n\tc\t\n"
        vt = ''.join(s.split())
        vanillal = len(vt)
        #textc = str(self.len) + '文字|' + str(vanillal) + ':文字(空白抜き)'
        textc = str(vanillal) + ':文字'
        if not self.is_save:
            textc += "*未保存*"
        textc = "I want Be... :" + textc
        if self.auto_indent:
            textc += "*AI"

        root.title(textc)
        return textc

    def saveas(self, types):
        """
        clear file name
        名前をつけて保存
        """
        if types == 'file':
            self.file = ''
        self.save_file(types)
        self.is_save = True

    def save_file(self, types):
        """
        SAVE file with dialog
        ファイルの保存処理
        """
        if types == '':
            return
        fTyp = [("", "*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        if self.file == '':
            self.file = tk.filedialog.asksaveasfilename(filetypes=[("txt files", "*.txt")], initialdir=os.getcwd())
        # else:
        #     self.file = self.path
        if self.file == '':
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
        """
        if page.get('0.0', 'end') != '\n' and self.is_changed:
            if not messagebox.askyesno("注意", "ファイルが変更されています、破棄しますか？"):
                return
        fTyp = [("", "*")]
        try:
            if not os.path.exists("path.bin"):
                raise not_open_path_exception
            with open("path.bin", mode='r', encoding="utf-8") as f:
                iDir = f.readline()
        except not_open_path_exception:
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
        """
        try:
            if page.get(tk.SEL_FIRST) != tk.SEL_LAST:
                self.cliptext = page.get(tk.SEL_FIRST, tk.SEL_LAST)
                pyperclip.copy(self.cliptext)
        except Exception:
            pass

    def txtpst(self):
        """
        paste text
        """
        try:
            self.pstxt = pyperclip.paste()
            print(self.pstxt)
            page.insert('insert', self.pstxt)
        except Exception:
            pass

    def txtcut(self):
        """
        cut text
        """
        self.cliptext = page.get(tk.SEL_FIRST, tk.SEL_LAST)
        pyperclip.copy(self.cliptext)
        page.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def start_cmode(self):
        """
        START AUTHOR MODE
        集中モード開始（フルスクリーンになる）
        """
        root.attributes("-fullscreen", True)
        return

    def end_cmode(self):
        """
        END AUTHOR MODE
        集中モード終了（フルスクリーンは解除されるがウィンドウからフォーカスが外れない場合があるので注意
        """
        root.attributes("-fullscreen", False)
        root.geometry("640x640")
        return

    def ruby(self):
        """
        テキストを選択してルビを振る
        選択範囲が十文字より多ければ警告を表示
        """
        b = tk.SEL_FIRST
        i = tk.SEL_FIRST
        tmpstr = page.get('sel.first', 'sel.last')
        if len(tmpstr) > 10:
            messagebox.showinfo('over', '10文字以上にルビは非対応の可能性があります')
        tmpstr = "|" + tmpstr + "《》"

        page.delete('sel.first', 'sel.last')
        page.insert('insert', tmpstr)
        page.mark_set('insert', 'insert-1c')

    def threepoint(self):
        """
        三点リーダの挿入
        """
        page.insert('insert', "……")
        pass

    def threedash(self):
        """
        ダッシュの挿入
        """
        page.insert('insert', "――")

    def t_change(self):
        self.is_changed = True

    def toggle_auto_indent(self):
        """
        オートインデント機能のオン・オフ
        """
        self.auto_indent = not self.auto_indent
        self.counter()

    def insert_space(self):
        """
        オートインデント
        """
        if self.hit_return:
            index = tk.INSERT
            page.insert(index, '　')
            self.hit_return = False

    def ime_check(self):
        self.hit_return = True

def res_path(rel):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel)
    return os.path.join(os.path.abspath("."), rel)


if __name__ == '__main__':
    textcount = 0
    dummy = []
    author = WillBeAuthor()
    wba = author
    prt = 'prot'
    mainstory = 'file'
    root = tk.Tk()
    root.geometry("640x640")
    icon = res_path('./res/wbe.ico')
    root.iconbitmap(default=icon)
    root.minsize(32, 32)
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label='New', command=lambda: wba.new_blank_file('file'))
    filemenu.add_command(label='Open', command=lambda: wba.fpopen('file'))
    filemenu.add_command(label='Save', command=lambda: wba.save_file('file'))
    filemenu.add_command(label='Save As', command=lambda: wba.saveas('file'))
    menubar.add_cascade(label='File', menu=filemenu)

    editmenu = tk.Menu(menubar, tearoff=0)
    editmenu.add_command(label='Copy', command=lambda: wba.txtcpy())
    editmenu.add_command(label='Cut', command=lambda: wba.txtcut())
    editmenu.add_command(label='Paste', command=lambda: wba.txtpst())
    menubar.add_cascade(label='Edit', menu=editmenu)
    pclipmenu = tk.Menu(menubar, tearoff=0)

    # メニューバー作成
    #集中モード
    c_mode = tk.Menu(menubar, tearoff=0)
    c_mode.add_command(label="START", command=lambda: wba.start_cmode())
    c_mode.add_command(label="END", command=lambda: wba.end_cmode())
    menubar.add_cascade(label='C-MODE', menu=c_mode)
    #オートインデント/オン・オフ
    auto_indent = tk.Menu(menubar, tearoff=0)
    auto_indent.add_command(label="Toggle(Ctrl-Q)", command=lambda: wba.toggle_auto_indent())
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
    # psbar.pack(side=tk.LEFT, fill="y")
    # テキストエリア作成
    page = tk.Text(root, undo=True, wrap=tk.NONE)
    # カラーコンフィグ
    page.configure(bg='ghost white', fg='black')
    #page.configure(fg='black')
    #page.configure(insertbackground='white')
    # page.grid(column=0, row=0, sticky=tk.E + tk.N + tk.S + tk.W)

    # xScrollbar.grid(row=1, column=0, sticky=tk.EW)
    # スクロールバー追加
    page.config(
        xscrollcommand=xScrollbar.set,
        yscrollcommand=yScrollbar.set)
    page.pack(fill='both', side=tk.LEFT, expand=True)
    # ファイルを保存
    page.bind('<Control-s>', lambda self: wba.save_file('file'))
    #コピペ＆カット
    page.bind('<Control-c>', lambda self: wba.txtcpy())
    page.bind('<Control-v>', lambda self: wba.txtpst())
    page.bind('<Control-x>', lambda self: wba.txtcut())
    #三点リーダー二つ組挿入
    page.bind('<Control-t>', lambda self: wba.threepoint())
    #ダッシュの挿入
    page.bind('<Control-d>', lambda self: wba.threedash())
    # page.bind('<Control-n>', lambda self: mos.counter())
    # ルビを振る
    page.bind('<Control-r>', lambda self: wba.ruby())
    # オートインデント
    page.bind('<Control-q>', lambda self: wba.toggle_auto_indent())
    page.bind('<KeyPress-Return>', lambda self: wba.ime_check())
    page.bind('<KeyRelease-Return>', lambda self: wba.insert_space() if wba.hit_return and wba.auto_indent else wba.ignore())
    # 文字カウント
    page.bind('<Any-KeyRelease>', wba.logger)
    # page.bind('<Control-z>', lambda self: wba.undo())
    # 文字数カウンタ
    # count = tk.StringVar()
    #
    # status = tk.Label(page, textvariable=count, borderwidth=2, relief="groove")
    # status.pack(side=tk.BOTTOM, fill=tk.X)

    root.protocol("WM_DELETE_WINDOW", wba.exit_as_save)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.mainloop()
