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
import gerar_listas

def app():
    with st.expander("Veja a explicação"):
        st.write('Em construção...')
    st.title('GERAR LISTAS')
    st.subheader('Listas: circuitos, tubos, componentes e sumarizado.')

    data_new = st.file_uploader('Selecione o arquivo para análise')
    st.markdown('---')
    if data_new:
        circuitos = pd.read_excel(data_new, sheet_name='CIRCUITO')
        tubos = pd.read_excel(data_new, sheet_name='TUBO')
        componentes = pd.read_excel(data_new, sheet_name='COMPONENTE')
        sumarizado = pd.read_excel(data_new, sheet_name='SUMARIZADO')
        ckt_column, tb_column,cp_column,sz_column,gl_column = st.columns(5)

        m = st.markdown("""
                    <style>
                    div.stButton > button:first-child { 
                        color: #4F8BF9;
                        border-radius: 10%;
                        backgroud-color: #00ff00;
                        height: 2em;
                        width: 7em;}
                    </style>""", unsafe_allow_html=True)

        with ckt_column:
            b = st.button('Circuitos')
            pressed_ckt = b
        
        with tb_column:
            b = st.button('Tubos')
            pressed_tb = b
        
        with cp_column: 
            b = st.button('Componentes')
            pressed_cp = b

        with sz_column:
            b = st.button('Sumarizado')
            pressed_sz = b

        with gl_column:
            b = st.button('Gerar Listas')
            pressed_gl = b
        if pressed_ckt:
            st.write(circuitos)
        elif pressed_tb:
            st.write(tubos)
        elif pressed_cp:
            st.write(componentes)
        elif pressed_sz:
            st.write(sumarizado)
        elif pressed_gl:
            ckt,tbsd,tbcd,cp,sz = gerar_listas.criar_listas(circuitos,tubos,componentes,sumarizado)
            # Create a Pandas Excel writer using XlsxWriter as the engine.
            buffer = io.BytesIO()
            st.write('Lista gerada!')
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                ckt.to_excel(writer, sheet_name='Lista de Circuitos',encoding='utf-8',index=False)
                tbsd.to_excel(writer, sheet_name='Lista de Tubos(sd)',encoding='utf-8',index=False)
                tbcd.to_excel(writer, sheet_name='Lista de Tubos(cd)', encoding='utf-8', index=False)
                cp.to_excel(writer, sheet_name='Lista de Componentes', encoding='utf-8', index=False)
                sz.to_excel(writer, sheet_name='Lista de Sumarizado', encoding='utf-8', index=False)
                writer.save()
                st.download_button(label = "Download da Lista",data=buffer,file_name = 'Lista_completa.xlsx',mime="application/vnd.ms-excel")
# --------------------Fim Eng------------------------
