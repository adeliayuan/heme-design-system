import streamlit as st

st.set_page_config(page_title="Sistem Deteksi Anemia", layout="wide")

# load css
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🩸 Sistem Klasifikasi Subtipe Anemia")

st.markdown("""
### Klasifikasi Subtipe Anemia Berbasis Machine Learning

Sistem ini dikembangkan untuk membantu proses **deteksi dini dan klasifikasi subtipe anemia**
berdasarkan parameter hasil pemeriksaan **Hematologi Lengkap (Complete Blood Count/CBC)**.

Model klasifikasi menggunakan metode **Extremely Randomized Trees (Extra Trees)**
dengan optimasi hyperparameter untuk meningkatkan performa.

---

### Klasifikasi yang Didukung
Sistem mampu mengidentifikasi beberapa kondisi berikut:

✅ **Anemia Defisiensi Besi (ADB)**  
✅ **Anemia Penyakit Kronis**  
✅ **Non Anemia**

---

### 🧪 Data Hematologi yang Digunakan
Beberapa data hasil tes laboratorium yang digunakan dalam proses klasifikasi antara lain:

- Hemoglobin (Hb)
- Hematokrit (HCT)
- Jumlah Eritrosit (RBC)
- Mean Corpuscular Volume (MCV)
- Mean Corpuscular Hemoglobin (MCH)
- Mean Corpuscular Hemoglobin Concentration (MCHC)
- Red Cell Distribution Width - Coefficient of Variation (RDW - CV)

""")

st.info("💡 Gunakan menu pada sidebar untuk memulai proses klasifikasi.")