import tkinter.messagebox
import os
from tkinter import messagebox
from wanabi import lang

class Encoding:
    def __init__(self, encoding="utf-8"):
        """
        encodingで実行時に書き込む文字コードが決まる、デフォルトはUTF-８
        :param encoding: 書き出すときのエンコーディング
        """
        self.lang = lang.Language()
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
            with open("conf/encode.txt", "w") as f:
                f.write("utf-8")
            messagebox.showerror(self.lang.unknown_code(0), self.lang.unknown_code(1))
        self.code = encoding

    def recover(self):
        messagebox.showinfo(self.lang.unknown_encode[0], self.lang.unknown_encode[1])
        with open("conf/encode.txt", "w") as f:
            f.write("utf-8")
