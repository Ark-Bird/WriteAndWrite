import tkinter as tk
import version
import textarea_config
from keybind import keybind


def menu_init(author, menubar, pkvin, indent, full_mode):
    """
    参照の引数menubarに各項目を追加
    初めにバージョンとライセンスを表示するためのクラスのインスタンスを作成している
    :return:
    """
    font_size = 10
    font_change = textarea_config.FontChange(font_size, author.page)
    show_info = version.ShowInfo()
    mode_change = textarea_config.ModeChange(author.page)
    filemenu = tk.Menu(menubar, tearoff=0)
    # ファイルメニュー、渡している'file'引数はダミー
    filemenu.add_command(label="新規ファイル", command=author.new_blank_file)
    filemenu.add_command(label="開く", command=author.open_text_file)
    filemenu.add_command(label="保存 (Ctrl-s)", command=author.save_file)
    filemenu.add_command(label="名前をつけて保存", command=author.save_as)
    filemenu.add_command(label="シリアライズして保存", command=pkvin.umeboshi)
    filemenu.add_command(label="デシリアライズして開く", command=pkvin.sunuki)
    filemenu.add_command(
        label="オートセーブ (Ctrl-e)", command=author.toggle_as_flag
    )
    filemenu.add_command(label="終了", command=author.exit_as_save)
    menubar.add_cascade(label="ファイル", menu=filemenu)

    # 編集メニュー、カット、コピー、ペーストをラムダ式で呼び出し
    # editmenu = tk.Menu(menubar, tearoff=0)
    # editmenu.add_command(label="コピー (Ctrl-c)", command=author.text_copy)
    # editmenu.add_command(label="カット (Ctrl-x)", command=author.text_cut)
    # # editmenu.add_command(label="貼り付け (Ctrl-v)", command=lambda: author.text_paste())
    # menubar.add_cascade(label="編集", menu=editmenu)

    # フォントサイズ変更
    fontmenu = tk.Menu(menubar, tearoff=0)
    fontmenu.add_command(label="フォントを大きく", command=font_change.font_size_big)
    fontmenu.add_command(label="フォントを小さく", command=font_change.font_size_small)
    menubar.add_cascade(label="フォントサイズ", menu=fontmenu)
    # メニューバー作成
    # 集中モード
    c_mode = tk.Menu(menubar, tearoff=0)
    c_mode.add_command(label="スタート", command=full_mode.start_c_mode)
    c_mode.add_command(label="終了", command=full_mode.end_c_mode)
    menubar.add_cascade(label="集中モード", menu=c_mode)
    # ColorMode Change
    color_mode = tk.Menu(menubar, tearoff=False)
    color_select = tk.Menu(color_mode, tearoff=False)
    color_select.add_command(
        label="normal", command=lambda: author.set_theme(theme="normal")
    )
    color_select.add_command(
        label="dark", command=lambda: author.set_theme(theme="dark")
    )
    color_select.add_command(
        label="paper", command=lambda: author.set_theme(theme="paper")
    )
    color_select.add_command(
        label="terminal", command=lambda: author.set_theme(theme="terminal")
    )
    color_mode.add_cascade(label="テーマ切り替え", menu=color_select)
    menubar.add_cascade(label="テーマ", menu=color_mode)
    # オートインデント/オン・オフ
    auto_indent = tk.Menu(menubar, tearoff=0)
    auto_indent.add_command(label="オン/オフ (Ctrl-q)", command=indent.toggle_auto_indent)
    auto_indent.add_command(label="半角/全角 (Ctrl-w)", command=indent.toggle_half_or_full)
    menubar.add_cascade(label="オートインデント", menu=auto_indent)
    #ViモードとEmacsモードの切り替え
    keybind_mode = tk.Menu(menubar, tearoff=0)
    keybind_mode.add_command(label="Vi-Mode", command=mode_change.change_vi_mode)
    keybind_mode.add_command(label="Emacs-Mode", command=mode_change.change_emacs_mode)
    menubar.add_cascade(label="Keybind Mode", menu=keybind_mode)
    # ヘルプメニューの表示
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(
        label="LICENSE", command=show_info.show_license
    )
    # バージョン情報
    help_menu.add_command(label="VERSION", command=show_info.show_version)
    menubar.add_cascade(label="HELP", menu=help_menu)
