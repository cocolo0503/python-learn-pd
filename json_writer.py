import json

class JsonWriter:
    CHAR_TABLE = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんっゃゅょ"

    @classmethod
    def save_to_json(cls, ui_data):
        name_str = str(ui_data.get("name", ""))
        name_ids = []
        
        # 4回確実に繰り返す
        for i in range(4):
            # スライス [i:i+1] は範囲外でもエラーにならず "" を返す
            char = name_str[i:i+1]
            if char and char in cls.CHAR_TABLE:
                idx = cls.CHAR_TABLE.find(char)
                name_ids.append(int(idx))
            else:
                # 文字がない、または表にない文字なら 0 (あ) に固定
                name_ids.append(0)

        data = {
            "name_ids": name_ids, # ここで必ず [int, int, int, int] になる
            "status": ui_data.get("status", {}),
            "items": ui_data.get("items", {}),
            "flags": ui_data.get("flags", {})
        }
        
        with open("data_store.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)