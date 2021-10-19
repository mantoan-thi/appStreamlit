import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import time
import io
from datetime import datetime
from itertools import combinations
from math import factorial
import sys
import warnings
warnings.filterwarnings("ignore")
import wire_similar


def app():
    with st.expander("Veja a explicação"):
        st.write('Em construção...')
    st.title('Checagem de chicotes similares')
    st.subheader('Análise de chicotes para prever ramal a mais ou chicotes similares.')
    st.markdown('---')
    data_new = st.file_uploader('Selecione o arquivo para análise')

    if data_new:
        st.markdown('---')
        df_new = pd.read_excel(data_new, sheet_name='CIRCUITO')
        st.success('Arquivo carregado com sucesso!')
        left_column, right_column = st.columns(2)

        m = st.markdown("""
                    <style>
                    div.stButton > button:first-child { 
                        color: #4F8BF9;
                        border-radius: 10%;
                        backgroud-color: #00ff00;
                        height: 2em;
                        width: 10em;}
                    </style>""", unsafe_allow_html=True)
        with left_column:
            b = st.button('Mostra dataframe')
            pressed_left = b
        with right_column:
            b = st.button('Comparar chicotes')
            pressed_right = b
        if pressed_left:
            st.write(df_new)
        elif pressed_right:
            qa,ck,novo_dados = wire_similar.comparar(df_new)
            # Create a Pandas Excel writer using XlsxWriter as the engine.
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                qa.to_excel(writer, sheet_name='Análise de Qualidade',encoding='utf-8',index=False)
                ck.to_excel(writer, sheet_name='Análise de Checker',encoding='utf-8',index=False)
                novo_dados.to_excel(writer, sheet_name='Análise Completa', encoding='utf-8', index=False)
                writer.save()
                st.download_button(label = "Download da análise completa",data=buffer,file_name = 'Analise_completa.xlsx',mime="application/vnd.ms-excel")

