from tkinter import messagebox
import const


def view_version() -> None:
    """
    バージョン情報をポップアップで表示
    :return:
    """
    version: const = const.Const("0.4.3_β_code:\"Shattered Skies\"")
    messagebox.showinfo("バージョン情報:", version)
    return
