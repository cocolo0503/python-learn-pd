import tkinter as tk
from tkinter import messagebox
from json_writer import JsonWriter
from logic_calculator import DQ1Calculator

class DQ1App:
    def __init__(self, root):
        self.root = root
        self.root.title("DQ1ふっかつのじゅもんジェネレーター")
        self.root.geometry("500x700")

        # UI要素の定義
        tk.Label(root, text="なまえ:").pack()
        self.e_name = tk.Entry(root, justify="center"); self.e_name.insert(0, "もょもと"); self.e_name.pack()

        tk.Label(root, text="けいけんち:").pack()
        self.s_exp = tk.Scale(root, from_=0, to=65535, orient="horizontal", length=300); self.s_exp.pack()

        tk.Label(root, text="ゴールド:").pack()
        self.s_gold = tk.Scale(root, from_=0, to=65535, orient="horizontal", length=300); self.s_gold.pack()

        # 道具
        tk.Label(root, text="やくそう / かぎ (個数):").pack()
        self.s_y = tk.Scale(root, from_=0, to=6, orient="horizontal", length=100); self.s_y.pack()
        self.s_k = tk.Scale(root, from_=0, to=6, orient="horizontal", length=100); self.s_k.pack()

        # 重要アイテム
        self.items_vars = {
            "たいようのいし": tk.BooleanVar(), "ぎんのたてごと": tk.BooleanVar(),
            "おうじょのあい": tk.BooleanVar(), "ろとのしるし": tk.BooleanVar(),
            "にじのしずく": tk.BooleanVar()
        }
        for k, v in self.items_vars.items():
            tk.Checkbutton(root, text=k, variable=v).pack()

        # ボタン
        btn_f = tk.Frame(root)
        btn_f.pack(pady=10)
        tk.Button(btn_f, text="1. JSON保存", command=self.save, bg="#4CAF50", fg="white", width=15).pack(side="left", padx=5)
        tk.Button(btn_f, text="2. 呪文生成", command=self.calc, bg="#2196F3", fg="white", width=15).pack(side="left", padx=5)

        self.res = tk.Entry(root, font=("MS Gothic", 16), justify="center", bg="black", fg="#00FF00")
        self.res.pack(fill="x", padx=20, pady=20)

    def save(self):
        ui_data = {
            "name": self.e_name.get(),
            "status": {
                "exp": self.s_exp.get(), "gold": self.s_gold.get(),
                "weapon": 7, "armor": 7, "shield": 2
            },
            "items": {
                "yakuso": self.s_y.get(), "kagi": self.s_k.get(),
                **{k: v.get() for k, v in self.items_vars.items()}
            },
            "flags": {"dragon": False}
        }
        JsonWriter.save_to_json(ui_data)
        messagebox.showinfo("成功", "JSONに記録しました")

    def calc(self):
        self.res.delete(0, tk.END)
        self.res.insert(0, DQ1Calculator.generate_from_json())

if __name__ == "__main__":
    root = tk.Tk(); app = DQ1App(root); root.mainloop()