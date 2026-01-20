import json

class JsonWriter:
    CHAR_TABLE = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんっゃゅょ"

    @classmethod
    def save_to_json(cls, ui_data):
        # 名前の安全取得
        name_str = str(ui_input_name := ui_data.get("name", ""))
        name_ids = []
        for i in range(4):
            # スライス[i:i+1]は範囲外でもエラーにならず空文字を返す
            char = name_str[i:i+1]
            idx = cls.CHAR_TABLE.find(char)
            name_ids.append(idx if idx != -1 else 0)

        data = {
            "name_ids": name_ids,
            "status": ui_data.get("status", {}),
            "items": ui_data.get("items", {}),
            "flags": ui_data.get("flags", {})
        }
        
        with open("data_store.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)