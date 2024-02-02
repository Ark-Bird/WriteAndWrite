from tkinter import messagebox
import const


class ShowInfo:
    def __init__(self):
        self.LICENSE: const = const.Const("""
    Copyright 2020 hiro

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    """)
        self.version: const = const.Const("0.8.10_β_code:\"MailBlue\"")

    def show_version(self) -> None:
        """
        バージョン情報をポップアップで表示
        :return:
        """
        messagebox.showinfo("バージョン情報:", self.version.get_const())
        return

    def show_license(self) -> None:
        """
        ライセンスをポップアップで表示
        :return:
        """
        messagebox.showinfo("LICENSE", self.LICENSE.get_const())
        return
