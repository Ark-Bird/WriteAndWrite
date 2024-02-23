from tkinter import messagebox
import const


class ShowInfo:
    def __init__(self):
        """
        バイナリ及びソースの除法を定数として記録
        """
        self._LICENSE: const.Const = const.Const("""
    Copyright 2020 hiro

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    """)
        self._version: const.Const = const.Const("""
        ver0.17.8_RC_code:/YetAgain/
        """)

        self._theme_example_conf: const.Const = const.Const("""
        テーマは以下の書式で書いてください
        "#RRGGBB"
        RGBはそれぞれ0~Fまでの数値
        数値の前に#を付けるのを忘れないでください
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

    def show_theme_example(self) -> None:
        """
        オリジナルテーマの設定法
        :return:
        """
        messagebox.showinfo("テーマ設定の書式", self._theme_example_conf.get_const())
