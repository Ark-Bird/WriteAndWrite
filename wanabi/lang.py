class Language:
    def __init__(self, Area="jp"):
        self.area = Area
        self.lang = "jp"
        if self.area == "jp":
            self.new_file = "新規ファイル"
            self.open = "開く"
            self.save = "保存"
            self.save_as = "名前を付けて保存"
            self.ser_save = "シリアライズして保存"
            self.des_open = "デシリアイズして開く"
            self.auto_save = "オートセーブ"
            self.exit = "終了"
            self.File = "ファイル"
            self.large_font = "フォントを大きく(Ctrl-L)"
            self.small_font = "フォントを小さく(Ctrl-S)"
            self.font_size = "フォントサイズ"
            self.start_concentration = "スタート"
            self.end_concentration = "終了"
            self.concentration_mode = "集中モード"
            self.change_theme = "テーマを変更"
            self.auto_indent_toggle = "オン/オフ(Ctrl-q)"
            self.auto_indent_half_or_full = "半角/全角"
            self.auto_indent = "オートインデント"
            self.wrap_enable = "折り返し有効"
            self.wrap_disable = "折り返し無効"
            self.wrap_text = "行末の折り返し"
            self.keybind_vi = "Vi-Mode"
            self.keybind_emacs = "Emacs-Mode"
            self.keybind_mode = "Keybind Mode"
            self.erase_blank_line = "連続した改行を削除"
            self.add_blank_line = "空行を挿入"
            self.tool = "ツール"
            self.topmost_enable = "最前面に表示"
            self.topmost_disable = "最前面表示を終了"
            self.is_topmost = "ウインドウ"
            self.lisence = "LISENCE"
            self.version = "version"
            self.now_file = "現在のファイル"
            self.how_config_theme = "テーマ設定方法"
            self.HELP = "HELP"
            self.change_lang = "change_language_en"
            self.report = "不具合の報告"
            # logmessage
            self.pathfile_permission_error = "path.binへの書き込み権限がありません、再試行します"
            self.cannot_write_file = "ファイルに書き込めませんでした"
            self.auto_save_enabled = "オートセーブが有効になりました"
            self.auto_save_disabled = "オートセーブが無効になりました"
            self.save_complete = "保存しました"
            self.opened = "開きました"
            self.app_clipboard_copy = "ローカルクリップボードにコピーしました"
            self.app_clipboard_paste = "ローカルクリップボードからのペーストをしました"
            self.app_clipboard_cut = "ローカルクリップボードへカットしました"
            self.init_auto_indent = "オートインデントの初期化"
            self.window_topmost_start = "ウインドウを最前面にします"
            self.window_topmost_end = "最前面化を解除しました"
            self.cursor_init = "カーソル設定ファイルがありません、作成します"
            self.curswidth_reset = "カーソル幅の設定ファイルが解釈できなかったため初期化します"
            self.fatalError_is_raise = "復帰不可能なエラーが発生しました"
            # c-mode
            self.concentration_mode_start = "集中モードを開始しました"
            self.concentration_mode_end = "集中モードを終了しました"
            # indent
            self.auto_indent_enable = "オートインデントは有効です"
            self.toggle_auto_indent = "インデント有効/無効を変更しました"
            self.auto_indent_half_or_full = "インデント半角/全角を変更"
            # furniture
            self.save_on_RAM_memory = "RAM上にテキストを保存しました"
            # font-size
            self.font_size_big = "フォントサイズを大きくしました"
            self.font_size_small = "フォントサイズを小さくしました"
            # mode
            self.keybind_vi = "viモードに変更"
            self.in_insert_mode = "インサートモードに変更"
            self.keybind_emacs = "emacsモードに変更"
            # titlebar
            self.title = "無題"
            self.no_saved = "未保存"
            self.saved = "保存住み"
            self.char = "文字"
            self.auto_indent_half_width = "オートインデント半角"
            self.auto_indent_full_width = "オートインデント全角"
            self.auto_indent_disable_now = "インデント無効"
        elif self.area == "en":
            self.new_file = "new file"
            self.open = "open file"
            self.save = "save file"
            self.save_as = "save as"
            self.ser_save = "save with serialize"
            self.des_open = "open deserialize"
            self.auto_save = "auto save"
            self.exit = "exit"
            self.File = "FILE"
            self.large_font = "large font(Ctrl-L)"
            self.small_font = "small font(Ctrl-S)"
            self.font_size = "Font Size"
            self.start_concentration = "Start"
            self.end_concentration = "End"
            self.concentration_mode = "Concentration Mode"
            self.change_theme = "change theme"
            self.auto_indent_toggle = "on/off(Ctrl-q)"
            self.auto_indent_half_or_full = "half/multi"
            self.auto_indent = "auto indent"
            self.wrap_enable = "wrap enable"
            self.wrap_disable = "wrap disable"
            self.wrap_text = "wrap text"
            self.keybind_vi = "Vi-Mode"
            self.keybind_emacs = "Emacs-Mode"
            self.keybind_mode = "Keybind Mode"
            self.erase_blank_line = "erase blank line"
            self.add_blank_line = "insert blank line"
            self.tool = "TOOL"
            self.topmost_enable = "topmost"
            self.topmost_disable = "end topmost"
            self.is_topmost = "Window"
            self.lisence = "LISENCE"
            self.version = "version"
            self.now_file = "Now Edit FILE"
            self.how_config_theme = "how change theme"
            self.HELP = "HELP"
            self.change_lang = "change_language_jp"
            self.report = "Crash report and support"
            # log meesage
            self.pathfile_permission_error = "can't write to path.bin、retry"
            self.cannot_write_file = "can't write a file"
            self.auto_save_enabled = "autosave enabled"
            self.auto_save_disabled = "autosave disabled"
            self.save_complete = "save complete"
            self.opened = "opened"
            self.app_clipboard_copy = "copy app clipboard"
            self.app_clipboard_paste = "paste app clipboard"
            self.app_clipboard_cut = "cut app clipboard"
            self.init_auto_indent = "initialize auto indent"
            self.window_topmost_start = "window topmost start"
            self.window_topmost_end = "window topmost end"
            self.cursor_init = "cursor config file is not found, create it"
            self.curswidth_reset = ("cursor width config is invalid," +
                                    " reset file")
            self.fatalError_is_raise = "fatal error is raised"
            self.auto_indent_enable = "auto_indent is enable"
            # c-mode
            self.concentration_mode_start = "concentration mode start"
            self.concentration_mode_end = "concentration mode end"
            # indent
            self.auto_indent_enable = "auto_indent is enable"
            self.toggle_auto_indent = "enable/disable auto_indent"
            self.auto_indent_half_or_full = "toggle auto_indent half or full"
            # furniture
            self.save_on_RAM_memory = "write on RAM memory"
            # font
            self.font_size_big = "font size zoom"
            self.font_size_small = "font size smaller"
            # mode
            self.change_vi_bind = "set keybind vi"
            self.in_insert_mode = "in insert mode"
            self.keybind_emacs = "set keybind emacs"
            # titlebar
            self.title = "no title"
            self.no_saved = "no saved"
            self.saved = "saved"
            self.char = " letter"
            self.auto_indent_half_width = " auto_indent half"
            self.auto_indent_full_width = " auto_indent full"
            self.auto_indent_disable_now = " auto_indent disable"