from tkinter import messagebox

import _tkinter

import extend_exception
import independent_method
from costom_theme import original_theme


def change_theme(page, theme) -> None:
    """
    テーマの変更
    引数pageはテキストエリアで、それをthemeに変更
    テーマの種類はここで管理
    どれともマッチしなかった場合は標準テーマでcolor.binを作成
    """
    try:
        if original_theme.original_enable:
            page.configure(bg=original_theme.back, fg=original_theme.letter, insertbackground=original_theme.cursor)
            return
    except _tkinter.TclError:
        messagebox.showerror("テーマ設定エラー", """テーマの数値が違います、
        標準テーマで起動します。
        テーマの書式はHELPからテーマ設定例を調べてください""")
        theme = "invalid_theme"
    except Exception:
        messagebox.showerror("不明なエラーです", "original_themeのoriginal_enableをFalseに設定することを考慮してください")
        raise extend_exception.FatalError
    match theme:
        case "normal":
            page.configure(bg="ghost white", fg="black", insertbackground="black")
        case "dark":
            page.configure(bg="gray16", fg="azure", insertbackground="white")
        case "paper":
            page.configure(bg="azure", fg="blueviolet", insertbackground="blueviolet")
        case "night-sky":
            page.configure(bg="#000022", fg="lavender", insertbackground="lightyellow")
        case "terminal":
            page.configure(bg="black", fg="springgreen3", insertbackground="green")
        case _:
            print("テーマファイルの破損、もしくは存在していません、標準設定で作成します")
            independent_method.write_theme_string("normal")
            page.configure(bg="ghost white", fg="black", insertbackground="black")
    return
