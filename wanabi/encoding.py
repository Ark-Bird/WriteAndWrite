import tkinter.messagebox
import os
class Encoding:
    def __init__(self, encoding="utf-8"):
        """
        encodingで実行時に書き込む文字コードが決まる、デフォルトはUTF-８
        :param encoding: 書き出すときのエンコーディング
        """
        try:
            with open("conf/encode.txt", "r") as f:
                encoding = f.read()
        except FileNotFoundError:
            try:
                os.makedirs("conf", exist_ok=True)
            except Exception:
                tkinter.messagebox.showerror("cannot make dir!", "ディレクトリを作成出来ませんでした")
                raise Exception
            with open("conf/encode.txt", "w") as f:
                f.write("utf-8")
            encoding = "utf-8"
            tkinter.messagebox.showinfo("初期化", "エンコーディング指定が無いのでutf-8で作成します")
        except Exception:
            encoding = "utf-8"
        self.code = encoding