def load_css():
    with open("style.css") as f:
        import streamlit as st
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)