import streamlit as st
from src.fetch_data import fetch_stock_data
from src.train_model import train_model
from src.predict_next_day import predict_next_day
from src.visualize import visualize
from src.symbols_loader import load_symbols

# --- Page Config ---
st.set_page_config(page_title="🌎 Global Stock Prediction Dashboard", layout="wide")
st.title("📈 Global Stock Market Trend & Forecast Dashboard")

# --- Load Symbols ---
symbols_df = load_symbols("data/symbols_global.csv")

# --- Custom CSS for Sidebar Footer ---
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] .sidebar-content {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100vh;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar Controls ---
with st.sidebar:
    # Top Controls
    st.header("🌍 Market Selection")

    region_list = sorted(symbols_df["region"].unique())
    region = st.selectbox("🌐 Select Region", region_list)

    country_list = sorted(symbols_df[symbols_df["region"] == region]["country"].unique())
    country = st.selectbox("🏳️ Select Country", country_list)

    symbol_list = symbols_df[
        (symbols_df["region"] == region) & (symbols_df["country"] == country)
    ]["symbol"].unique()
    symbol = st.selectbox("💹 Select Stock Symbol", symbol_list)

    st.markdown("---")

    fetch_button = st.button("Fetch & Predict")

    # Footer
    st.markdown(
        """
        <div style="font-size:12px; margin-top:10px;">
        💡 Data powered by Alpha Vantage<br>
        💡 Get Key API Alpha Vantage: <a href="https://www.alphavantage.co/support/#api-key" target="_blank">Click Here</a>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Main Logic ---
if fetch_button:
    try:
        st.info(f"📡 Fetching {symbol} data from Alpha Vantage...")
        df = fetch_stock_data(symbol=symbol, output_path=f"data/{symbol}_daily.csv")

        st.info("🤖 Training model...")
        model, df = train_model(data_path=f"data/{symbol}_daily.csv", model_path="models/linear_regression.pkl")

        st.info("🔮 Predicting next day price...")
        prediction = predict_next_day(model_path="models/linear_regression.pkl", data_path=f"data/{symbol}_daily.csv")

        st.success(f"Next predicted closing price for {symbol}: **{prediction:.2f} USD**")

        fig, df = visualize(data_path=f"data/{symbol}_daily.csv", model_path="models/linear_regression.pkl")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("View Recent Data"):
            st.dataframe(df.tail(10))

    except Exception as e:
        st.error(f"Error: {e}")
