import tkinter as tk
import version
import textarea_config
from keybind import keybind


def menu_init(author, menubar, pkvin, indent, full_mode) -> None:
    """
    参照の引数menubarに各項目を追加
    初めにバージョンとライセンスを表示するためのクラスのインスタンスを作成している
    :return:
    """
    font_size: int = 13
    font_change = textarea_config.FontChange(font_size, author.page)
    show_info: version.ShowInfo = version.ShowInfo()
    mode_change: textarea_config.ModeChange = textarea_config.ModeChange(author)
    file_menu: tk.Menu = tk.Menu(menubar, tearoff=0)
    # ファイルメニュー、渡している'file'引数はダミー
    file_menu.add_command(label="新規ファイル", command=author.new_blank_file)
    file_menu.add_command(label="開く", command=author.open_text_file)
    file_menu.add_command(label="保存 (Ctrl-s)", command=author.save_file)
    file_menu.add_command(label="名前をつけて保存", command=author.save_as)
    file_menu.add_command(label="シリアライズして保存", command=pkvin.umeboshi)
    file_menu.add_command(label="デシリアライズして開く", command=pkvin.sunuki)
    file_menu.add_command(
        label="オートセーブ (Ctrl-e)", command=author.toggle_autosave_flag
    )
    file_menu.add_command(label="終了", command=author.exit_as_save)
    menubar.add_cascade(label="ファイル", menu=file_menu)

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
        label="nightsky", command=lambda: author.set_theme(theme="nightsky")
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
    # 折り返しのオンオフ
    wrap_mode = tk.Menu(menubar, tearoff=0)
    wrap_mode.add_command(label="折り返し有効", command=author.wrap_enable)
    wrap_mode.add_command(label="折り返し無効", command=author.wrap_disable)
    menubar.add_cascade(label="行末の折り返し", menu=wrap_mode)
    # ViモードとEmacsモードの切り替え
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
    help_menu.add_command(label="現在のファイル(Ctrl-0)", command=author.file_full_name_show)
    help_menu.add_command(label="推奨フォント", command=show_info.show_recommend_font)
    menubar.add_cascade(label="HELP", menu=help_menu)
    return
