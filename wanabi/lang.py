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
            self.now_file = "現在のファイル"
            self.how_config_theme = "how change theme"
            self.HELP = "HELP"
            self.change_lang = "change_language_jp"
            self.report = "Crash report and support"