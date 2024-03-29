import os

import extend_exception
from tkinter import messagebox

import theme_mod


def write_theme_string(change_theme) -> None:
    """
    文字列の書き込み
    基本的にテーマファイルへの書き込みに使用
    :param change_theme:
    :return:
    """
    try:
        os.makedirs("conf", exist_ok=True)
    except Exception:
        messagebox.showerror("Error!", "ディレクトリを作成出来ませんでした")
        raise extend_exception.FatalError
    with open("conf/color.bin", "w") as file:
        file.write(change_theme)
    return


def write_filename_string(change_filename) -> None:
    """
    ファイルの保存時にpath.binにファイルのパスを書き込む
    :param change_filename: 保存したファイルのフルパス
    :return:
    """
    try:
        os.makedirs("conf", exist_ok=True)
    except Exception:
        messagebox.showerror("Error!", "ディレクトリを作成出来ませんでした")
        raise extend_exception.FatalError
    with open("conf/path.bin", mode="w", encoding="utf-8") as sf:
        sf.write(change_filename)
    return


def ignore() -> None:
    """
    何もしない
    例外を握りつぶす時等に使用
    passではなく明示的に握りつぶす
    """
    pass
    return
