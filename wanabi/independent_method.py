import os
import threading
import time
import tkinter

from wanabi import extend_exception
import wanabi.encoding
# import extend_exception
from tkinter import messagebox
import inspect

codepoint = wanabi.encoding.Encoding()
strcode = codepoint.code
def write_theme_string(change_theme) -> None:
    """
    文字列の書き込み
    基本的にテーマファイルへの書き込みに使用
    :param change_theme:
    :return:
    """
    global strcode
    try:
        conf_dir_make()
    except Exception:
        messagebox.showerror("Error!", "ディレクトリを作成出来ませんでした")
        raise extend_exception.FatalError
    with open("conf/color.bin", "w", encoding=strcode) as file:
        file.write(change_theme)
    return


def write_filename_string(change_filename) -> None:
    """
    ファイルの保存時にpath.binにファイルのパスを書き込む
    :param change_filename: 保存したファイルのフルパス
    :return:
    """
    global strcode
    try:
        conf_dir_make()
    except Exception:
        messagebox.showerror("Error!", "ディレクトリを作成出来ませんでした")
        raise extend_exception.FatalError
    try:
        with open("conf/path.bin", mode="w", encoding=strcode) as sf:
            sf.write(change_filename)
    except PermissionError:
        raise extend_exception.PathPermissionException
    return


def find_erase_flag_read() -> bool:
    """
    検索時に入力した検索ワードを検索時に消すかどうかの判定
    :return: 成功時True,失敗時False
    """
    global strcode
    try:
        # successはディレクトリの作成結果フラグ
        success: bool = conf_dir_make()
        if not success:
            return False
        with open("conf/find_erase.txt", "r", encoding=strcode) as fefp:
            erase_flag = fefp.read()
    except FileNotFoundError:
        with open("conf/find_erase.txt", "w", encoding=strcode) as wp:
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
    global strcode
    try:
        conf_dir_make()
    except extend_exception.CannotMakedirsException:
        raise extend_exception.FatalError
    try:
        with open("conf/font-family.txt", "r", encoding=strcode) as font_conf:
            font = font_conf.read()
            return font
    except FileNotFoundError:
        try:
            with open("conf/font-family.txt", "w", encoding=strcode) as wf:
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


def fix_this_later() -> None:
    """
    修正が必要なことをコマンドラインに表示
    :return: None
    """
    global strcode
    mes_box: bool = False
    try:
        with open("wanabi/conf/debug_enable.txt", "r", encoding=strcode) as f:
            debug_flag = f.read()
            if debug_flag == "True":
                mes_box = True
    except FileNotFoundError:
        with open("wanabi/conf/debug_enable.txt", "w", encoding=strcode) as f:
            f.write("False")
    except Exception:
        raise extend_exception.FatalError
    if mes_box:
        print(f"{inspect.stack()[1].function}で例外が起きました")
        messagebox.showwarning("要修正箇所", f"{inspect.stack()[1].function}を修正してください")
    print(inspect.stack()[1].function)
    print("未修正の箇所です")
    return

def temp_save(page: tkinter.Text) -> None:
    """
    クラッシュ時にそこまでのデータがtemp.txtに保存される
    :param page:
    :return:
    """
    global strcode
    try:
        with open("conf/temp.txt", "w", encoding=strcode) as f:
              f.write(page.get("0.0", "end"))
    except Exception:
        print("一時ファイルが作成出来ません")
        raise extend_exception.IgnorableException
    return None

def temp_save_thread(page):
    """
    一時ファイルをスレッドで保存
    :return:
    """
    global strcode
    while True:
        try:
            with open("conf/temp.txt", "w", encoding=strcode) as f:
                f.write(page.get("0.0", "end"))
        except Exception:
            print("一時ファイルへの書き込みに失敗しました")
            raise extend_exception.IgnorableException
        time.sleep(2)
    return None

def thread_temp_save(page):
    """
    スレッドループ
    :return:
    """
    global strcode
    threading.Thread(target=temp_save_thread, daemon=True, args=(page,)).start()