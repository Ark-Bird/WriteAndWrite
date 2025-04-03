import tkinter as tk
from cProfile import label
from wanabi import aqua
from wanabi import lang
from wanabi import version
from wanabi import textarea_config
from wanabi import lang
# import version
# import textarea_config
from wanabi import aqua
from tkinter import messagebox
def chg_lang():
    with open("conf/lang.txt", "r") as f:
        now_lang = f.read()
    with open("conf/lang.txt", "w+") as f:
        if now_lang == "jp":
            f.write("en")
        else:
            f.write("jp")
    messagebox.showinfo("need restart","change language is after restart")
def menu_init(author, menubar, pkvin, indent, full_mode, font_change, use_lang="jp") -> None:
    """
    参照の引数menubarに各項目を追加
    初めにバージョンとライセンスを表示するためのクラスのインスタンスを作成している
    :return:
    """
    try:
        with open("conf/lang.txt", "r",) as f:
            UIlang = f.read()
    except FileNotFoundError:
        with open("conf/lang.txt", "w",) as wf:
            wf.write("jp")
            messagebox.showwarning("lang.txt is not found", "lang.txt is Not found set Japanese")
            UIlang = "jp"

    i18n = lang.Language(UIlang)
    # 初期値
    mode_change = textarea_config.ModeChange(author)
    # ヘルプ情報のインスタンス
    show_info: version.ShowInfo = version.ShowInfo()
    file_menu: tk.Menu = tk.Menu(menubar, tearoff=0)
    # ファイルメニュー
    file_menu.add_command(label=i18n.new_file, command=author.new_blank_file)
    file_menu.add_command(label=i18n.open, command=author.open_text_file)
    file_menu.add_command(label=i18n.save, command=author.save_file)
    file_menu.add_command(label=i18n.save_as, command=author.save_as)
    file_menu.add_command(label=i18n.ser_save, command=pkvin.umeboshi)
    file_menu.add_command(label=i18n.des_open, command=pkvin.sunuki)
    file_menu.add_command(
        label=i18n.auto_save, command=author.toggle_autosave_flag
    )
    file_menu.add_command(label=i18n.exit, command=author.exit_as_save)
    menubar.add_cascade(label=i18n.File, menu=file_menu)

    # 編集メニュー、カット、コピー、ペーストをラムダ式で呼び出し
    # editmenu = tk.Menu(menubar, tearoff=0)
    # editmenu.add_command(label="コピー (Ctrl-c)", command=author.text_copy)
    # editmenu.add_command(label="カット (Ctr                                                                 l-x)", command=author.text_cut)
    # # editmenu.add_command(label="貼り付け (Ctrl-v)", command=lambda: author.text_paste())
    # menubar.add_cascade(label="編集", menu=editmenu)

    # フォントサイズ変更
    font_menu = tk.Menu(menubar, tearoff=0)
    font_menu.add_command(label=i18n.large_font, command=font_change.font_size_big)
    font_menu.add_command(label=i18n.small_font, command=font_change.font_size_small)
    menubar.add_cascade(label=i18n.font_size, menu=font_menu)
    # メニューバー作成
    # 集中モード
    c_mode = tk.Menu(menubar, tearoff=0)
    c_mode.add_command(label=i18n.start_concentration, command=full_mode.start_c_mode)
    c_mode.add_command(label=i18n.end_concentration, command=full_mode.end_c_mode)
    menubar.add_cascade(label=i18n.concentration_mode, menu=c_mode)
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
        label="night-sky", command=lambda: author.set_theme(theme="night-sky")
    )
    color_select.add_command(
        label="terminal", command=lambda: author.set_theme(theme="terminal")
    )
    color_select.add_command(
        label="original", command=lambda: author.set_theme(theme="original")
    )
    color_select.add_command(
        label="Apply", command=author.theme_apply
    )
    color_mode.add_cascade(
        label=i18n.change_theme, menu=color_select
    )
    menubar.add_cascade(label=i18n.change_theme, menu=color_mode)
    # オートインデント/オン・オフ
    auto_indent = tk.Menu(menubar, tearoff=0)
    auto_indent.add_command(label=i18n.auto_indent_toggle, command=indent.toggle_auto_indent)
    auto_indent.add_command(label=i18n.auto_indent_half_or_full, command=indent.toggle_half_or_full)
    menubar.add_cascade(label=i18n.auto_indent, menu=auto_indent)
    # 折り返しのオンオフ
    wrap_mode = tk.Menu(menubar, tearoff=0)
    wrap_mode.add_command(label=i18n.wrap_enable, command=author.wrap_enable)
    wrap_mode.add_command(label=i18n.wrap_disable, command=author.wrap_disable)
    menubar.add_cascade(label=i18n.wrap_text, menu=wrap_mode)
    # ViモードとEmacsモードの切り替え
    keybind_mode = tk.Menu(menubar, tearoff=0)
    keybind_mode.add_command(label=i18n.keybind_vi, command=mode_change.change_vi_mode)
    keybind_mode.add_command(label=i18n.keybind_emacs, command=mode_change.change_emacs_mode)
    menubar.add_cascade(label=i18n.keybind_mode, menu=keybind_mode)

    # ツール
    modify_line = tk.Menu(menubar, tearoff=0)
    modify_line.add_command(label=i18n.erase_blank_line, command=author.erase_newline)
    modify_line.add_command(label=i18n.add_blank_line, command=author.insert_newline)
    menubar.add_cascade(label=i18n.tool, menu=modify_line)
    # ウィンドウを最前面に表示
    attri = tk.Menu(menubar, tearoff=0)
    attri.add_command(label=i18n.topmost_enable, command=author.enable_topmost_window)
    attri.add_command(label=i18n.topmost_disable, command=author.disable_topmost_window)
    menubar.add_cascade(label=i18n.is_topmost, menu=attri)
    # ヘルプメニューの表示
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label=i18n.lisence, command=show_info.show_license)
    # バージョン情報
    help_menu.add_command(label=i18n.version, command=show_info.show_version)
    help_menu.add_command(label=i18n.now_file, command=author.file_full_name_show)
    help_menu.add_command(label=i18n.how_config_theme, command=show_info.show_theme_example)
    help_menu.add_command(label=i18n.change_lang, command=chg_lang)
    help_menu.add_command(label=i18n.report, command=version.report_and_contact)
    menubar.add_cascade(label=i18n.HELP, menu=help_menu)
    return
