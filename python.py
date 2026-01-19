import tkinter as tk
from tkinter import messagebox

class DQ1Cipher:
    # 64文字テーブル
    CHAR_TABLE = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんっゃゅょ"

    @classmethod
    def get_name_indices(cls, name_str):
        """名前を数値のリスト(長さ4)に変換する"""
        indices = []
        for i in range(4):
            if i < len(name_str):
                idx = cls.CHAR_TABLE.find(name_str[i])
                indices.append(int(idx) if idx != -1 else 0)
            else:
                indices.append(0) # 4文字に満たない場合は「あ」で埋める
        return indices

    @classmethod
    def encode(cls, name_str, exp_val, gold_val, item_id):
        # 1. データの型を強制
        name_indices = cls.get_name_indices(name_str)
        exp = int(exp_val)
        gold = int(gold_val)
        item = int(item_id)
        
        # 2. 15バイトのバッファを作成
        data = [0] * 15
        
        # 3. データのパッキング (DQ1の構造を模した配置)
        data[0] = name_indices[0] # 名前の1文字目をシードにする
        data[1] = (exp >> 8) & 0xFF
        data[2] = exp & 0xFF
        data[3] = (gold >> 8) & 0xFF
        data[4] = gold & 0xFF
        data[5] = item & 0x0F
        data[6] = name_indices[1]
        data[7] = name_indices[2]
        data[8] = name_indices[3]
        
        # 4. チェックサム計算 (0〜13番目の合計を64で割った余り)
        checksum = 0
        for i in range(14):
            checksum += data[i]
        data[14] = int(checksum % 64)
        
        # 5. 文字列生成
        password = ""
        seed = data[0] # 暗号化の鍵
        for i in range(20):
            # (データ + 鍵 + 位置補正) を64の範囲に収める
            # インデックスエラー防止のため % 15 を徹底
            val = (int(data[i % 15]) + seed + i) % 64
            password += cls.CHAR_TABLE[val]
            if i in [4, 9, 14]: password += " "
            
        return password

    @classmethod
    def decode(cls, password_str, name_str):
        # 呪文の掃除
        clean_pw = "".join(c for c in password_str if c in cls.CHAR_TABLE)
        if len(clean_pw) < 20: # 20文字必須
            raise ValueError("じゅもんは 20もじ 必要です")

        name_indices = cls.get_name_indices(name_str)
        seed = name_indices[0]
        
        # スクランブル解除
        decoded_data = [0] * 15
        for i in range(15):
            char_idx = cls.CHAR_TABLE.find(clean_pw[i])
            # エンコードの逆算: (文字番号 - 鍵 - 位置補正)
            val = (char_idx - seed - i) % 64
            decoded_data[i] = int(val)
        
        # チェックサム検証
        current_sum = 0
        for i in range(14):
            current_sum += decoded_data[i]
        
        if decoded_data[14] != (current_sum % 64):
            raise ValueError("じゅもんが ちがいます")

        # データの復元
        exp = (decoded_data[1] << 8) | decoded_data[2]
        gold = (decoded_data[3] << 8) | decoded_data[4]
        item_id = decoded_data[5] & 0x0F
        
        return exp, gold, item_id

class DQ1App:
    def __init__(self, root):
        self.root = root
        self.root.title("DQ1ふっかつのじゅもん復元機")
        self.root.geometry("450x500")

        # --- UI配置 ---
        tk.Label(root, text="なまえ (ひらがな4文字まで):").pack(pady=5)
        self.ent_name = tk.Entry(root, justify="center")
        self.ent_name.insert(0, "あ")
        self.ent_name.pack()

        tk.Label(root, text="EXP (経験値):").pack()
        self.scale_exp = tk.Scale(root, from_=0, to=65535, orient=tk.HORIZONTAL, length=300)
        self.scale_exp.pack()

        tk.Label(root, text="GOLD (所持金):").pack()
        self.scale_gold = tk.Scale(root, from_=0, to=65535, orient=tk.HORIZONTAL, length=300)
        self.scale_gold.pack()

        self.items = ["なし", "ぎんのたてごと", "たいようのいし", "くもったかがみ"]
        self.item_var = tk.StringVar(value=self.items[0])
        tk.OptionMenu(root, self.item_var, *self.items).pack(pady=5)

        tk.Button(root, text="▼ じゅもん作成", command=self.do_encode, bg="#ADD8E6", width=20).pack(pady=10)
        
        self.ent_pw = tk.Entry(root, font=("Courier", 12), width=30, justify="center")
        self.ent_pw.pack(pady=5)

        tk.Button(root, text="▲ じゅもん解析", command=self.do_decode, bg="#FFFACD", width=20).pack(pady=10)

    def do_encode(self):
        try:
            pw = DQ1Cipher.encode(self.ent_name.get(), self.scale_exp.get(), self.scale_gold.get(), self.items.index(self.item_var.get()))
            self.ent_pw.delete(0, tk.END)
            self.ent_pw.insert(0, pw)
        except Exception as e:
            messagebox.showerror("エラー", f"作成失敗: {e}")

    def do_decode(self):
        try:
            exp, gold, item_id = DQ1Cipher.decode(self.ent_pw.get(), self.ent_name.get())
            self.scale_exp.set(exp)
            self.scale_gold.set(gold)
            self.item_var.set(self.items[item_id])
            messagebox.showinfo("成功", "ステータスを復元しました")
        except Exception as e:
            messagebox.showwarning("エラー", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = DQ1App(root)
    root.mainloop()