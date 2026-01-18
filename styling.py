import streamlit as st

def apply_page_config(page_title: str, page_icon: str):
    """Apply consistent page configuration and styling across all pages"""
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout="wide")
    
    st.markdown("""
        <style>
            /* Slim sidebar */
            [data-testid="stSidebar"] {
                min-width: 200px;
                max-width: 200px;
            }
            
            [data-testid="stSidebar"] > div:first-child {
                padding-top: 1rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
            
            /* Compact navigation */
            [data-testid="stSidebarNav"] {
                padding-top: 1rem;
            }
            
            [data-testid="stSidebarNav"] ul {
                padding-left: 0.5rem;
            }
            
            /* Hide Streamlit branding */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
            }
        </style>
        """, unsafe_allow_html=True)