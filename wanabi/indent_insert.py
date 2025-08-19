import tkinter


class Indent:
    def __init__(self, author, page):
        self.page: tkinter.Text = page
        self.hit_return: bool = False
        self.auto_indent: bool = False
        self.half_space: bool = False
        self.author = author
        self.blank_line: bool = False
        self.paren_flag: bool = False
        self.paren_kind: str = ""
        self.start_flag: bool = True
        self.in_paren: bool = False

    def toggle_auto_indent(self, event=None) -> bool:
        """
        オートインデント機能のオン・オフ
        返り値は無し
        挿入されるインデントは全角・半角はtoggle_half_or_full関数でトグルする
        デフォルトは全角スペース
        """
        self.auto_indent = not self.auto_indent
        self.author.change_titlebar()
        self.author.command_hist(self.author.language.toggle_auto_indent)
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
        self.author.command_hist(self.author.language.auto_indent_half_or_full)
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

    def paren_del(self) -> None:
        """
        行頭の括弧を入力した時、オートインデントが入っていた場合戦闘の空白を削除
        対応する括弧を挿入
        :return: None
        """

        c = self.page.get("insert -1c")
        s = self.page.get("insert -2c")
        n = self.page.get("insert -3c")
        if c == "「" or c == "『":
            if n == "！" or n == "？":
                return
            if s == " " or s == "　":
                self.page.delete("insert -2c")
            if self.start_flag:
                self.start_flag = False
            if c == "「":
                self.page.insert("insert", "」")
                self.paren_kind = "「"
                self.page.mark_set("insert", "insert -1c")
                self.paren_flag = True
                self.in_paren = True
            if c == "『":
                self.page.insert("insert", "』")
                self.paren_kind = "『"
                self.page.mark_set("insert", "insert -1c")
                self.paren_flag = True
                self.in_paren = True
        c = self.page.get("insert -1c")
        if c == "」" or c == "』":
            if self.paren_kind == "「" and c == "」":
                self.page.delete("insert")
                # self.page.mark_set("insert", "insert +1c")
            if self.paren_kind == "『" and c == "』":
                self.page.delete("insert")
                # self.page.mark_set("insert", "insert +1c")
            self.in_paren = False
        return

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
        :return:None
        """
        if self.hit_return and self.auto_indent:
            self.insert_space()
        else:
            self.paren_del()
        return

    def auto_indent_enable(self):
        return self.auto_indent

    def half_space_checker(self):
        return self.half_space
