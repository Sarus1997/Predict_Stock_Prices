import joblib
import pandas as pd

def predict_next_day(model_path="models/linear_regression.pkl", data_path="data/AAPL_daily.csv"):
    """ทำนายราคาหุ้นวันถัดไป"""
    model = joblib.load(model_path)
    df = pd.read_csv(data_path, index_col=0)
    df["close"] = df["4. close"]
    df["day"] = range(len(df))

    next_day = [[df["day"].iloc[-1] + 1]]
    prediction = model.predict(next_day)[0]
    return prediction
