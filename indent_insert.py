from independent_method import ignore


class Indent:
    def __init__(self, author, page):
        self.page = page
        self.hit_return: bool = False
        self.auto_indent: bool = False
        self.half_space: bool = False
        self.author = author
        self.blank_line = False

    def toggle_auto_indent(self, event=None) -> bool:
        """
        オートインデント機能のオン・オフ
        返り値は無し
        挿入されるインデントは全角・半角はtoggle_half_or_full関数でトグルする
        デフォルトは全角スペース
        """
        self.auto_indent = not self.auto_indent
        self.author.change_titlebar()
        return self.auto_indent

    def toggle_half_or_full(self, event=None) -> None:
        """
        オートインデントの半角全角切り替え
        """
        if self.half_space:
            self.half_space = False
        else:
            self.half_space = True
        self.author.change_titlebar()
        return

    def insert_space(self, ev=None) -> None:
        """
        オートインデント
        self.half_spaceがTrueのとき半角スペース、Falseの時全角スペースのインデントを挿入
        カーソルを移動して前の文字を調べ、空行と判断すればインデントを削除する
        """
        if self.hit_return:
            if self.blank_line:
                prev = self.page.get("insert -3c")
                d = self.page.get("insert -2c")
                if (d == " " or d == "　") and prev == "\n":
                    self.page.delete("insert -2c")
                if self.half_space:
                    self.page.insert("insert", " ")
                else:
                    self.page.insert("insert", "　")
            self.hit_return = False
        return

    def paren_del(self):
        c = self.page.get("insert -1c")
        s = self.page.get("insert -2c")
        if c == "「" and s == "　":
            self.page.delete("insert -2c")

    def ime_check(self, event=None) -> None:
        """
        IMEのリターンか、改行かの判断
        改行ならばインスタンス変数のhit_returnを立てる
        返り値無し
        """
        self.blank_line = True
        self.hit_return = True
        return

    def indent_system(self, event=None) -> None:
        """
        インデントの挿入
        EnterがIMEの確定ならなにもしない
        :param event: 無視する
        :return:
        """
        if self.hit_return and self.auto_indent:
            self.insert_space()
        else:
            self.paren_del()
            ignore()

    def auto_indent_enable_and_half_space_checker(self):
        return self.auto_indent, self.half_space
