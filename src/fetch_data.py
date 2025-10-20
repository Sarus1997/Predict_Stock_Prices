import os
import requests
import pandas as pd
from dotenv import load_dotenv

# โหลดค่า API Key จากไฟล์ .env
load_dotenv()
API_KEY = os.getenv("ALPHAVANTAGE_KEY")

def fetch_stock_data(symbol="AAPL", output_path="data/AAPL_daily.csv"):
    """📡 ดึงข้อมูลราคาหุ้นรายวันจาก Alpha Vantage"""
    if not API_KEY:
        raise ValueError("❌ ไม่พบ ALPHAVANTAGE_KEY ในไฟล์ .env")

    # สร้างโฟลเดอร์ถ้ายังไม่มี
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    url = (
        f"https://www.alphavantage.co/query?"
        f"function=TIME_SERIES_DAILY&symbol={symbol}"
        f"&outputsize=compact&apikey={API_KEY}"
    )

    print(f"🔎 กำลังดึงข้อมูลหุ้น {symbol} ...")
    response = requests.get(url)
    
    # ตรวจสอบสถานะการเชื่อมต่อ
    if response.status_code != 200:
        raise ConnectionError(f"🌐 ไม่สามารถเชื่อมต่อ API ได้ (Status: {response.status_code})")

    data = response.json()

    # ตรวจสอบกรณีเกิด Error จาก API
    if "Error Message" in data:
        raise Exception(f"❌ Symbol '{symbol}' ไม่ถูกต้อง หรือไม่รองรับใน Alpha Vantage")
    elif "Note" in data:
        raise Exception("⚠️ API ถูกเรียกเกินโควต้าที่อนุญาต (โปรดลองใหม่ใน 1 นาที)")
    elif "Time Series (Daily)" not in data:
        raise Exception("❌ ไม่พบข้อมูลหุ้นจาก API (ตรวจสอบ symbol หรือ API Key)")

    # แปลงข้อมูลเป็น DataFrame
    df = pd.DataFrame(data["Time Series (Daily)"]).T
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # บันทึกข้อมูลลงไฟล์ CSV
    df.to_csv(output_path)
    print(f"✅ บันทึกข้อมูล {symbol} ลงไฟล์: {output_path}")

    return df
