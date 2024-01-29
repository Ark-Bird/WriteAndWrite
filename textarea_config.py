import tkinter as tk


def init_textarea(root, author, page, decorate, indent) -> None:
    # テキストエリアを配置し、スクロールバーを付ける
    xscrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=page.xview)
    yscrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=page.yview)
    yscrollbar.pack(side=tk.RIGHT, fill="y")
    xscrollbar.pack(side=tk.BOTTOM, fill="x")
    page.pack(fill="both", expand=True)
    page["yscrollcommand"] = yscrollbar.set
    page["xscrollcommand"] = xscrollbar.set

    # ファイルを保存
    page.bind("<Control-s>", author.save_file)
    # コピペ＆カット
    # page.bind("<Control-c>", author.text_copy)
    # page.bind('<Control-v>', author.text_paste)
    # page.bind("<Control-x>", author.text_cut)
    # 三点リーダー二つ組挿入
    page.bind("<Control-t>", decorate.three_point)
    # ダッシュの挿入
    page.bind("<Control-d>", decorate.double_dash)
    # ルビを振る
    page.bind("<Control-r>", decorate.ruby)
    # 傍点をつける
    page.bind("<Control-b>", decorate.dot_mark)
    # オートインデント
    # 半角全角切り替え
    page.bind("<Control-w>", indent.toggle_half_or_full)
    # オートインデントのオン・オフ
    page.bind("<Control-q>", indent.toggle_auto_indent)
    # オートセーブ
    page.bind("<Control-e>", author.toggle_as_flag)
    # エンターが押された場合、IMEの変換で押したものか改行をしたのかを判断してオートインデントを行う
    page.bind("<KeyPress-Return>", indent.ime_check)
    page.bind(
        "<KeyRelease-Return>",
        indent.indent_system
    )
    # 文字カウント
    page.bind("<Any-KeyPress>", author.logger)
    return
