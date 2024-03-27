from tkinter import messagebox
import const


class ShowInfo:
    def __init__(self):
        """
        バイナリ及びソースの情報を定数として記録
        """
        # ライセンス
        self._LICENSE: const.Const = const.Const("""
    Copyright 2020 hiro

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    """)
        # バージョン
        self._version: const.Const = const.Const("""
        ver1.2.23_code:/GA/
        """)

        # テーマ書式
        self._theme_example_conf: const.Const = const.Const("""
        テーマは以下の書式で書いてください
        "#RRGGBB"
        設定値は先頭から 背景 文字色 キャレット色です
        RGBはそれぞれ0~Fまでの数値
        数値の前に#を付けるのを忘れないでください
        """)

    def show_version(self) -> None:
        """
        バージョン情報をポップアップで表示
        :return:None
        """
        messagebox.showinfo("バージョン情報:", self._version.get_const())
        return

    def show_license(self) -> None:
        """
        ライセンスをポップアップで表示
        :return:None
        """
        messagebox.showinfo("LICENSE", self._LICENSE.get_const())
        return

    def show_theme_example(self) -> None:
        """
        オリジナルテーマの設定方法の例示
        :return:None
        """
        messagebox.showinfo("テーマ設定の書式", self._theme_example_conf.get_const())
        return


class AppName:
    def __init__(self):
        self._app_name: const.Const = const.Const("""思兼""")

    def return_app_name_for_now(self):
        """
        暫定アプリ名を返す
        :return: app_name
        """
        return self._app_name.get_const()
