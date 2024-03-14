import os
import tkinter
from tkinter import messagebox

import _tkinter

import extend_exception
import independent_method


def make_default_theme() -> None:
    """
    何らかの理由でテーマファイルが存在しない、もしくは破損している場合に生成
    :return:None
    """
    os.makedirs("conf", exist_ok=True)
    with open("conf/original_theme.txt", "w") as theme_file:
        theme_file.write("False #000000 #FFFFFF #FFFFFF")
    return


def change_theme(page: tkinter.Text, theme: str) -> None:
    """
    テーマの変更
    引数pageはテキストエリアで、それをthemeに変更
    テーマの種類はここで管理
    どれともマッチしなかった場合は標準テーマでcolor.binを作成
    :return:None
    """
    os.makedirs("conf", exist_ok=True)
    try:
        with open("conf/original_theme.txt", "r") as theme_file:
            original_theme = theme_file.read()
            enable, bg, fg, cursor = original_theme.split()
    except FileNotFoundError:
        messagebox.showerror("テーマファイルが見つかりません", "dist/custom_theme/にオリジナルテーマを作成します")
        make_default_theme()
    except _tkinter.TclError:
        messagebox.showerror("テーマ設定エラー", """テーマの数値が違います、
        標準テーマで起動します。
        テーマの書式はHELPからテーマ設定例を調べてください""")
        make_default_theme()
        theme = "invalid_theme"
    except Exception:
        messagebox.showerror("不明なエラーです", "original_themeのoriginal_enableの書式が正しくありません、初期設定で作成します、ソフトを再起動してください")
        make_default_theme()
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
        case "original":
            if enable == "True":
                page.configure(bg=bg, fg=fg, insertbackground=cursor)
            else:
                messagebox.showinfo("変更出来ません", """コンフィグファイルでカスタムテーマが無効になっています
                テーマをデフォルトのものに初期化します""")
                independent_method.write_theme_string("normal")
                with open("conf/original_theme.txt", "w") as theme_file:
                    theme_file.write("False #000000 #FFFFFF #FFFFFF")
                return
        case _:
            messagebox.showerror("original_themeの書式が正しくありません", "テーマファイルの破損、もしくは存在していません、標準設定で作成します")
            independent_method.write_theme_string("normal")
            make_default_theme()
            page.configure(bg="ghost white", fg="black", insertbackground="black")
    return
