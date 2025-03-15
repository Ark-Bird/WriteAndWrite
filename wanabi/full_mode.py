import tkinter.messagebox
from wanabi import lang

class FullMode:
    def __init__(self, author):
        """
        初期化、デフォルトで全画面は無効
        rootはset_root_full_modeで設定するのでこの時点では空
        """
        self.lang = lang.Language()
        self.c_mode_flag: bool = False
        self.root = None
        self.author = author

    def set_root_full_mode(self, root) -> None:
        """
        フルスクリーンにするウインドウをセットする
        :param root:rootフィールドにインスタンスを渡す
        :return:None
        """
        self.root = root
        return

    def start_c_mode(self) -> None:
        """
        START AUTHOR MODE
        集中モード開始（フルスクリーンになる）
        :return:None
        """
        if not self.valid_root():
            return
        if self.c_mode_flag:
            return
        self.c_mode_flag = True
        self.root.attributes("-fullscreen", True)
        self.author.command_hist(self.author.language.concentration_mode_start)
        return

    def end_c_mode(self) -> None:
        """
        END AUTHOR MODE
        集中モード終了（フルスクリーンは解除されるがウィンドウからフォーカスが外れない場合があるので注意
        :return:None
        """
        if not self.valid_root():
            return
        if not self.c_mode_flag:
            return
        self.c_mode_flag = False
        self.root.attributes("-fullscreen", False)
        self.root.geometry("640x640")
        self.author.command_hist(self.author.language.concentration_mode_end)
        return

    def valid_root(self) -> bool:
        """
        self.rootがセットされている時Trueを返す
        何らかの原因で実行時に山椒が渡されていない場合False
        :return:None
        """
        if self.root is None:
            tkinter.messagebox.showerror("root is NOT SET", "ウインドウをフルスクリーンにできません")
            return False
        else:
            return True
