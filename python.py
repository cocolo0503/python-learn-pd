# import tkinter as tk
# from tkinter import messagebox

# class DQ1Cipher:
#     CHAR_TABLE = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんっゃゅょ"

#     @classmethod
#     def encode(cls, name, exp, gold, w, a, s, y, k, v_id):
#         # 名前の各文字を安全に取得（スライスなら空でもエラーにならない）
#         n1 = name[0:1] if name[0:1] else "あ"
#         n2 = name[1:2] if name[1:2] else "あ"
#         n3 = name[2:3] if name[2:3] else "あ"
#         n4 = name[3:4] if name[3:4] else "あ"

#         def get_idx(c):
#             i = cls.CHAR_TABLE.find(c)
#             return int(i) if i != -1 else 0

#         # すべてを確実に数値(int)にする
#         name_vals = [get_idx(n1), get_idx(n2), get_idx(n3), get_idx(n4)]
#         seed = int(name_vals[0])
        
#         # 15要素の数値リストを作成
#         data = [0] * 15
#         data[0] = (seed + v_id) % 64
#         data[1] = (int(exp) >> 8) & 0xFF
#         data[2] = int(exp) & 0xFF
#         data[3] = (int(gold) >> 8) & 0xFF
#         data[4] = int(gold) & 0xFF
#         data[5] = ((int(w) & 7) << 5) | ((int(a) & 7) << 2) | (int(s) & 3)
#         data[6] = ((int(y) & 15) << 4) | (int(k) & 15)
#         data[7], data[8], data[9] = name_vals[1], name_vals[2], name_vals[3]

#         # チェックサム
#         data[14] = sum(data[:14]) % 64
        
#         # 文字列生成
#         pw = ""
#         for i in range(20):
#             d_val = int(data[i % 15])
#             char_idx = (d_val + seed + i + v_id) % 64
#             pw += cls.CHAR_TABLE[char_idx]
#             if i in [4, 9, 14]: pw += " "
#         return pw

# class DQ1App:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("DQ1ふっかつメーカー")
#         self.root.geometry("450x600")

#         # 設定データ
#         self.WS = ["なし","たけざお","こんぼう","どうのつるぎ","てつのおの","はがねのつるぎ","ほのおのつるぎ","ロトのつるぎ"]
#         self.AS = ["なし","ぬののふく","かわのふく","くさりかたびら","てつのよろい","はがねのよろい","まほうのよろい","ロトのよろい"]

#         # --- UI構築 ---
#         f = tk.Frame(root, padx=20, pady=10); f.pack()
        
#         tk.Label(f, text="なまえ:").grid(row=0, column=0)
#         self.e_name = tk.Entry(f); self.e_name.insert(0, "ろと"); self.e_name.grid(row=0, column=1)

#         self.s_exp = self._sc(f, "EXP (経験値)", 65535, 1)
#         self.s_gold = self._sc(f, "GOLD (所持金)", 65535, 2)
        
#         tk.Label(f, text="武器:").grid(row=3, column=0)
#         self.v_w = tk.StringVar(value=self.WS[0])
#         tk.OptionMenu(f, self.v_w, *self.WS).grid(row=3, column=1)

#         tk.Label(f, text="鎧:").grid(row=4, column=0)
#         self.v_a = tk.StringVar(value=self.AS[0])
#         tk.OptionMenu(f, self.v_a, *self.AS).grid(row=4, column=1)

#         tk.Button(root, text="じゅもんを つくる", command=self.generate, 
#                   bg="#0055ff", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

#         self.res = tk.Text(root, height=10, width=40, font=("MS Gothic", 11), bg="black", fg="#00ff00")
#         self.res.pack(pady=10)

#     def _sc(self, p, t, m, r):
#         tk.Label(p, text=t).grid(row=r, column=0)
#         s = tk.Scale(p, from_=0, to=m, orient="horizontal", length=200)
#         s.grid(row=r, column=1); return s

#     def generate(self):
#         try:
#             name = str(self.e_name.get())
#             exp = int(self.s_exp.get())
#             gold = int(self.s_gold.get())
#             w_idx = self.WS.index(self.v_w.get())
#             a_idx = self.AS.index(self.v_a.get())
            
#             self.res.delete("1.0", tk.END)
#             for i in range(8):
#                 pw = DQ1Cipher.encode(name, exp, gold, w_idx, a_idx, 0, 5, 1, i)
#                 self.res.insert(tk.END, f"{i+1}: {pw}\n")
#         except Exception as e:
#             messagebox.showerror("エラー", f"予期せぬエラー: {e}")

# if __name__ == "__main__":
#     root = tk.Tk(); app = DQ1App(root); root.mainloop()