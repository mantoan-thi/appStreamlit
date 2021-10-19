import app_eng
import app_qa
import streamlit as st
from datetime import datetime



PAGES = {
    "Análise de chicotes similares": app_qa,
    "Gera listas de componentes": app_eng
}
st.sidebar.title('Navegação')
selection = st.sidebar.radio("Vamos para", list(PAGES.keys()))
page = PAGES[selection]
page.app()
