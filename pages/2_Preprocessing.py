import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import load_css
load_css()

st.title("⚙️ Preprocessing Data")

df = st.session_state.get('data')

if df is None:
    st.warning("⚠️ Upload data terlebih dahulu")
else:
    df = df.copy()

    st.subheader("Data Awal")
    st.dataframe(df.head())

    st.write(f"Jumlah data awal: **{df.shape[0]} baris**")
    st.write(f"Jumlah fitur: **{df.shape[1]} kolom**")

    # HAPUS DATA THALASSEMIA
    
    if 'Subtipe Anemia' in df.columns:
        df = df[df['Subtipe Anemia'] != 'thalassemia']
        df = df[df['Subtipe Anemia'] != 'thalassemia'].reset_index(drop=True)

    # KONVERSI KOMA -> TITIK

    kolom_numerik = [
        'Hb', 'HCT', 'RBC',
        'MCV', 'MCH', 'MCHC',
        'RDW - SD'
    ]

    for col in kolom_numerik:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(',', '.', regex=False)
            )

            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 3. KONVERSI NUMERIK LAIN

    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    # MISSING VALUE
  
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns

    for col in num_cols:
        if col != 'Subtipe Anemia':
            df[col] = df.groupby('Subtipe Anemia')[col].transform(
                lambda x: x.fillna(x.mean())
            )

    cat_cols = df.select_dtypes(include=['object']).columns

    for col in cat_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].mode()[0])

    # HAPUS DUPLIKAT

    df = df.drop_duplicates().reset_index(drop=True)

    # ENCODING
    
    if 'Jenis Kelamin' in df.columns:
        df['Jenis Kelamin'] = df['Jenis Kelamin'].map({
            'P': 0,
            'L': 1
        })

    if 'Subtipe Anemia' in df.columns:
        df['Subtipe Anemia'] = df['Subtipe Anemia'].map({
            'non anemia': 0,
            'anemia defisiensi besi': 1,
            'anemia penyakit kronis': 2
        })

    # SIMPAN KE SESSION

    st.session_state['df_processed'] = df

    # OUTPUT
    st.success("✅ Preprocessing selesai")

    st.subheader("Informasi Data Setelah Preprocessing")
    st.write(f"Jumlah data setelah preprocessing: **{df.shape[0]} baris**")
    st.write(f"Jumlah fitur setelah preprocessing: **{df.shape[1]} kolom**")

    st.subheader("Data Setelah Preprocessing")
    st.dataframe(df.head())

    # DISTRIBUSI KELAS

    if 'Subtipe Anemia' in df.columns:

        # Mapping label kelas
        label_kelas = {
            0: 'Non Anemia',
            1: 'Anemia Defisiensi Besi',
            2: 'Anemia Penyakit Kronis'
        }

        distribusi = (
            df['Subtipe Anemia']
            .value_counts()
            .sort_index()
        )

        nama_kelas = [
            label_kelas[i] for i in distribusi.index
        ]

        st.subheader("Distribusi Kelas")

        # Tabel distribusi
        distribusi_df = pd.DataFrame({
            'Kelas': nama_kelas,
            'Jumlah Data': distribusi.values
        })

        st.dataframe(distribusi_df)

        # Diagram batang
        fig, ax = plt.subplots(figsize=(8, 5))

        bars = ax.bar(
            nama_kelas,
            distribusi.values
        )

        