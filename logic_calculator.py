import json

class DQ1Calculator:
    CHAR_TABLE = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんっゃゅょ"

    @classmethod
    def get_char_safe(cls, index):
        """指定したインデックスの文字を安全に取得する。範囲外なら「あ」を返す"""
        safe_idx = int(index) % 64
        # [start:end] のスライスなら絶対に Index Error は起きない
        result = cls.CHAR_TABLE[safe_idx : safe_idx + 1]
        return result if result else "あ"

    @classmethod
    def generate_from_json(cls):
        try:
            with open("data_store.json", "r", encoding="utf-8") as f:
                d = json.load(f)
        except:
            return "JSONガアリマセン"

        n_ids = d.get("name_ids", [0, 0, 0, 0])
        st = d.get("status", {})
        it = d.get("items", {})
        seed = int(n_ids[0])

        buf = [0] * 15
        buf[0] = seed
        # --- (中略: バッファ計算部分は前回と同じ) ---
        buf[1] = (int(st.get("exp", 0)) >> 8) & 0xFF
        buf[2] = int(st.get("exp", 0)) & 0xFF
        buf[3] = (int(st.get("gold", 0)) >> 8) & 0xFF
        buf[4] = int(st.get("gold", 0)) & 0xFF
        buf[5] = (int(st.get("weapon", 0)) << 5) | (int(st.get("armor", 0)) << 2)
        buf[7], buf[8], buf[9] = n_ids[1], n_ids[2], n_ids[3]
        buf[14] = sum(buf[:14]) % 64

        # 呪文生成ループ
        res_chars = []
        for i in range(20):
            # (値 + 鍵 + 位置) % 64
            val = (int(buf[i % 15]) + seed + i) % 64
            # 直接 [] で参照せず、スライス関数を使う
            res_chars.append(cls.get_char_safe(val))
        
        # 5文字ずつ結合
        c = res_chars
        return f"{''.join(c[0:5])} {''.join(c[5:10])} {''.join(c[10:15])} {''.join(c[15:20])}"