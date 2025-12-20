#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 20:47:33 2017
@author: hiro
"""
import os
import platform
import queue
import sys
import threading
import time
import tkinter
import tkinter as tk
import tkinter.font
from queue import Queue
from tkinter import filedialog
from tkinter import messagebox
import re
from collections import deque

from wanabi.extend_exception import IgnorableException
from wanabi.log_recorder_me import record_hist
# import app_name
# import extend_exception
# import full_mode
# import indent_insert
# import independent_method
# import menu_init
# import string_decorate
# import textarea_config
# import theme_mod
# import vinegar
# from independent_method import ignore

from wanabi import app_name, encoding
from wanabi import extend_exception
from wanabi import full_mode
from wanabi import indent_insert
from wanabi import independent_method
from wanabi import menu_init
from wanabi import string_decorate
from wanabi import textarea_config
from wanabi import theme_mod
from wanabi import vinegar
from wanabi import lang
import wanabi.encoding
from wanabi.independent_method import ignore
from wanabi.vinegar import Vinegar

"""
Copyright 2020 hiro

     This file is part of wanabi.

    wanabi is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

    wanabi is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with wanabi. If not, see <https://www.gnu.org/licenses/>. 
"""


class WillBeAuthor:
    """
    The God class
    """

    def __init__(self):
        """
        変数初期化
        file_name:ファイル名
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
        self.codepoint: wanabi.encoding.Encoding = wanabi.encoding.Encoding()
        self.code = self.codepoint.code
        self.file_name: str = ""
        self.written_textum: str = ""
        self.is_changed: bool = False
        self.clipped_text: str = ""
        self.pasting_text: str = ""
        self.is_save: bool = True
        self.is_exit: bool = False
        self.is_init: bool = True
        self.is_autosave_flag: bool = False
        self.title_var_string: str = ""
        self.copied_text: str = ""
        self.page: tk.Text | None = None
        self.root: tk.Tk | None = None
        self.init: bool = True
        self.indent: indent_insert.Indent | None = None
        self.before_text: str = "\n"
        self.prev_save_dir: str = ""
        self.cursor_move_mode: str = "vi"
        self.is_wrap: bool = True
        self.debug_enable: bool = self.is_debug_enable()
        self.end_of_code: bool = False
        self.mess: None | tk.Label = None
        self.do_command: None | tk.StringVar = None
        self.do_command: None | tk.StringVar = None
        self.letter_count: int = 0
        self.count_thread: threading.Thread = threading.Thread(target=self.counter)
        self.com_hist: deque = deque()
        self.app_name: app_name.AppName = app_name.AppName()
        self.is_terminate: bool = False
        self.vi_mode_now: str = "Command_mode"
        self.is_thread_autosave_flag: bool = False
        self.is_already_run_autosave_flag: bool = False
        self.t: threading.Thread | None = None
        self.is_not_t_autosave_enable: bool = True
        self.t_end: bool = False
        self.save_flag_cvs: tk.Canvas | None = None
        self.temp_save_thread_flag:bool = False
        self.save_thread_done:bool = False
        self.is_end:bool = False
        self.letters: int = 0
        self.no_ask: bool = False
        self.que = Queue(maxsize=1)
        try:
            with open("conf/lang.txt", "r", encoding=self.code) as f:
                self.lang = f.read()
            if self.lang == "jp":
                self.language = lang.Language("jp")
            elif self.lang == "en":
                self.language = lang.Language("en")
            else:
                with open(f"conf/lang.txt", "r", encoding=self.code) as f:
                    f.write("en")
                    self.language = lang.Language("en")
        except FileNotFoundError:
            with open("conf/lang.txt", "w", encoding=self.code) as f:
                f.write("jp")
                self.language = lang.Language("jp")
        except:
            self.command_hist(self.language.fatalError_is_raise)
            raise Exception
        try:
            with open("conf/no_ask.txt", "r", encoding="utf-8") as f:
                no_ask = f.read()
                if no_ask == "True":
                    self.no_ask = True
                    messagebox.showinfo("新規ファイルの作成時に確認をしません", "新規ファイルを作成時に確認をせず旧ファイルを閉じます、\n"
                                                                                "内容は保存されません、注意してください")
                else:
                    self.no_ask = False
        except FileNotFoundError:
            with open("conf/no_ask.txt", "w", encoding="utf-8") as wf:
                wf.write("False")
        except:
            print("設定ファイルを作成出来ません")
            raise Exception
        if self.debug_enable:
            self.log2me = record_hist.RecordHist("conf/command.log")
        try:
            self.theme: str = self.read_theme()
        except FileNotFoundError:
            ignore()
        except Exception:
            raise extend_exception.FatalError

    def setroot(self, root) -> None:
        """
        rootウインドウの参照を受け取り、クラス内で扱えるようにする
        :return:None
        """
        self.root = root
        return

    def init_label(self, message: str) -> None:
        """
        ラベルの初期化
        :param message:
        :return:
        """
        self.do_command = tk.StringVar()
        self.do_command.set(message)
        self.mess = tk.Label(self.root, textvariable=self.do_command)
        self.mess.pack(side="bottom", fill='x')

    def is_saved_flag_color(self) -> None:
        """
        保存完了時に緑
        美穗存知に赤
        :return:
        """
        self.save_flag_cvs = tk.Canvas(self.root, height=5)
        self.save_flag_cvs.pack(side="bottom", fill="x")

    def save_cvs_color(self) -> None:
        """
        キャンバスの幅と高さを取得し、保存時緑、未保存時赤に塗り替え
        :return:
        """
        width : int = self.save_flag_cvs.winfo_width()
        height : int = self.save_flag_cvs.winfo_height()
        self.save_flag_cvs.delete("status")
        if self.is_save:
            self.save_flag_cvs.create_rectangle(0, 0, width, height, fill="green", tags="status")
        else:
            self.save_flag_cvs.create_rectangle(0, 0, width, height, fill="red", tags="status")

    def command_hist(self, command) -> None:
        """
        コマンドのログを表示
        :param command: 実行されたコマンド
        :return: None
        """
        self.com_hist.append(command)
        if len(self.com_hist) > 5:
            self.com_hist.popleft()
        com_log = "→".join(self.com_hist)
        self.do_command.set(com_log)
        if self.debug_enable:
            self.log2me.write_log(command)

    def read_theme(self) -> str:
        """
        テーマファイルを読み込み、テーマ名を返す
        ファイルが存在しなければnormalでcolor.binを作成
        :return: color.binに書かれたテーマ名
        """
        try:
            with open("conf/color.bin", "r", encoding=self.code) as f:
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
        :return:None
        """
        independent_method.write_theme_string(theme)
        theme_mod.change_theme(self.page, self.command_hist, theme=theme)
        return

    def theme_apply(self) -> None:
        """
        ユーザ定義テーマを適用する
        :return:None
        """
        theme_mod.change_theme(self.page, self.command_hist, theme="original")
        return

    def logger(self, event=None) -> None:
        """
        テキストの変更を検知して変更フラグを立てる
        終了時にセーブするか訊ねるようにする
        文字カウントの変更
        Ctrlとの組み合わせに対応
        基本的に何かのキーが押された時に呼ばれる
        :return:None
        """
        if event:
            ignore()
        self.change_titlebar()
        self.is_save = False
        self.is_text_changed()
        self.is_init = False
        return

    def letter_count_after(self):
        s = self.page.get("0.0", "end")
        s = re.sub('[ 　\n\r\t]|[|]|《.*》', '', s)
        self.letters = len(s)
        return self.letters

    def counter(self) -> None:
        """
        文字カウント
        テキストエリアから全文を読んで空白をトリムした長さを返す
        loggerから呼ばれる
        カウントした文字はタイトルバーに表示
        オートインデント有効の場合タイトルバーに表示
        自動セーブの有効無効をタイトルバーに表示
        :return:None
        """
        while not self.is_end:
            if self.is_terminate:
                break
            #s: str = self.page.get("0.0", "end")
            # s = re.sub('[ 　\n\r\t]|[|]|《.*》', '', s)
            # text_length_without_whitespace: int = len(s)
            # self.letter_count = text_length_without_whitespace
            time.sleep(1)

    def count_only_letters(self, event=None) -> None:
        """
        文字数のみのカウント
        :return:
        """
        if event:
            ignore()
        text = self.page.get("0.0", "end")
        text = re.sub('[ 　\t\r\n「」,.、。]', '', text)
        messagebox.showinfo("現在の文字数", f"{len(text)}")

    def erase_newline(self) -> None:
        """
        連続した空行を削除する
        :return: None
        """
        if messagebox.askyesno("空行を削除しますか？", "テキストの空行を削除しますか？"):
            s: str = self.page.get("0.0", "end")
            s = re.sub('[\n]+', '\n', s)
            self.page.delete("0.0", "end")
            self.page.insert("0.0", s)
        return

    def insert_newline(self) -> None:
        """
        空行を1行空きに変更
        :return: None
        """
        if messagebox.askyesno("改行を1行おきを変更しますか？", "テキストの単一改行を1行空きに変更しますか？"):
            s: str = self.page.get("0.0", "end")
            s = re.sub('[\n]+', '\n\n', s)
            self.page.delete("0.0", "end")
            self.page.insert("0.0", s)
            self.page.delete("end-2c", "end")
        return

    def check_if_is_saved(self) -> None:
        """
        テキストが初期状態、もしくは未保存か保存済みかを書き換えるメソッド
        :return: None
        """
        if self.file_name == "" and self.page.get("0.0", "end") == "\n":
            self.title_var_string += ":" + self.language.title + ":"
        # 保存の有無
        elif not self.is_save:
            self.title_var_string += "*" + self.language.no_saved + "*:"
        elif self.is_save and not self.init:
            self.title_var_string += ":"+ self.language.saved +":"
        else:
            self.init = False

    def cursor_move_vi_or_emacs(self) -> str | None:
        """
        現在のカーソル移動モードを文字列で返す
        :return: 現在の移動モードの文字列
        """
        # カーソル移動の方法
        if self.cursor_move_mode == "vi":
            return "Vi mode:"
        elif self.cursor_move_mode == "emacs":
            return "Emacs mode:"
        return None

    def check_autosave_flag(self) -> str:
        """
        オートセーブの有効かどうかを文字列で返す
        :return: オートセーブの状態
        """
        if self.is_autosave_flag:
            return ":" + self.language.auto_save_enabled
        else:
            return ":" + self.language.auto_save_disabled

    def change_titlebar(self) -> None:
        """
        タイトルバーの文字列を変更
        :return:None
        """
        # auto_indentはオートインデントが有効かどうかのフラグ
        # half_spaceは挿入されるインデントが半角が全角かのフラグ
        auto_indent: bool = self.indent.auto_indent_enable()
        half_space: bool = self.indent.half_space_checker()
        # self.title_var_string = str(self.letter_count) + ":" + self.language.char
        self.title_var_string = str(self.letters) + ":" + self.language.char
        self.check_if_is_saved()
        self.title_var_string = self.app_name.return_app_name_for_now() + self.title_var_string
        # オートインデントの半角/全角状態の表示
        if auto_indent:
            if half_space:
                self.title_var_string += self.language.auto_indent_half_width
            else:
                self.title_var_string += self.language.auto_indent_full_width
        else:
            self.title_var_string += self.language.auto_indent_disable_now
        # オートセーブは有効か
        self.title_var_string += self.check_autosave_flag()
        # カーソル移動の方法
        self.title_var_string += self.cursor_move_vi_or_emacs()
        self.title_var_string += ":" + self.vi_mode_now
        self.title_var_string += independent_method.path_to_filename(self.file_name)
        self.root.title(self.title_var_string)
        return

    def repeat_save_file(self, _) -> None:
        """
        オートセーブ
        ファイルパスはユニコードであること
        :return:None
        """
        if self.que.empty():
            try:
                self.que.put(self.page.get("0.0", "end-1c"), block=False)
            except queue.Full:
                pass
        if self.prev_save_dir == "" and self.is_autosave_flag:
            self.prev_save_dir = filedialog.asksaveasfilename(filetypes=[("txt files", "*.txt")],
                                                              initialdir=self.prev_save_dir)
            independent_method.write_filename_string(self.prev_save_dir)
        try:
            with open("conf/path.bin", "r", encoding=self.code) as text_filename:
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
        except extend_exception.PathPermissionException:
            self.command_hist(self.language.pathfile_permission_error)
        except Exception:
            self.prev_save_dir = ""
            independent_method.write_filename_string("")
            raise extend_exception.CannotWriteFileException
        if self.prev_save_dir == "/":
            print("assert!")
            independent_method.write_filename_string(self.prev_save_dir)
        try:
            independent_method.write_filename_string(self.prev_save_dir)
        except FileNotFoundError:
            independent_method.write_filename_string("")
        except extend_exception.PathPermissionException:
            self.command_hist(self.language.pathfile_permission_error)
        except Exception:
            raise extend_exception.FatalError
        self.change_titlebar()
        if self.is_autosave_flag:
            self.save_file()
            self.is_save = True
            self.before_text = self.page.get("0.0", "end")
        try:
            self.root.after(1000, self.repeat_save_file, "dummy")
        except Exception:
            self.command_hist(self.language.cannot_write_file)
            self.root.after(1000, self.repeat_save_file, "dummy")
            raise extend_exception.CannotWriteFileException
        self.save_cvs_color()
        self.letter_count_after()
        return

    def toggle_autosave_flag(self, event=None) -> None:
        """
        オートセーブフラグのトグル
        self.is_autosave_flag:オートセーブのフラグ
        :return:None
        """
        if event:
            ignore()
        if self.is_autosave_flag:
            self.change_auto_save_disable()
        else:
            self.file_name = ""
            self.change_auto_save_enable()
        self.change_titlebar()
        return

    def change_auto_save_enable(self) -> None:
        """
        オートセーフのフラグを有効にする
        :return:None
        """
        self.is_autosave_flag = True
        self.command_hist(self.language.auto_save_enabled)
        return

    def change_auto_save_disable(self) -> None:
        """
        オートセーブ機能の無効化
        :return:None
        """
        self.command_hist(self.language.auto_save_disabled)
        self.is_autosave_flag = False
        return

    def save_as(self) -> None:
        """
        clear file name
        名前をつけて保存
        :return:None
        """
        self.file_name = ""
        self.save_file()
        return

    def save_file(self, event=None) -> None:
        """
        SAVE file with dialog
        ファイルの保存処理
        path.binを開いて前回のファイル保存先を開く
        存在しなければNotOpenPathException例外を投げる
        失敗時Falseをリターン
        """
        if event:
            ignore()
        if self.end_of_code:
            independent_method.fix_this_later()
            sys.exit()
        # 前回の保存場所を参照
        try:
            if not os.path.exists("conf/path.bin"):
                raise extend_exception.NotOpenPathException
            with open("conf/path.bin", mode="r", encoding=self.code) as f:
                prev_save_directory: str = os.path.abspath(os.path.dirname(f.readline()))
        except extend_exception.NotOpenPathException:
            prev_save_directory = os.path.abspath(os.path.dirname(__file__))
        if self.file_name == "":
            self.file_name = tk.filedialog.asksaveasfilename(
                filetypes=[("txt files", "*.txt")], initialdir=prev_save_directory
            )
        if self.file_name == "":
            self.change_auto_save_disable()
            return
        if not self.file_name:
            self.file_name = ""
            return
        if True:
            self.written_textum = self.page.get("0.0", "end")
            # 末尾の改行を削除する
            self.written_textum = self.written_textum[0:-1]
            if self.que.empty():
                try:
                    self.que.put(self.written_textum, block=False)
                except queue.Full:
                    pass
        if self.file_name[-4:] != ".txt":
            self.file_name += ".txt"
        if self.before_text == self.page.get("0.0", "end"):
            return
        with open(self.file_name, mode="w", encoding=self.code) as textum_file:
            try:
                textum_file.write(self.page.get("0.0", "end-1c"))
            except queue.Empty:
                pass
        if not self.is_autosave_flag:
            self.command_hist(self.file_name + self.language.save_complete)
        try:
            with open("conf/path.bin", mode="w", encoding=self.code) as conf:
                conf.write(self.file_name)
        except PermissionError:
            self.command_hist(self.language.pathfile_permission_error)
            time.sleep(0.05)
            self.save_file()
        self.is_text_unchanged()
        self.is_save = True
        self.save_cvs_color()
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
            self.is_terminate = True
            self.count_thread.join()
            self.end_of_code = True
            self.is_thread_autosave_flag = False
        else:
            return
        if self.is_not_t_autosave_enable:
            self.autosave_thread_end()
        try:
            with open("conf/temp.txt", "w", encoding=self.code) as temp_file:
                temp_file.write(s)
        except:
            raise extend_exception.IgnorableException
        self.is_end = True
        self.count_thread.join()
        self.root.destroy()
        sys.exit(0)

    def new_blank_file(self, event=None, no_ask=False) -> None:
        """
        clear text field
        テキストをクリアして新しいファイルにする
        変更フラグを降ろす
        保存フラグを立てる
        :return:None
        """
        self.written_textum = self.page.get("0.0", "end")
        self.prev_save_dir = ""
        if not self.no_ask:
            if not self.is_save:
                if messagebox.askyesno("保存しますか?", "ファイルが変更されています、保存しますか?"):
                    self.save_as()
                if not messagebox.askyesno("破棄しますか？", "文書を破棄しますか？"):
                    return
        self.page.delete("0.0", "end")
        self.is_text_unchanged()
        self.file_name = ""
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
        :return:None
        """
        if self.page.get("0.0", "end") != "\n" and self.is_changed:
            if not messagebox.askyesno("注意", "ファイルが変更されています、破棄しますか？"):
                return
        # path.binは前回保存したディレクトリが書き込まれている
        try:
            if not os.path.exists("conf/path.bin"):
                raise extend_exception.NotOpenPathException
            with open("conf/path.bin", mode="r", encoding=self.code) as f:
                directory_before_saved = f.readline()
        except extend_exception.NotOpenPathException:
            directory_before_saved = os.path.abspath(os.path.dirname(__file__))
        self.file_name = tk.filedialog.askopenfilename(initialdir=directory_before_saved)
        if self.file_name == "":
            return
        self.prev_save_dir = self.file_name
        try:
            with open(self.file_name, encoding="utf-8_sig") as f:
                loaded = f.read()
        except UnicodeDecodeError:
            messagebox.showerror("文字コードエラー", "ファイルがUTF-8ではありません")
            return
        self.page.delete("0.0", "end")
        self.page.insert("0.0", loaded)
        self.is_text_changed()
        self.change_auto_save_disable()
        self.change_titlebar()
        self.command_hist(self.file_name + self.language.opened)
        return

    def open_file(self, file_name) -> None:
        with open(file_name, "r") as f:
            txt = f.read()
            self.page.insert("0.0",txt)
        return

    def text_copy(self, event=None) -> None:
        """
        copy text
        テキストの範囲が選択されていなかった場合例外を投げ、握りつぶす
        :return:None
        """
        if event:
            ignore()
        try:
            # 選択範囲をクリップボードにコピー
            self.clipped_text = self.page.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            # 問題の無い例外は握りつぶす
            ignore()
            return
        except Exception:
            # どうしようもない例外でエラーをレイズ
            raise extend_exception.FatalError
        self.command_hist(self.language.app_clipboard_copy)
        return

    def text_paste(self, event=None) -> None:
        """
        paste text
        範囲を選択していなかった場合の例外は握りつぶす
        tk.TclError以外のエラーが出ると落ちる
        :return:None
        """
        if event:
            ignore()
        if self.clipped_text == "":
            return
        try:
            self.page.insert("insert", self.clipped_text)
        # 選択範囲がない場合例外が投げられる
        except tk.TclError:
            # 問題の無いエラー（握りつぶす）
            ignore()
            return
        except Exception:
            # 致命的なエラー
            raise extend_exception.FatalError
        self.command_hist(self.language.app_clipboard_copy)
        return

    def text_cut(self, event=None) -> None:
        """
        cut text
        返り値無し
        TclError以外の例外が投げられると落ちる
        :return:None
        """
        if event:
            ignore()
        try:
            # ローカル変数とクリップボードにコピー
            self.clipped_text = self.page.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.page.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            # 選択範囲がない場合例を投げられるので握りつぶす
            ignore()
            return
        except Exception:
            print("致命的なエラー")
            raise extend_exception.FatalError
        self.command_hist(self.language.app_clipboard_copy)
        return

    def is_text_changed(self) -> None:
        """
        テキストの変更フラグを立てる
        テキストエリアでキーが押されると呼ばれる
        :return:None
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
        """
        :param event:ダミー
        :return: 文字列breakこのイベントでキーバインドを上書き
        """
        if event:
            ignore()
        if self.file_name == "":
            messagebox.showinfo("Not open", "現在ファイルを開いていません")
            return "break"
        messagebox.showinfo("現在のファイル", self.file_name)
        return "break"

    def auto_indent(self) -> None:
        """
        conf/auto_indent.txtの中がTrueのときオートインデントを有効化
        :return: None
        """
        try:
            with open("conf/auto_indent.txt", "r")as ifp:
                indent = ifp.read()
                if indent == "True":
                    self.indent.auto_indent = True
                    self.page.insert('insert', '　')
                else:
                    pass
        except FileNotFoundError:
            independent_method.conf_dir_make()
            with open("conf/auto_indent.txt", "w+")as wfp:
                wfp.write("False")
        except Exception:
            raise extend_exception.FatalError
        self.command_hist(self.language.init_auto_indent)

    def wrap_enable(self) -> None:
        """
        テキストエリアの端で自動で折り返すように設定する
        起動時はこちらのオプションになっている
        :return:None
        """
        self.page.configure(wrap='char')
        return

    def wrap_disable(self) -> None:
        """
        テキストエリアの折り返しを無効化する
        :return:None
        """
        self.page.configure(wrap='none')
        return

    def enable_topmost_window(self) -> None:
        self.root.attributes("-topmost", True)
        self.command_hist(self.language.window_topmost_start)

    def disable_topmost_window(self) -> None:
        self.root.attributes("-topmost", False)
        self.command_hist(self.language.window_topmost_end)

    def is_debug_enable(self) -> bool:
        """
        conf/debug.txtを読んでTrueならデバッグ関数の有効化
        :return: bool
        """
        try:
            with open("conf/debug.txt", mode="r", encoding=self.code) as f:
                debug_enable = f.read()
                if debug_enable == "True":
                    return True
                else:
                    return False
        except FileNotFoundError:
            with open("conf/debug.txt", mode="w", encoding=self.code) as f:
                f.write("False")
                return False
        except Exception:
            self.command_hist(self.language.fatalError_is_raise)
            raise extend_exception.FatalError

    def autosave_thread(self) -> None:
        """
        Ctrl-Shift-Eでマルチスレッドのオートセーブを有効化
        :return:`
        """
        # prev_text: str = self.page.get("0.0", "end-1c")
        text = ""
        while not self.t_end:
            if self.is_not_t_autosave_enable:
                break
            if not self.is_already_run_autosave_flag:
                break
            if self.file_name == "":
                break
            if not self.is_thread_autosave_flag:
                break
            # text = self.page.get("0.0", "end-1c")
            if not self.que.empty():
                try:
                    text = self.que.get(block=False)
                except queue.Empty:
                    time.sleep(1)
                    continue
            # if prev_text == text:
            #     time.sleep(1)
            #     self.is_save = True
            #     continue
            try:
                with open(self.file_name, "w", encoding=self.code) as file:
                    file.write(text)
            except queue.Empty:
                pass
            self.is_save = True
            time.sleep(2)
            # prev_text = self.page.get("0.0", "end-1c")

    def autosave_thread_start(self, event=None) -> None:
        if event:
            ignore()
        self.t = threading.Thread(target=self.autosave_thread, daemon=True)
        self.is_thread_autosave_flag = True
        self.is_already_run_autosave_flag = True
        self.is_not_t_autosave_enable = False
        self.t_end = False
        self.t.start()
        self.command_hist("ベータ版オートセーブを有効にしました(secret)")

    def autosave_thread_end(self, event=None) -> None:
        if event:
            ignore()
        self.is_thread_autosave_flag = False
        self.is_already_run_autosave_flag = False
        self.t_end = True
        self.is_not_t_autosave_enable = True
        # self.t.join()
        self.command_hist("ベータ版オートセーブを無効にしました(secret)")

    def boss_come(self, event=None):
        if event:
            ignore()
        self.root.iconify()

def init_page(page: tk.Text):
    """
    テキストエリアの初期化処理
    :param page:テキストエリアのインスタンス
    :return:
    """
    decorate: string_decorate.StringDecorator = string_decorate.StringDecorator(page)
    pkvin: Vinegar = vinegar.Vinegar(page)
    return decorate, pkvin


def reset_cursor() -> str:
    default: str = "False 2"
    with open("conf/insert_width.txt", "w") as reset:
        reset.write("False 2")
    return default


def main() -> None:
    """
    主処理系
    if __name__ == "__main__"から呼ばれる
    グローバル変数を閉じ込めるためだけの関数
    :return:None
    """
    file_flag: bool = False
    temp_thread = "False"
    init_done = False
    try:
        with open("conf/init_done.txt", "r") as init_done_file:
            init_done_file.read()
            init_done = True
    except FileNotFoundError:
        messagebox.showinfo("初期化します", "設定ファイルが存在しないか\n破損しているため初期化します")
    conf_flag = os.path.exists("conf")
    if not conf_flag:
        messagebox.showinfo("not initialize", "設定ファイルを作成します")
    independent_method.conf_dir_make()
    open_click_file_name: str = ""
    if len(sys.argv) >= 3:
        print("引数は無しかファイル名一つだけです")
        sys.exit()
    if len(sys.argv) == 2:
        file_flag = True
        open_click_file_name = sys.argv[1]
    # Windowsもしくはそれ以外を判別
    pf: str = platform.system()
    conf_exist: bool = os.path.isdir("conf")
    if not conf_exist:
        try:
            independent_method.conf_dir_make()
        except extend_exception.CannotMakedirsException:
            messagebox.showinfo("can't mkdir!", "設定ファイル用ディレクトリを作成出来ませんでした、終了します")
            raise extend_exception.FatalError
    author: WillBeAuthor = WillBeAuthor()
    root: tk.Tk = tk.Tk()
    author.setroot(root)
    # ラベルの作成
    author.init_label("初期化")
    author.is_saved_flag_color()
    font_family: str = independent_method.read_font()
    font: tk.font.Font = tk.font.Font(root, family=font_family)
    full_screen: full_mode.FullMode = full_mode.FullMode(author)
    full_screen.set_root_full_mode(root)
    root.geometry("820x640")
    cursor_width: int = 2
    try:
        with open("conf/insert_width.txt","r") as f:
            cursor_flag, cursor_width = f.read().split()
        if cursor_flag == "True":
            cursor_width = int(cursor_width)
        elif cursor_flag == "False":
            cursor_width = 2
        else:
            with open("conf/insert_width.txt","w") as reset:
                reset.write("False 2")
                cursor_width = 2
    except ValueError:
        messagebox.showinfo("attention!", author.language.curswidth_reset)
        reset_cursor()
        cursor_width = 2
    except FileNotFoundError:
        messagebox.showinfo("Attention", author.language.cursor_init)
        reset_cursor()
        cursor_width = 2
    except Exception:
        raise extend_exception.FatalError
    page: tk.Text = tk.Text(root, undo=True, wrap="char", insertwidth=cursor_width)
    font_size: int = 13
    font_change: textarea_config.FontChange = textarea_config.FontChange(font_family, font_size, page, author)
    temp_assign: tuple[string_decorate.StringDecorator, vinegar.Vinegar] = init_page(page)
    decorate: string_decorate.StringDecorator
    pk1vin: vinegar.Vinegar
    decorate, pk1vin = temp_assign
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
    # color.binの作成
    try:
        with open("conf/original_theme.txt", "r", encoding=author.code) as tf:
            _ = tf.read()
            pass
        pass
    except FileNotFoundError:
        with open("conf/original_theme.txt", "w", encoding=author.code) as theme_file:
            theme_file.write("False #000000 #FFFFFF #FFFFFF")
    except:
        raise extend_exception.FatalError
    # オートインデントの設定
    try:
        with open("conf/auto_indent.txt", "r", encoding=author.code) as default_indent:
            indent_flag = default_indent.read()
            if indent_flag == "True":
                indent.toggle_auto_indent()
                author.command_hist("auto indent enable")
    except FileNotFoundError:
        with open("conf/auto_indent.txt", "w", encoding=author.code) as default:
            default.write("False")
    except Exception:
        independent_method.fix_this_later()
        raise extend_exception.FatalError
    root.minsize(32, 32)
    menubar: tk.Menu = tk.Menu(root, font=font)
    ask_use_language = "jp"
    try:
        with open("conf/lang.txt", "r") as lang_file:
            ask_use_language = lang_file.read()
        if ask_use_language == "jp" or ask_use_language == "en":
            pass
        else:
            ask_use_language = False
    except FileNotFoundError:
        ask_use_language = False
        pass
    except Exception:
        raise extend_exception.FatalError
    if not ask_use_language:
        ask_use_language = messagebox.askyesno("default language", "使用言語は日本語ですか？(use japanese?")
        if ask_use_language:
            with open("conf/lang.txt", "w", encoding=author.code) as lang_file:
                lang_file.write("jp")
            ask_use_language = "jp"
        else:
            with open("conf/lang.txt", "w", encoding=author.code) as lang_file:
                lang_file.write("en")
            ask_use_language = "en"
    # 一時ファイルをスレッドにするかどうか
    try:
        with open("conf/temp_save_thread.txt", "r", encoding=author.code) as temp_thread_file:
            temp_thread = temp_thread_file.read()
            if temp_thread == "True":
                independent_method.thread_temp_save(author.page)
    except FileNotFoundError:
        with open("conf/temp_save_thread.txt", "w", encoding=author.code) as default:
            default.write("False")
    except Exception:
        raise extend_exception.FatalError
    menu_init.menu_init(author, menubar, pk1vin, indent, full_screen, font_change, use_lang=ask_use_language)
    # タイトル
    root.config(menu=menubar)
    root.title("インクの跡は全て文字")
    author.change_titlebar()
    root.configure(background="gray")

    textarea_config.init_textarea(root, author, page, decorate, indent, font_change)

    root.protocol("WM_DELETE_WINDOW", author.exit_as_save)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    theme: str = author.read_theme()
    author.set_theme(theme=theme)
    author.auto_indent()
    author.command_hist("start initialise")
    author.command_hist("read theme")
    try:
        if author.temp_save_thread_flag and not author.save_thread_done:
            independent_method.thread_temp_save(author.page)
            author.save_thread_done = True
        else:
            independent_method.temp_save(author.page)
    except IgnorableException:
        ignore()
    if temp_thread == "True":
        author.command_hist("一時ファイルの保存にスレッドを使用します")
    author.command_hist("initialising")
    if author.debug_enable:
        author.command_hist("enable debug_log")
    if file_flag:
        author.open_file(open_click_file_name)
    # 文字カウントThreadのスタート
    author.count_thread.start()
    # オートセーブその他の再帰呼び出し
    author.save_cvs_color()
    try:
        with open("conf/init_done.txt", "w") as init_done_file:
            init_done_file.write("")
    except extend_exception.CannotWriteFileException:
        messagebox.showinfo("初期化ファイルを書き込めませんでした")
    except FileNotFoundError:
        pass
    if not init_done:
        messagebox.showinfo("設定を初期化しました", "設定を初期化したのでプログラムを再起動してください")
    root.after(4000, author.repeat_save_file, "dummy")
    insert_mode = textarea_config.ModeChange(author)
    insert_mode.change_vi_insert_mode()
    author.command_hist("initialise complete")
    root.mainloop()


if __name__ == "__main__":
    main()
