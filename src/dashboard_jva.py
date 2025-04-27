import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="JVA Values", layout='wide')
st.title("Example of Dashboard")
st.write("Present values from the JVA company")

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
file_path = os.path.join(project_root, 'data', 'jva_daily_raw.csv')
df_cotacoes = pd.read_csv(file_path)


st.write("Preview the head of the Dataframe")
st.dataframe(df_cotacoes.head())
columns_to_plot = ['1. open', '2. high', '3. low', '4. close']

chart_data = df_cotacoes.set_index('date')[columns_to_plot]
st.line_chart(chart_data)