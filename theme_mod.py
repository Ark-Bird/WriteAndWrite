import os
import tkinter
from tkinter import messagebox

import _tkinter

import extend_exception
import independent_method


def change_theme(page: tkinter.Text, theme: str) -> None:
    """
    テーマの変更
    引数pageはテキストエリアで、それをthemeに変更
    テーマの種類はここで管理
    どれともマッチしなかった場合は標準テーマでcolor.binを作成
    """
    try:
        with open("dist/custom_theme/original_theme.txt", "r") as theme_file:
            original_theme = theme_file.read()
            enable, bg, fg, cursor = original_theme.split()
        if enable == "True":
            page.configure(bg=bg, fg=fg, insertbackground=cursor)
            return
    except FileNotFoundError:
        messagebox.showerror("テーマファイルが見つかりません", "dist/custom_theme/にオリジナルテーマを作成します")
        os.makedirs("dist/custom_theme", exist_ok=True)
        with open("dist/custom_theme/original_theme.txt", "w") as theme_file:
            theme_file.write("False #000000 #FFFFFF #FFFFFF")
    except _tkinter.TclError:
        messagebox.showerror("テーマ設定エラー", """テーマの数値が違います、
        標準テーマで起動します。
        テーマの書式はHELPからテーマ設定例を調べてください""")
        os.makedirs("dist/custom_theme", exist_ok=True)
        with open("dist/custom_theme/original_theme.txt", "w") as theme_file:
            theme_file.write("False #000000 #FFFFFF #FFFFFF")
        theme = "invalid_theme"
    except Exception:
        messagebox.showerror("不明なエラーです", "original_themeのoriginal_enableの書式が正しくありません、初期設定で作成します、ソフトを再起動してください")
        with open("dist/custom_theme/original_theme.txt", "w") as theme_file:
            theme_file.write("False #000000 #FFFFFF #FFFFFF")
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
