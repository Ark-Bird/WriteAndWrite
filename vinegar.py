import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import pickle


class Vinegar:
    def __init__(self, page: tk.Text):
        self.page: tk.Text = page

    def umeboshi(self) -> None:
        """
        テキストをシリアライズして保存
        :return:None
        """
        all_text: str = self.page.get("0.0", "end")
        pkl: str = tk.filedialog.asksaveasfilename()
        pkl = pkl + ".pkl"
        with open(pkl, "wb") as f:
            pickle.dump(all_text, f)
        return

    def sunuki(self) -> None:
        """
        シリアライズしたテキストをロード
        注!:ファイルは信用出来るものを使用すること！
        :return:None
        """
        tkinter.messagebox.showinfo("NOTICE!", "デシリアライズを行う時は対象ファイルが安全であることを確認してください")
        pkl: str = tk.filedialog.askopenfilename()
        if pkl == "":
            return
        with open(pkl, "rb") as f:
            deserialized_text: str = pickle.load(f)
        self.page.delete("0.0", "end")
        self.page.insert("insert", deserialized_text[:-1])
        return
