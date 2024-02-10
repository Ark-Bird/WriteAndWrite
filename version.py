from tkinter import messagebox
import const


class ShowInfo:
    def __init__(self):
        self._LICENSE: const = const.Const("""
    Copyright 2020 hiro

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    """)
        self._version: const.Const = const.Const("""
        0.13.18_RC_code:/MagicOfStella/
        """)
        self._recommend_font: const.Const = const.Const("""
        このプログラムの推奨フォントは
        https://moji.or.jp/
        より配布されているIPAフォントになります、
        リポジトリに同梱されているIPAexfont00401.zipを展開し、
        中のライセンスに同意していただければ使用可能です
        """)

    def show_version(self) -> None:
        """
        バージョン情報をポップアップで表示
        :return:
        """
        messagebox.showinfo("バージョン情報:", self._version.get_const())
        return

    def show_license(self) -> None:
        """
        ライセンスをポップアップで表示
        :return:
        """
        messagebox.showinfo("LICENSE", self._LICENSE.get_const())
        return

    def show_recommend_font(self) -> None:
        """
        推奨フォント情報
        :return:
        """
        messagebox.showinfo("推奨情報", self._recommend_font.get_const())
        return
