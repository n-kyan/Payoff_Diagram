import streamlit as st


def apply_page_config(page_title: str):
    
    st.set_page_config(
        page_title=page_title,
        page_icon="Serpinski-Tri.webp",
        layout="wide"
    )