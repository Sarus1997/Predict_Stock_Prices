import pandas as pd
import joblib
import plotly.graph_objects as go

def visualize(data_path="data/AAPL_daily.csv", model_path="models/linear_regression.pkl"):
    """สร้างกราฟราคาจริง + เส้นแนวโน้ม Linear Regression"""
    model = joblib.load(model_path)
    df = pd.read_csv(data_path, index_col=0)
    df["close"] = df["4. close"]
    df["day"] = range(len(df))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["close"], mode='lines', name='ราคาจริง', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=model.predict(df[["day"]]), mode='lines', name='แนวโน้ม (Linear Regression)', line=dict(color='red')))
    fig.update_layout(title="📈 แนวโน้มราคาหุ้น", xaxis_title="วันที่", yaxis_title="ราคา (USD)")
    return fig, df
