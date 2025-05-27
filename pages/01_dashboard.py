import streamlit as st
import pandas as pd

st.title("데이터 대시보드 예시")
df = pd.read_csv("data/sample.csv")
st.dataframe(df)
st.line_chart(df)
