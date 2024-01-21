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


def start_c_mode(root) -> None:
    """
    START AUTHOR MODE
    集中モード開始（フルスクリーンになる）
    返り値無し
    """
    root.attributes("-fullscreen", True)
    return


def end_c_mode(root) -> None:
    """
    END AUTHOR MODE
    集中モード終了（フルスクリーンは解除されるがウィンドウからフォーカスが外れない場合があるので注意
    返り値無し
    """
    root.attributes("-fullscreen", False)
    root.geometry("640x640")
    return


def write_string(change_theme) -> None:
    with open("color.bin", mode="w", encoding="utf-8") as f:
        f.write(change_theme)
    return
