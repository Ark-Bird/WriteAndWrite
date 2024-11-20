import tkinter.messagebox
class Encoding:
    def __init__(self, encoding="utf-8"):
        try:
            with open("conf/encode.txt", "r") as f:
                encoding = f.read()
        except FileNotFoundError:
            with open("conf/encode.txt", "w") as f:
                f.write("utf-8")
            encoding = "utf-8"
            tkinter.messagebox.showinfo("初期化", "エンコーディング指定が無いのでutf-8で作成します")
        except Exception:
            encoding = "utf-8"
        self.code = encoding