import os

import extend_exception
from tkinter import messagebox


def write_theme_string(change_theme) -> None:
    """
    文字列の書き込み
    基本的にテーマファイルへの書き込みに使用
    :param change_theme:
    :return:
    """
    try:
        conf_dir_make()
    except Exception:
        messagebox.showerror("Error!", "ディレクトリを作成出来ませんでした")
        raise extend_exception.FatalError
    with open("conf/color.bin", "w", encoding="utf-8") as file:
        file.write(change_theme)
    return


def write_filename_string(change_filename) -> None:
    """
    ファイルの保存時にpath.binにファイルのパスを書き込む
    :param change_filename: 保存したファイルのフルパス
    :return:
    """
    try:
        conf_dir_make()
    except Exception:
        messagebox.showerror("Error!", "ディレクトリを作成出来ませんでした")
        raise extend_exception.FatalError
    with open("conf/path.bin", mode="w", encoding="utf-8") as sf:
        sf.write(change_filename)
    return


def find_erase_flag_read() -> bool:
    """
    検索時に入力した検索ワードを検索時に消すかどうかの判定
    :return: 成功時True,失敗時False
    """
    try:
        # successはディレクトリの作成結果フラグ
        success = conf_dir_make()
        if not success:
            return False
        with open("conf/find_erase.txt", "r", encoding="utf-8") as fefp:
            erase_flag = fefp.read()
    except FileNotFoundError:
        with open("conf/find_erase.txt", "w", encoding="utf-8") as wp:
            wp.write("False")
            erase_flag = False
    except Exception:
        raise extend_exception.FatalError
    if erase_flag == "True":
        return True
    else:
        return False


def ignore() -> None:
    """
    何もしない
    例外を握りつぶす時等に使用
    passではなく明示的に握りつぶす
    """
    pass
    return


def conf_dir_make() -> bool:
    """
    confディレクトリを作成
    失敗した場合ソレを示す例外を投げる
    :return:
    """
    try:
        os.makedirs("conf", exist_ok=True)
    except Exception:
        messagebox.showerror("cannot make dir!", "ディレクトリを作成出来ませんでした")
        raise extend_exception.CannotMakedirsException
    return True


def read_font() -> str:
    """
    フォントの設定ファイルを読み込み、形式が正しくない場合デフォルトでTimesフォントを使用する
    :return: フォント名
    """
    try:
        conf_dir_make()
    except extend_exception.CannotMakedirsException:
        raise extend_exception.FatalError
    try:
        with open("conf/font-family.txt", "r", encoding="utf-8") as font_conf:
            font = font_conf.read()
            return font
    except FileNotFoundError:
        try:
            with open("conf/font-family.txt", "w", encoding="utf-8") as wf:
                wf.write("Times")
                return "Times"
        except Exception:
            raise extend_exception.FatalError


def path_to_filename(filepath: str) -> str:
    """
    ファイルパスのファイル名を抜き出して返す
    :param filepath:
    :return:ファイル名
    """
    basename = os.path.basename(filepath)
    return basename
