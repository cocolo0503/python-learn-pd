import json

class DQ1Calculator:
    CHAR_TABLE = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんっゃゅょ"

    @classmethod
    def get_char_safe(cls, index):
        """範囲外参照を物理的に防ぐ"""
        safe_idx = int(index) % 64
        # スライス参照によりIndexErrorを完全に回避
        return cls.CHAR_TABLE[safe_idx:safe_idx+1] or "あ"

    @classmethod
    def generate_from_json(cls):
        try:
            with open("data_store.json", "r", encoding="utf-8") as f:
                d = json.load(f)
        except: return "保存ボタンを先に押してください"

        n = d.get("name_ids", [0, 0, 0, 0])
        st = d.get("status", {})
        it = d.get("items", {})
        seed = n[0]

        buf = [0] * 15
        buf[0] = seed
        buf[1] = (int(st.get("exp",0)) >> 8) & 0xFF
        buf[2] = int(st.get("exp",0)) & 0xFF
        buf[3] = (int(st.get("gold",0)) >> 8) & 0xFF
        buf[4] = int(st.get("gold",0)) & 0xFF
        buf[5] = (int(st.get("weapon",0)) << 5) | (int(st.get("armor",0)) << 2) | int(st.get("shield",0))
        buf[6] = (int(it.get("yakuso",0)) << 4) | int(it.get("kagi",0))
        buf[7], buf[8], buf[9] = n[1], n[2], n[3]

        # 重要アイテムフラグ
        f1 = 0
        if it.get("taiyo_ishi"):   f1 |= (1 << 0)
        if it.get("gin_tategoto"): f1 |= (1 << 1)
        if it.get("lora_love"):    f1 |= (1 << 2)
        if it.get("roto_shirusu"): f1 |= (1 << 3)
        if it.get("nijino_shizuku"): f1 |= (1 << 4)
        buf[10] = f1
        buf[14] = sum(buf[:14]) % 64

        # 呪文生成
        res = []
        for i in range(20):
            val = (buf[i % 15] + seed + i) % 64
            res.append(cls.get_char_safe(val))
        
        c = res
        return f"{''.join(c[0:5])} {''.join(c[5:10])} {''.join(c[10:15])} {''.join(c[15:20])}"