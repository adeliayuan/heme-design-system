import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_curve,
    auc
)
from sklearn.preprocessing import label_binarize
from imblearn.over_sampling import SMOTE

from model_apso import build_model
from utils import load_css

load_css()

st.title("Modeling Extremely Randomized Trees")

df = st.session_state.get('df_processed')

if df is None:
    st.warning("⚠️ Lakukan preprocessing terlebih dahulu")
else:

    # FITUR & TARGET
    X = df.iloc[:, 1:-1].values
    y = df.iloc[:, -1].values

    if st.button("Jalankan Model"):

        with st.spinner("Melakukan proses training dan evaluasi model..."):

            model = build_model()

            # CROSS VALIDATION
            skf = StratifiedKFold(
                n_splits=10,
                shuffle=True,
                random_state=42
            )
            accs, pres, recs, f1s = [], [], [], []

            for train_idx, test_idx in skf.split(X, y):
                X_train, X_test = X[train_idx], X[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]

                # TRAINING
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                # METRIK EVALUASI
                accs.append(
                    accuracy_score(y_test, y_pred)
                )
                pres.append(
                    precision_score(
                        y_test,
                        y_pred,
                        average='macro'
                    )
                )
                recs.append(
                    recall_score(
                        y_test,
                        y_pred,
                        average='macro'
                    )
                )

                f1s.append(
                    f1_score(
                        y_test,
                        y_pred,
                        average='macro'
                    )
                )

        st.success("Modeling berhasil dilakukan")

        # RATA-RATA METRIK

        acc = np.mean(accs)
        prec = np.mean(pres)
        rec = np.mean(recs)
        f1 = np.mean(f1s)

        # TAMPILKAN METRIK

        st.subheader("📊 Hasil Evaluasi Model")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Accuracy",
            f"{acc*100:.2f}%"
        )

        col2.metric(
            "Precision",
            f"{prec*100:.2f}%"
        )

        col3.metric(
            "Recall",
            f"{rec*100:.2f}%"
        )

        col4.metric(
            "F1-Score",
            f"{f1*100:.2f}%"
        )

        # INTERPRETASI METRIK

        st.markdown(f"""
        ### Interpretasi Evaluasi Model

        Model **Extremely Randomized Trees** menunjukkan performa klasifikasi yang sangat baik
        dengan nilai **akurasi sebesar {acc*100:.2f}%**. Hal ini menunjukkan bahwa model
        mampu mengklasifikasikan sebagian besar data dengan tepat.

        Nilai **precision sebesar {prec*100:.2f}%** menunjukkan bahwa prediksi yang dihasilkan
        model memiliki tingkat ketepatan yang tinggi pada masing-masing kelas.

        Nilai **recall sebesar {rec*100:.2f}%** mengindikasikan bahwa model sangat baik
        dalam mengenali seluruh kategori subtipe anemia.

        Selain itu, nilai **F1-Score sebesar {f1*100:.2f}%** menunjukkan keseimbangan yang baik
        antara precision dan recall sehingga model dinilai stabil dalam proses klasifikasi multikelas.
        """)

        # ROC CURVE MULTICLASS

        st.subheader("Kurva ROC")

        classes = np.unique(y)

        # Label kelas
        class_labels = {
            0: "Non Anemia",
            1: "Anemia Defisiensi Besi",
            2: "Anemia Penyakit Kronis"
        }

        # Binarisasi label
        y_bin = label_binarize(y, classes=classes)

        # Training full data
        model.fit(X, y)

        # Probabilitas prediksi
        y_score = model.predict_proba(X)

        fpr, tpr, roc_auc = {}, {}, {}

        for i in range(len(classes)):

            fpr[i], tpr[i], _ = roc_curve(
                y_bin[:, i],
                y_score[:, i]
            )

            roc_auc[i] = auc(
                fpr[i],
                tpr[i]
            )

        # PLOT ROC
        fig2, ax2 = plt.subplots(figsize=(5.5, 3.8))

        roc_colors = [
            '#1E88E5',
            '#43A047',
            '#FB8C00'
        ]

        for i, color in zip(range(len(classes)), roc_colors):
            ax2.plot(
                fpr[i],
                tpr[i],
                color=color,
                lw=2,
                label=f"{class_labels[i]} (AUC = {roc_auc[i]:.3f})"
            )

            ax2.fill_between(
                fpr[i],
                tpr[i],
                alpha=0.15,
                color=color
            )

        ax2.plot(
            [0, 1],
            [0, 1],
            linestyle='--',
            color='gray'
        )

        ax2.set_xlabel(
            "False Positive Rate",
            fontsize=9
        )

        ax2.set_ylabel(
            "True Positive Rate",
            fontsize=9
        )

        ax2.set_title(
            "Kurva ROC",
            fontsize=11,
            fontweight='bold'
        )

        ax2.tick_params(axis='both', labelsize=8)

        ax2.legend(
            loc='lower right',
            fontsize=7
        )

        ax2.grid(alpha=0.3)

        # TAMPILKAN DI TENGAH
        roc_col1, roc_col2, roc_col3 = st.columns([1, 2, 1])

        with roc_col2:
            st.pyplot(fig2)

        # INTERPRETASI ROC
        rata_auc = np.mean(list(roc_auc.values()))

        st.markdown(f"""
        ### Interpretasi Kurva ROC

        Berdasarkan ROC Curve multiclass, model menghasilkan rata-rata
        nilai **AUC sebesar {rata_auc:.3f}** yang menunjukkan kemampuan
        klasifikasi yang sangat baik dalam membedakan masing-masing kelas subtipe anemia.

        Kurva ROC yang mendekati sudut kiri atas menunjukkan bahwa model memiliki
        performa yang tinggi. Hal ini mengindikasikan bahwa
        model mampu membedakan data antar kelas secara optimal dengan tingkat kesalahan
        klasifikasi yang relatif rendah.
        """)
        # SAVE MODEL 
        st.session_state['model'] = model