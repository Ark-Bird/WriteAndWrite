import aqua
class NotOpenPathException(Exception):
    """
    ファイルを開くのに失敗した時の例外
    基本的に握りつぶしてデフォルトを適用して続行する目的
    """

    pass


class FatalError(Exception):
    """
    復旧不能なエラーの発生時に投げる
    """

    pass


root = None


def set_root(window):
    """
    windowの参照をもらい、このファイル内のグローバル変数として使用出来るようにする
    :param window:
    :return:
    """
    global root
    root = window


def start_c_mode() -> None:
    """
    START AUTHOR MODE
    集中モード開始（フルスクリーンになる）
    返り値無し
    """
    global root
    root.attributes("-fullscreen", True)
    return


def end_c_mode() -> None:
    """
    END AUTHOR MODE
    集中モード終了（フルスクリーンは解除されるがウィンドウからフォーカスが外れない場合があるので注意
    返り値無し
    """
    global root
    root.attributes("-fullscreen", False)
    root.geometry("640x640")
    return


def write_string(change_theme) -> None:
    """
    文字列の書き込み
    基本的にテーマファイルへの書き込みに使用
    :param change_theme:
    :return:
    """
    with open("color.bin", mode="w", encoding="utf-8") as f:
        f.write(change_theme)
    return
