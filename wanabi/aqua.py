#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 20:47:33 2017
@author: hiro
"""
import os
import platform
import sys
import threading
import time
import tkinter
import tkinter as tk
import tkinter.font
from tkinter import filedialog
from tkinter import messagebox
import re
from collections import deque
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
import wanabi.encoding
from wanabi.independent_method import ignore

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
        self.codepoint = wanabi.encoding.Encoding()
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
        self.debug_enable = self.is_debug_enable()
        self.end_of_code = False
        self.mess: None | tk.Label = None
        self.do_command: None | tk.StringVar = None
        self.letter_count = 0
        self.count_thread = threading.Thread(target=self.counter)
        self.com_hist = deque()
        self.app_name: app_name.AppName = app_name.AppName()
        self.is_terminate = False
        self.vi_mode_now = "Command_mode"
        self.is_thread_autosave_flag = False
        self.is_already_run_autosave_flag = False
        self.t = None
        self.is_not_t_autosave_enable = True
        self.t_end = False
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

        :param message:
        :return:
        """
        self.do_command = tk.StringVar()
        self.do_command.set(message)
        self.mess = tk.Label(self.root, textvariable=self.do_command)
        self.mess.pack(side=tk.BOTTOM, fill='x')

    def command_hist(self, command) -> None:
        """
        コマンドのログを表示
        :param command: 実行されたコマンド
        :return: None
        """
        self.com_hist.append(command)
        if len(self.com_hist) > 10:
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
        self.change_titlebar()
        self.is_save = False
        self.is_text_changed()
        self.is_init = False
        return

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
        while True:
            if self.is_terminate:
                break
            s: str = self.page.get("0.0", "end")
            s = re.sub('[ 　\n\r\t]|[|]|《.*》', '', s)
            text_length_without_whitespace: int = len(s)
            self.letter_count = text_length_without_whitespace
            time.sleep(1)

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

    def check_autosave_flag(self) -> str:
        """
        オートセーブの有効かどうかを文字列で返す
        :return: オートセーブの状態
        """
        if self.is_autosave_flag:
            return ":オートセーブ有効:"
        else:
            return ":オートセーブ無効:"

    def change_titlebar(self) -> None:
        """
        タイトルバーの文字列を変更
        :return:None
        """
        # auto_indentはオートインデントが有効かどうかのフラグ
        # half_spaceは挿入されるインデントが半角が全角かのフラグ
        auto_indent: bool = self.indent.auto_indent_enable()
        half_space: bool = self.indent.half_space_checker()
        self.title_var_string = str(self.letter_count) + ":  文字"
        self.check_if_is_saved()
        self.title_var_string = self.app_name.return_app_name_for_now() + self.title_var_string
        # オートインデントの半角/全角状態の表示
        if auto_indent:
            if half_space:
                self.title_var_string += "*オートインデント半角*"
            else:
                self.title_var_string += "*オートインデント全角*"
        else:
            self.title_var_string += "*オートインデント無効"
        # オートセーブは有効か
        self.title_var_string += self.check_autosave_flag()
        # カーソル移動の方法
        self.title_var_string += self.cursor_move_vi_or_emacs()
        self.title_var_string += ":" + self.vi_mode_now
        self.title_var_string += independent_method.path_to_filename(self.file_name)
        self.root.title(self.title_var_string)
        return

    def repeat_save_file(self) -> None:
        """
        オートセーブ
        ファイルパスはユニコードであること
        :return:None
        """
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
            self.command_hist("path.binへの書き込み権限がありません、再試行します")
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
            self.command_hist("path.binへの書き込み権限がありません、再試行します")
        except Exception:
            raise extend_exception.FatalError
        self.change_titlebar()
        if self.is_autosave_flag:
            self.save_file()
            self.is_save = True
            self.before_text = self.page.get("0.0", "end")
        try:
            self.root.after(1000, self.repeat_save_file)
        except Exception:
            self.command_hist("ファイルに書き込めませんでした")
            self.root.after(1000, self.repeat_save_file)
            raise extend_exception.CannotWriteFileException
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
        self.command_hist("オートセーブ機能が有効になりました")
        return

    def change_auto_save_disable(self) -> None:
        """
        オートセーブ機能の無効化
        :return:None
        """
        self.command_hist("オートセーブ機能が無効になりました")
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
        if self.file_name[-4:] != ".txt":
            self.file_name += ".txt"
        if self.before_text == self.page.get("0.0", "end"):
            return
        with open(self.file_name, mode="w", encoding=self.code) as textum_file:
            textum_file.write(self.written_textum)
        if not self.is_autosave_flag:
            self.command_hist(self.file_name + "を保存しました")
        try:
            with open("conf/path.bin", mode="w", encoding=self.code) as conf:
                conf.write(self.file_name)
        except PermissionError:
            self.command_hist("path.binへの書き込み権限がありません、再試行します")
            time.sleep(0.05)
            self.save_file()
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
            self.is_terminate = True
            self.count_thread.join()
            self.end_of_code = True
            self.is_thread_autosave_flag = False
        else:
            return
        if self.is_not_t_autosave_enable:
            self.autosave_thread_end()
        self.root.destroy()
        sys.exit(0)

    def new_blank_file(self) -> None:
        """
        clear text field
        テキストをクリアして新しいファイルにする
        変更フラグを降ろす
        保存フラグを立てる
        :return:None
        """
        self.written_textum = self.page.get("0.0", "end")
        self.prev_save_dir = ""
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
        self.command_hist(self.file_name + "を開きました")
        return

    def text_copy(self, event=None) -> None:
        """
        copy text
        テキストの範囲が選択されていなかった場合例外を投げ、握りつぶす
        :return:None
        """
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
        self.command_hist("ローカルクリップボードにコピーしました")
        return

    def text_paste(self, event=None) -> None:
        """
        paste text
        範囲を選択していなかった場合の例外は握りつぶす
        tk.TclError以外のエラーが出ると落ちる
        :return:None
        """
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
        self.command_hist("ローカルクリップボードからのペーストをしました")
        return

    def text_cut(self, event=None) -> None:
        """
        cut text
        返り値無し
        TclError以外の例外が投げられると落ちる
        :return:None
        """
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
        self.command_hist("ローカルクリップボードへカットしました")
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
        if self.file_name == "":
            messagebox.showinfo("Not open", "現在ファイルを開いていません")
            return "break"
        messagebox.showinfo("現在のファイル", self.file_name)
        return "break"

    def auto_indent(self) -> None:
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
        self.command_hist("オートインデントの初期化")

    def wrap_enable(self) -> None:
        """
        テキストエリアの端で自動で折り返すように設定する
        起動時はこちらのオプションになっている
        :return:None
        """
        self.page.configure(wrap=tk.CHAR)
        return

    def wrap_disable(self) -> None:
        """
        テキストエリアの折り返しを無効化する
        :return:None
        """
        self.page.configure(wrap=tk.NONE)
        return

    def enable_topmost_window(self) -> None:
        self.root.attributes("-topmost", True)
        self.command_hist("ウインドウを最前面にします")

    def disable_topmost_window(self) -> None:
        self.root.attributes("-topmost", False)
        self.command_hist("最前面化を解除しました")

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
        except Exception:
            return False

    def autosave_thread(self) -> None:
        prev_text = self.page.get("0.0", "end-1c")
        while True:
            if self.is_not_t_autosave_enable:
                break
            if not self.is_already_run_autosave_flag:
                break
            if self.file_name == "":
                break
            if not self.is_thread_autosave_flag:
                break
            text = self.page.get("0.0", "end-1c")
            if prev_text == text:
                time.sleep(1)
                self.is_save = True
                continue
            with open(self.file_name, "w", encoding=self.code) as file:
                file.write(text)
            self.is_save = True
            time.sleep(2)
            prev_text = self.page.get("0.0", "end-1c")
    def autosave_thread_start(self, event=None) -> None:
        self.t = threading.Thread(target=self.autosave_thread)
        self.is_thread_autosave_flag = True
        self.is_already_run_autosave_flag = True
        self.is_not_t_autosave_enable = False
        self.t.start()
    def autosave_thread_end(self, event=None) -> None:
        self.is_thread_autosave_flag = False
        self.is_already_run_autosave_flag = False
        self.t_end = True
        self.is_not_t_autosave_enable = True
        # self.t.join()


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
    :return:None
    """
    independent_method.conf_dir_make()
    file_flag: bool = False
    if len(sys.argv) >= 3:
        print("引数は無しかファイル名一つだけです")
        sys.exit()
    if len(sys.argv) == 2:
        file_flag = True
        open_file: str = sys.argv[1]
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
    if file_flag:
        author.file_name = open_file
    root: tk.Tk = tk.Tk()
    author.setroot(root)
    # ラベルの作成
    author.init_label("初期化")
    font_family: str = independent_method.read_font()
    font: tk.font.Font = tk.font.Font(root, family=font_family)
    full_screen: full_mode.FullMode = full_mode.FullMode(author)
    full_screen.set_root_full_mode(root)
    root.geometry("640x640")
    page: tk.Text = tk.Text(root, undo=True, wrap=tkinter.CHAR)
    font_size: int = 13
    font_change: textarea_config.FontChange = textarea_config.FontChange(font_family, font_size, page, author)
    temp_assign: tuple[string_decorate.StringDecorator, vinegar.Vinegar] = init_page(page)
    decorate: string_decorate
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
                author.command_hist("オートインデントは有効です")
    except FileNotFoundError:
        with open("conf/auto_indent.txt", "w", encoding=author.code) as default:
            default.write("False")
    except Exception:
        independent_method.fix_this_later()
        raise extend_exception.FatalError
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
    theme: str = author.read_theme()
    author.set_theme(theme=theme)
    author.auto_indent()
    author.command_hist("初期化始め")
    author.command_hist("テーマを読み込みました")
    author.command_hist("初期化中")
    if author.debug_enable:
        author.command_hist("デバッグログを有効化しました")
    # 文字カウントThreadのスタート
    author.count_thread.start()
    # オートセーブその他の再帰呼び出し
    root.after(4000, author.repeat_save_file)
    insert_mode = textarea_config.ModeChange(author)
    insert_mode.change_vi_insert_mode()
    author.command_hist("初期化完了")
    root.mainloop()


if __name__ == "__main__":
    main()
