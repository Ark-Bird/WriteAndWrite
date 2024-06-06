import tkinter
import tkinter as tk
from tkinter import TclError
from tkinter import messagebox

from wanabi import extend_exception
from wanabi import independent_method
# import independent_method
# from independent_method import ignore


def decorate_text(text, char="") -> str:
    """
    ルビを振った文字列を返す
    傍点とルビの機能を統一
    :param text: ルビを振るテキスト
    :param char: ルビ、デフォルトでは無し
    :return: ルビ用文字を結合した文字列
    """
    return "|" + text + "《" + char + "》"


class StringDecorator:
    def __init__(self, page):
        """
        テキストpageを受け取ってそれを装飾するクラス
        :param page: テキストエリア
        """
        self.page: tkinter.Text = page
        
    def dot_mark(self, event=None) -> None:
        """
        傍点をつける
        pageは傍点をつけるテキストエリアで引数
        おそらく例外は出ないはずなので例外を投げられたら握りつぶす
        :return:
        """
        try:
            m: str = self.page.get("insert", "insert +1c")
            if m == "\n":
                self.page.mark_set("insert", "insert+1c")
                return
            m = decorate_text(m, char="・")
            self.page.delete("insert")
            self.page.insert("insert", m)
        except Exception:
            independent_method.fix_this_later()
            raise extend_exception.FatalError
        return
    
    def three_point(self, event=None) -> None:
        """
        三点リーダの挿入
        全角で二つ一組で挿入
        """
        self.page.insert("insert", """……""")
        self.page.mark_set("insert", "insert-1c")
        return

    def double_dash(self, event=None) -> None:
        """
        ダッシュの挿入
        全角で二つ一組で挿入
        """
        s: str = self.page.get("insert", "insert+1c")
        self.page.insert("insert", """――""" + s)
        self.page.mark_set("insert", "insert-1c")
        return

    def search(self, event=None) -> str | None:
        """
        選択範囲の文字列を先頭から検索
        検索時に消去フラグがTrueならば検索時に検索文字列を削除
        :param event:None
        :return: str | None
        """
        target_full_text: str = self.page.get("0.0", "end")
        search_word: str = ""
        erase_flag: bool = independent_method.find_erase_flag_read()
        try:
            search_word = self.page.get(tk.SEL_FIRST, tk.SEL_LAST)
            if erase_flag:
                self.page.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except TclError:
            independent_method.ignore()
        except Exception:
            independent_method.fix_this_later()
            raise extend_exception.FatalError
        if search_word == "":
            return
        search_result: int = target_full_text.find(search_word)
        self.page.mark_set("insert", "0.0")
        self.page.mark_set("insert", "insert+" + str(search_result) + "c")
        return "break"

    def ruby(self, event=None, char="") -> None:
        """
        テキストを選択してルビを振る
        選択範囲が十文字より多ければ警告を表示、十文字の基準は一般的なWEB小説投稿サイトの最長文字数、
        これ以上でも問題無く表示できるサイトもある、その場合該当業をコメントアウトすればよい
        ルビの書式は小説家になろう及びカクヨム、及びその互換書式に対応しています
        :return:None
        """
        try:
            temp_str: str = self.page.get("sel.first", "sel.last")
            # 投稿サイトが10文字以上のルビに対応の場合、以下二行をコメントアウトしてください
            if len(temp_str) > 10:
                messagebox.showinfo("over", "10文字以上にルビは非対応の可能性があります")
            temp_str = decorate_text(temp_str)
    
            self.page.delete("sel.first", "sel.last")
            self.page.insert("insert", temp_str)
            self.page.mark_set("insert", "insert-1c")
        except TclError:
            independent_method.ignore()
        except Exception:
            independent_method.fix_this_later()
            raise extend_exception.FatalError
        return
