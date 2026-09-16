import streamlit as st
import pandas as pd
import plotly.express as px

st.title("⚙ Forecast Model Insights")

data = {
"Model":["Auto ARIMA","Prophet","XGBoost"],
"MAPE":[3.1,2.8,3.4],
"RMSE":[2.2,1.9,2.5]
}

df = pd.DataFrame(data)

fig = px.bar(
    df,
    x="Model",
    y="MAPE",
    title="Model Accuracy Comparison"
)

st.plotly_chart(fig,use_container_width=True)