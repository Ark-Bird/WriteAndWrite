class FullMode:
    def __init__(self, root):
        self.root = root
        self.c_mode_flag = False

    def start_c_mode(self) -> None:
        """
        START AUTHOR MODE
        集中モード開始（フルスクリーンになる）
        返り値無し
        """
        if self.c_mode_flag:
            return
        self.c_mode_flag = True
        self.root.attributes("-fullscreen", True)
        return

    def end_c_mode(self) -> None:
        """
        END AUTHOR MODE
        集中モード終了（フルスクリーンは解除されるがウィンドウからフォーカスが外れない場合があるので注意
        返り値無し
        """
        if not self.c_mode_flag:
            return
        self.c_mode_flag = False
        self.root.attributes("-fullscreen", False)
        self.root.geometry("640x640")
        return
