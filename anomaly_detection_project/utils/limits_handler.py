import json
import os

def load_limits(limits_path):
    """limits.json 파일을 불러와 Upper/Lower Limit 값을 반환"""
    if not os.path.exists(limits_path):
        raise FileNotFoundError(f"🚨 {limits_path} 파일이 존재하지 않습니다!")

    with open(limits_path, "r") as file:
        limits = json.load(file)
    return limits["Upper"], limits["Lower"]
