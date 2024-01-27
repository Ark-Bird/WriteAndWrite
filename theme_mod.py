import independent_method


def change_theme(page, theme) -> None:
    """
    テーマの変更
    引数pageはテキストエリアで、それをthemeに変更
    テーマの種類はここで管理
    どれともマッチしなかった場合は標準テーマでcolor.binを作成
    """
    match theme:
        case "normal":
            page.configure(bg="ghost white", fg="black", insertbackground="black")
        case "dark":
            page.configure(bg="gray16", fg="azure", insertbackground="white")
        case "paper":
            page.configure(bg="azure", fg="blueviolet", insertbackground="blueviolet")
        case "terminal":
            page.configure(bg="black", fg="springgreen3", insertbackground="green")
        case _:
            independent_method.write_string("normal")
            page.configure(bg="ghost white", fg="black", insertbackground="black")
    return
