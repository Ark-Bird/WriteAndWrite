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


def dot_mark(page) -> None:
    """
    傍点をつける
    :param page:
    pageは傍点をつけるテキストエリアで引数
    おそらく例外は出ないはずなので例外を投げられたら握りつぶす
    :return:
    """
    try:
        m = page.get("insert", "insert +1c")
        if m == "\n":
            page.mark_set("insert", "insert+1c")
            return
        m = "|" + m + "《・》"
        page.delete("insert")
        page.insert("insert", m)
    except Exception:
        raise FatalError
    return


def three_point(page) -> None:
    """
    三点リーダの挿入
    全角で二つ一組で挿入
    """
    page.insert("insert", "……")
    pass


def double_dash(page) -> None:
    """
    ダッシュの挿入
    全角で二つ一組で挿入
    """
    page.insert("insert", "――")


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
