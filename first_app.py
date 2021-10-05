import streamlit as st
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
import gerar_listas

#st.title('Classificação Mercadológica')
#st.subheader('**Classificação com NLP**')
#st.markdown('Este app faz a classificação mercadológica, a partir da descrição…')

area = ['Armazém','Engenharia','Qualidade','Default']
default_area = area.index('Default')
option = st.sidebar.selectbox('Selecione a Área',area,index=default_area)

# Função de entrada
def primeira_impressa():
    turno = ['bom dia','boa tarde','boa noite','Você não deveria trabalhar nesse horário!!!']
    now = datetime.now()

    if now.hour >= 5 and now.hour < 15:
        st.title('Olá '+turno[0]+', seja bem vindo!')
        st.write(datetime.today().strftime('%A, %B %d, %Y %H:%M:%S'))
    elif now.hour >= 15 and now.hour < 18:
        st.title('Olá '+turno[1]+', seja bem vindo!')
        st.write(datetime.today().strftime('%A, %B %d, %Y %H:%M:%S'))
    elif now.hour >= 18 and now.hour < 23:
        st.title('Olá '+turno[2]+', seja bem vindo!')
        st.write(datetime.today().strftime('%A, %B %d, %Y %H:%M:%S'))
    elif now.hour >= 23 and now.hour < 5:
        st.title(turno[3])
        st.write(datetime.today().strftime('%A, %B %d, %Y %H:%M:%S'))

# Título
def titulo(til):
    st.title(til)

#-------------Inicio Qualidade --------------------
def qualidade():
    st.subheader('Análise de chicotes para prever ramal a mais ou chicotes similares')
    data_new = st.file_uploader('Selecione o arquivo para análise')
    if data_new:
        df_new = pd.read_excel(data_new, sheet_name='CIRCUITO')
        left_column, right_column = st.columns(2)
        pressed_left = left_column.button('Mostra dataframe')
        pressed_right = right_column.button('Comparar chicotes')
        if pressed_left:
            df_new
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
# --------------------Fim Qualidade------------------------

#-------------Inicio Engenharia --------------------

def Eng_():
    st.subheader('Gerar listas')
    data_new = st.file_uploader('Selecione o arquivo para análise')
    if data_new:
        circuitos = pd.read_excel(data_new, sheet_name='CIRCUITO')
        tubos = pd.read_excel(data_new, sheet_name='TUBO')
        componentes = pd.read_excel(data_new, sheet_name='COMPONENTE')
        sumarizado = pd.read_excel(data_new, sheet_name='SUMARIZADO')
        ckt_column, tb_column,cp_column,sz_column,gl_column = st.columns(5)
        pressed_ckt = ckt_column.button('Circuitos')
        pressed_tb = tb_column.button('Tubos')
        pressed_cp = cp_column.button('Componentes')
        pressed_sz = sz_column.button('Sumarizado')
        pressed_gl = gl_column.button('Gerar Listas')
        if pressed_ckt:
            circuitos
        elif pressed_tb:
            tubos
        elif pressed_cp:
            componentes
        elif pressed_sz:
            sumarizado
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

# Engenharia
def selecionar_analise():
    acoe = ['Gerar listas','Comparar chicotes','Análisar comunização','Default']
    default_ix = acoe.index('Default')
    option_eng = st.selectbox('Selecione qual o tipo de análise',acoe,index=default_ix)
    if option_eng == 'Gerar listas':
        Eng_()
    elif option_eng == 'Comparar chicotes':
        'Você selecionou', option_eng
    elif option_eng == 'Análisar comunização':
        'Você selecionou', option_eng

def main():
    if option == 'Armazém':
        titulo(option)
    elif option == 'Engenharia':
        titulo(option)
        selecionar_analise()
    elif option == 'Qualidade':
        titulo(option)
        qualidade()

if __name__ == '__main__':
    main()
    primeira_impressa()