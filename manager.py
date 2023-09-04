import json

from typing import Dict, Any

def read_json() -> Dict[str, Any]:
    try:
        with open("token.json", "r", encoding="UTF-8") as fp:
            json_data = json.load(fp)

    except Exception as e:
        print(e)

    return json_data