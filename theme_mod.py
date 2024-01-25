import independent_method


def change_theme(page, theme) -> None:
    """
    テーマの変更
    theme_fはテーマが変更されているかのフラグ、Falseの時即時リターン
    new_themeは変更するテーマ
    モード名をcolor.binに書き込む
    color.binに存在しないテーマ名が書き込まれていた場合標準テーマに変更
    該当ファイルはプレーンテキストでありマニュアルでの編集が可能
    ストレージへの負荷軽減のためモード変更のない場合ファイルへ書き込まずリターン
    """
    if theme == "dark":
        independent_method.write_string("dark")
        page.configure(bg="gray16", fg="azure", insertbackground="white")
    elif theme == "paper":
        independent_method.write_string("paper")
        page.configure(bg="azure", fg="blueviolet", insertbackground="blueviolet")
    elif theme == "terminal":
        independent_method.write_string("terminal")
        page.configure(bg="black", fg="springgreen3", insertbackground="green")
    else:
        independent_method.write_string("normal")
        page.configure(bg="ghost white", fg="black", insertbackground="black")
    return
