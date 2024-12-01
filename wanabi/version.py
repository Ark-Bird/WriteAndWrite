from tkinter import messagebox
from wanabi import const
# import const


class ShowInfo:
    def __init__(self):
        """
        バイナリ及びソースの情報を定数として記録
        """
        # ライセンス
        self._LICENSE: const.Const = const.Const("""
    Copyright 2020 hiro

         This file is part of wanabi.

    wanabi is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

    wanabi is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with wanabi. If not, see <https://www.gnu.org/licenses/>. 
    """)
        # バージョン
        self._VERSION: const.Const = const.Const("""
        ver2.6.11_code:/天沼矛/beta
        """)

        # テーマ書式
        self._THEME_EXAMPLE_CONF: const.Const = const.Const("""
        テーマは以下の書式で書いてください
        "enable #RRGGBB #RRGGBB #RRGGBB"
        設定値は先頭から　有効 背景 文字色 キャレット色です
        RGBはそれぞれ0~Fまでの数値
        数値の前に#を付けるのを忘れないでください
        先頭の要素が「True」になっている場合ユーザ定義テーマが有効になります
        """)

    def show_version(self) -> None:
        """
        バージョン情報をポップアップで表示
        :return:None
        """
        messagebox.showinfo("バージョン情報:", self._VERSION.get_const())
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
        messagebox.showinfo("テーマ設定の書式", self._THEME_EXAMPLE_CONF.get_const())
        return
