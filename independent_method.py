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


def ignore() -> None:
    """
    何もしない
    例外を握りつぶす時等に使用
    passではなく明示的に握りつぶす
    """
    pass
    return
