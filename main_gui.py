import tkinter as tk
from tkinter import messagebox, ttk
from json_writer import JsonWriter
from logic_calculator import DQ1Calculator

class DQ1App:
    def __init__(self, root):
        self.root = root
        self.root.title("DQ1ふっかつメーカー・コンプリート")
        self.root.geometry("600x700")

        # --- ステータスエリア ---
        st_frame = tk.LabelFrame(root, text="ステータス")
        st_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(st_frame, text="なまえ:").grid(row=0, column=0)
        self.e_name = tk.Entry(st_frame); self.e_name.insert(0, "ろと"); self.e_name.grid(row=0, column=1)
        
        tk.Label(st_frame, text="EXP:").grid(row=1, column=0)
        self.s_exp = tk.Scale(st_frame, from_=0, to=65535, orient="horizontal", length=200); self.s_exp.grid(row=1, column=1)

        # --- 装備エリア ---
        eq_frame = tk.LabelFrame(root, text="そうび")
        eq_frame.pack(fill="x", padx=10, pady=5)
        self.WS = ["なし","たけざお","こんぼう","銅剣","鉄斧","鋼剣","炎剣","ロト剣"]
        self.v_w = tk.StringVar(value=self.WS[0]); tk.OptionMenu(eq_frame, self.v_w, *self.WS).pack(side="left")
        self.AS = ["なし","布","皮","鎖","鉄","鋼","魔法","ロト鎧"]
        self.v_a = tk.StringVar(value=self.AS[0]); tk.OptionMenu(eq_frame, self.v_a, *self.AS).pack(side="left")

        # --- 重要アイテムエリア ---
        it_frame = tk.LabelFrame(root, text="だいじなもの")
        it_frame.pack(fill="x", padx=10, pady=5)
        self.items_vars = {
            "matsutake": tk.BooleanVar(), "taiyo_ishi": tk.BooleanVar(),
            "lora_love": tk.BooleanVar(), "nijino_shizuku": tk.BooleanVar(),
            "roto_shirusu": tk.BooleanVar()
        }
        for k, v in self.items_vars.items():
            tk.Checkbutton(it_frame, text=k, variable=v).pack(side="left")

        # --- ボタン ---
        tk.Button(root, text="1. JSON保存", command=self.save, bg="#4CAF50", fg="white").pack(pady=5)
        tk.Button(root, text="2. 呪文生成", command=self.calc, bg="#2196F3", fg="white").pack(pady=5)

        self.res = tk.Entry(root, font=("MS Gothic", 18), justify="center", bg="black", fg="#00FF00")
        self.res.pack(padx=10, pady=20, fill="x")

    def save(self):
        # UIから取得する値を整理（全てのキーを明示的に作成）
        ui_data = {
            "name": self.e_name.get(),
            "status": {
                "exp": self.s_exp.get(),
                "gold": 1000,
                "weapon": self.WS.index(self.v_w.get()),
                "armor": self.AS.index(self.v_a.get()),
                "shield": 0
            },
            "items": {
                "yakuso": 6,
                "kagi": 4,
                "matsutake": self.items_vars.get("matsutake", tk.BooleanVar()).get(),
                "taiyo_ishi": self.items_vars.get("taiyo_ishi", tk.BooleanVar()).get(),
                "lora_love": self.items_vars.get("lora_love", tk.BooleanVar()).get(),
                "nijino_shizuku": self.items_vars.get("nijino_shizuku", tk.BooleanVar()).get(),
                "roto_shirusu": self.items_vars.get("roto_shirusu", tk.BooleanVar()).get(),
                "oseijo": False, # UIにないものは一旦False固定
                "gin_tategoto": False,
                "kumonowa": False
            },
            "flags": {"dragon": False, "golem": False, "death_knight": False}
        }
        JsonWriter.save_to_json(ui_data)
        messagebox.showinfo("OK", "保存完了！もう一度「呪文生成」を押してください。")

    def calc(self):
        self.res.delete(0, tk.END)
        self.res.insert(0, DQ1Calculator.generate_from_json())

if __name__ == "__main__":
    root = tk.Tk(); DQ1App(root); root.mainloop()