import tkinter as tk
import tkinter.filedialog
import pickle
class Vinegar:
    def __init__(self, page):
        self.page = page

    def umeboshi(self) -> None:
        all_text = self.page.get("0.0", "end")
        pkl = tk.filedialog.asksaveasfilename()
        pkl = pkl + ".pkl"
        with open(pkl, "wb") as f:
            pickle.dump(all_text, f)
        return

    def sunuki(self) -> None:
        pkl = tk.filedialog.askopenfilename()
        with open(pkl, "rb") as f:
            deserialized_text = pickle.load(f)
        self.page.delete("0.0", "end")
        self.page.insert("insert", deserialized_text[:-1])
        return
