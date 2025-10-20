import pandas as pd

def load_symbols(path="data/symbols_global.csv"):
    """โหลดรายการหุ้นทั้งหมดทั่วโลก"""
    df = pd.read_csv(path, on_bad_lines='skip')  # ข้ามแถวที่ผิดพลาด
    return df
