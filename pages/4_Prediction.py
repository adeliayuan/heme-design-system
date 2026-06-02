import streamlit as st
import numpy as np

from utils import load_css
load_css()

st.title("🩸 Klasifikasi Subtipe Anemia")

model = st.session_state.get('model')

if model is None:
    st.warning("⚠️ Lakukan modeling terlebih dahulu")
else:

    st.markdown("""
    Masukkan data hasil pemeriksaan hematologi untuk melakukan
    prediksi subtipe anemia menggunakan model
    **Extremely Randomized Trees**.
    """)

    # INPUT FORM
    col1, col2 = st.columns(2)

    # KOLOM KIRI
    with col1:
        nama = st.text_input("Nama Pasien")
        jk = st.selectbox(
            "Jenis Kelamin",
            ["Perempuan", "Laki-laki"]
        )

        jk_val = 0 if jk == "Perempuan" else 1

        usia = st.number_input(
            "Usia (Tahun)",
            min_value=0,
            step=1,
            format="%d"
        )

        hb = st.number_input(
            "Hemoglobin (Hb)"
        )

        hct = st.number_input(
            "Hematokrit (HCT)"
        )

    # KOLOM KANAN
    with col2:
        rbc = st.number_input(
            "Red Blood Cell Count (RBC)"
        )
        
        mcv = st.number_input(
            "Mean Corpuscular Volume (MCV)"
        )

        mch = st.number_input(
            "Mean Corpuscular Hemoglobin (MCH)"
        )

        mchc = st.number_input(
            "Mean Corpuscular Hemoglobin Concentration (MCHC)"
        )

        rdw = st.number_input(
            "Red Cell Distribution Width (RDW)"
        )

    # BUTTON

    st.markdown("")

    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

    with col_btn2:
        prediksi = st.button(
            "🔍 Mulai Prediksi",
            use_container_width=True
        )

    # PREDIKSI
    if prediksi:

        data = np.array([[
            jk_val,
            usia,
            hb,
            hct,
            rbc,
            mcv,
            mch,
            mchc,
            rdw
        ]])

        hasil = model.predict(data)

        # Label klasifikasi
        label = {
            0: "Non Anemia",
            1: "Anemia Defisiensi Besi",
            2: "Anemia Penyakit Kronis"
        }

        hasil_prediksi = label[hasil[0]]

        # OUTPUT
        st.subheader("Hasil Prediksi")

        st.success(
            f"""
            Pasien atas nama **{nama if nama else '-'}**
            terklasifikasi sebagai:

            ### {hasil_prediksi}
            """
        )

        # INTERPRETASI SINGKAT

        if hasil[0] == 0:
            st.info("""
            Hasil menunjukkan bahwa parameter hematologi pasien
            berada pada kategori non anemia.
            """)

        elif hasil[0] == 1:
            st.warning("""
            Hasil prediksi mengindikasikan kemungkinan
            **Anemia Defisiensi Besi**.
            Disarankan melakukan konsultasi lanjutan
            dengan tenaga medis.
            """)

        elif hasil[0] == 2:
            st.warning("""
            Hasil prediksi mengindikasikan kemungkinan
            **Anemia Penyakit Kronis**.
            Pemeriksaan medis lebih lanjut tetap diperlukan
            untuk memastikan diagnosis klinis.
            """)