def write_theme_string(change_theme) -> None:
    """
    文字列の書き込み
    基本的にテーマファイルへの書き込みに使用
    :param change_theme:
    :return:
    """
    with open("color.bin", mode="w", encoding="utf-8") as tf:
        tf.write(change_theme)
    return


def write_filename_string(change_filename) -> None:
    with open("path.bin", mode="w", encoding="utf-8") as sf:
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
