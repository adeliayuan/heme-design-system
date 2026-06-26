import streamlit as st

st.set_page_config(
    page_title="Sistem Klasifikasi Subtipe Anemia",
    layout="wide"
)

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Judul
st.markdown(
    """
    <h2 style='text-align:center; margin-bottom:20px;'>
    Sistem Klasifikasi Subtipe Anemia
    </h2>
    """,
    unsafe_allow_html=True
)

# Deskripsi
st.markdown(
    """
    <div class="description-box">
        Sistem ini dikembangkan untuk membantu proses identifikasi dini dan
        klasifikasi subtipe anemia berdasarkan hasil pemeriksaan
        Hematologi Lengkap (Complete Blood Count/CBC).<br>
        Model klasifikasi menggunakan metode Extremely Randomized Trees (Extra Trees).
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# Dua kolom
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">Klasifikasi yang Didukung</div>
        <p class="card-text">☑ Anemia Defisiensi Besi (ADB)</p>
        <p class="card-text">☑ Anemia Penyakit Kronis</p>
        <p class="card-text">☑ Non Anemia</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">Data Hematologi yang Digunakan</div>
        <p class="card-text">• Hemoglobin (Hb)</p>
        <p class="card-text">• Hematokrit (HCT)</p>
        <p class="card-text">• Jumlah Eritrosit (RBC)</p>
        <p class="card-text">• Mean Corpuscular Volume (MCV)</p>
        <p class="card-text">• Mean Corpuscular Hemoglobin (MCH)</p>
        <p class="card-text">• Mean Corpuscular Hemoglobin Concentration (MCHC)</p>
        <p class="card-text">• Red Cell Distribution Width CV (RDW-CV)</p>
    </div>
    """, unsafe_allow_html=True)

# Info bawah
st.markdown(
    """
    <div class="info-box">
        💡 Gunakan menu pada sidebar untuk memulai proses klasifikasi.
    </div>
    """,
    unsafe_allow_html=True
)
