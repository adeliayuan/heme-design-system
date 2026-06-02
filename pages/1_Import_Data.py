import streamlit as st
import pandas as pd
from utils import load_css
load_css()

st.title("Import Data")

file = st.file_uploader("Upload CSV atau Excel", type=["csv","xlsx"])

if file:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.session_state['data'] = df
    st.success("Data berhasil diupload")
    st.dataframe(df.head())