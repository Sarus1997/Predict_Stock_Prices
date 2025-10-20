import pandas as pd
import joblib
import os
from sklearn.linear_model import LinearRegression

def train_model(data_path="data/AAPL_daily.csv", model_path="models/linear_regression.pkl"):
    """ฝึกโมเดล Linear Regression สำหรับพยากรณ์ราคาหุ้น"""
    df = pd.read_csv(data_path, index_col=0)
    df["close"] = df["4. close"]
    df["day"] = range(len(df))

    X = df[["day"]].values
    y = df["close"].values

    model = LinearRegression()
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, model_path)
    return model, df
