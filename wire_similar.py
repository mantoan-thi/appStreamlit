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

# Selecionado as colunas
def discriminada(df_ckt):
    df = df_ckt[['PROD_TERM', 'OT', 'OT_DISCRIMINADA', 'CIRC_ESQ', 'CIR_DIR', 'TIPO',
                 'BITOLA', 'COR', 'COMP', 'COD_OP_01_ESQ', 'TERMINAL_ESQ', 'ACC_ESQ_1',
                 'COD_OP_01_DIR', 'TERMINAL_DIR', 'ACC_DIR_1', 'SOLDA']].copy()

    # Gerando lista de Part number, sem duplicação
    lista_de_part_number = set(df['PROD_TERM'])

    # Removendo Ot's discrininadas
    indexNames = df[df['OT_DISCRIMINADA'] == 'SIM'].index
    df.drop(indexNames, inplace=True)
    df.drop(columns=['OT_DISCRIMINADA'], axis=1, inplace=True)
    return lista_de_part_number, df

def analisar(list_, tol):
    contar1 = 0
    contar2 = 0
    list_comp = list_.copy()
    list_comp['Delta'] = 0
    list_comp['COD_OP_01_ESQ'] = list_comp['COD_OP_01_ESQ'].apply(lambda x: 0 if x != 'U' else 'U')
    list_comp['COD_OP_01_DIR'] = list_comp['COD_OP_01_DIR'].apply(lambda x: 0 if x != 'U' else 'U')
    while contar1 < list_comp.shape[0]:
        contar2 = contar1 + 1
        while contar2 < list_comp.shape[0]:
            if list_comp['PROD_TERM'].iloc[contar1] != list_comp['PROD_TERM'].iloc[contar2]:
                # Tipo+bit+cor
                tipoA = list_comp['TIPO'].iloc[contar1] + list_comp['BITOLA'].iloc[contar1] + list_comp['COR'].iloc[
                    contar1]
                tipoB = list_comp['TIPO'].iloc[contar2] + list_comp['BITOLA'].iloc[contar2] + list_comp['COR'].iloc[
                    contar2]
                TAE = str(list_comp['COD_OP_01_ESQ'].iloc[contar1]) + str(
                    list_comp['TERMINAL_ESQ'].iloc[contar1]) + str(list_comp['ACC_ESQ_1'].iloc[contar1])
                TAD = str(list_comp['COD_OP_01_DIR'].iloc[contar1]) + str(
                    list_comp['TERMINAL_DIR'].iloc[contar1]) + str(list_comp['ACC_DIR_1'].iloc[contar1])
                TBE = str(list_comp['COD_OP_01_ESQ'].iloc[contar2]) + str(
                    list_comp['TERMINAL_ESQ'].iloc[contar2]) + str(list_comp['ACC_ESQ_1'].iloc[contar2])
                TBD = str(list_comp['COD_OP_01_DIR'].iloc[contar2]) + str(
                    list_comp['TERMINAL_DIR'].iloc[contar2]) + str(list_comp['ACC_DIR_1'].iloc[contar2])
                COMPA = int(list_comp['COMP'].iloc[contar1])
                COMPB = int(list_comp['COMP'].iloc[contar2])
                dif = abs(COMPA - COMPB)
                JTA = str(list_comp['SOLDA'].iloc[contar1])[0]
                JTB = str(list_comp['SOLDA'].iloc[contar2])[0]
                if tipoA == tipoB:  # Comparando Tipo,Bit e cor
                    if COMPA == COMPB or dif < tol:  # Checando dimensional
                        if TAE == TBE and TAD == TBD:  # Terminais
                            list_comp['Delta'].iloc[contar1] = 'Comum'
                            list_comp['Delta'].iloc[contar2] = 'Comum'
                        if TAE == TBD and TAD == TBE:  # Terminais
                            list_comp['Delta'].iloc[contar1] = 'Comum'
                            list_comp['Delta'].iloc[contar2] = 'Comum'

            contar2 += 1
        contar1 += 1
        contar2 = 0
        list_comp['Delta'].loc[list_comp['Delta'] == 0] = 'DIF'
        nova_lista = list_.copy()
        nova_lista['Delta'] = list_comp['Delta']
        nova_lista.fillna(0, inplace=True)
        nova_lista.sort_values(by=['OT'], ascending=True, inplace=True)
    return nova_lista

# Contagem de saídas
def contar_saidas(x, nova_lista3):
    valor = 0
    for e in nova_lista3['Saida_esq']:
        if e == x:
            valor += 1
    for d in nova_lista3['Saida_dir']:
        if d == x:
            valor += 1
    return valor

# Contagem de ligações
def contar_lig(e, d, nova_lista3):
    contador = 0
    valor = 0
    while contador < nova_lista3.shape[0]:
        if nova_lista3['Saida_esq'].iloc[contador] == e and nova_lista3['Saida_dir'].iloc[contador] == d:
            valor += 1
        if nova_lista3['Saida_esq'].iloc[contador] == d and nova_lista3['Saida_dir'].iloc[contador] == e:
            valor += 1
        contador += 1

    return valor

# Retorna o percentual de similaridade
def perct(l, c):
    if l == 0:
        new_l = 0
    else:
        new_l = l / c
    return '{:.0%}'.format(new_l)

# Calcula a quantidade de cobinações
def calculate_combinations(n, r):
    return factorial(n) // factorial(r) // factorial(n - r)

def processar(new_df_circuitos):
    # separa as saídas dos circuitos
    new_df_circuitos['Saida_esq'] = new_df_circuitos['CIRC_ESQ'].str[-3:]
    new_df_circuitos['Saida_dir'] = new_df_circuitos['CIR_DIR'].str[-3:]

    # Calcula a quantidade de saídas
    new_df_circuitos['qtde_sds_esq'] = new_df_circuitos.apply(lambda x: contar_saidas(x.Saida_esq, new_df_circuitos),
                                                              axis=1)
    new_df_circuitos['qtde_sds_dir'] = new_df_circuitos.apply(lambda x: contar_saidas(x.Saida_dir, new_df_circuitos),
                                                              axis=1)

    # Calcula a quantidade de ligações
    new_df_circuitos['qtde_lig_esq'] = new_df_circuitos.apply(lambda x: contar_lig(x['Saida_esq'], x['Saida_dir'], new_df_circuitos), axis=1)
    new_df_circuitos['qtde_lig_dir'] = new_df_circuitos['qtde_lig_esq']

    # Calcula o percetual de ligações
    new_df_circuitos['Perct_lig_esq'] = new_df_circuitos.apply(lambda x: perct(x['qtde_lig_esq'], x['qtde_sds_esq']),
                                                               axis=1)
    new_df_circuitos['Perct_lig_dir'] = new_df_circuitos.apply(lambda x: perct(x['qtde_lig_dir'], x['qtde_sds_dir']),
                                                               axis=1)
    return new_df_circuitos

def risk(simil, A, B):
    if simil == 1:
        return 'Alto'
    else:
        if (A + B) == 1:
            return 'Moderado'
        else:
            return 'Baixo'

def ordenar(x):
    if x == 'Alto':
        return 1
    else:
        if x == 'Moderado':
            return 2
        else:
            return 3

# Barra de status simples
def printProgressBar(i, max, postText):
    n_bar = 10  # size of progress bar
    j = i / max
    sys.stdout.write('\r')
    sys.stdout.write(f"{postText} [{'=' * int(n_bar * j):{n_bar}s}] {int(100 * j)}%")
    sys.stdout.flush()

# Critério de checker
def checker(nE, nD, sE, sD):
    detect = []
    det = ''
    if nE == 1:
        detect.append(sE)
    if nD == 1:
        detect.append(sD)
    if len(detect) > 1:
        det = 'Adicionar pino de presença para as saídas' + str(detect)
    else:
        det = 'Adicionar pino de presença para na saída' + str(detect)
    if not detect:
        det = ''
    return det

# Testes de qualidade
def QA(nA, nB, sA, sB, pA, pB):
    sdsA = []
    sdsB = []
    pnA = []
    pnB = []
    qa = ''
    if nA != 0:
        # pnA.append(pA)
        # pnB.append(pB)
        sdsA.append(sA)
    if nB != 0:
        # pnA.append(pA)
        # pnB.append(pB)
        sdsB.append(sB)
    if sdsA != []:
        if len(sdsA) > 1:
            qa = 'Testar PN ' + str(pA) + ' no lugar do PN ' + str(pB) + ' não direncionar as saídas ' + str(sdsA)
        else:
            qa = 'Testar PN ' + str(pA) + ' no lugar do PN ' + str(pB) + ' não direncionar a saída ' + str(sdsA)
    else:
        if sdsB != []:
            if len(sdsB) > 1:
                qa = 'Testar PN ' + str(pB) + ' no lugar do PN ' + str(pA) + ' não direncionar as saídas ' + str(sdsB)
            else:
                qa = 'Testar PN ' + str(pB) + ' no lugar do PN ' + str(pA) + ' não direncionar a saída ' + str(sdsB)
        else:
            qa = 'Sem testes'
    return qa

# Formata o resultado
def result(resultado):
    New_resultado = pd.DataFrame(resultado, columns=['Similaridade', 'Part_numberA', 'Núm_saídas_diferentesA',
                                                     'Saídas_exclusivasA', 'De_Para_A', 'Núm_CktA', 'Part_numberB',
                                                     'Núm_saídas_diferentesB', 'Saídas_exclusivasB', 'De_Para_B',
                                                     'Núm_CktB'])
    New_resultado['Risk2'] = New_resultado['Núm_saídas_diferentesA'] + New_resultado['Núm_saídas_diferentesB']
    New_resultado['Risk'] = New_resultado.apply(
        lambda x: risk(x['Similaridade'], x['Núm_saídas_diferentesA'], x['Núm_saídas_diferentesB']), axis=1)
    New_resultado['Risk3'] = New_resultado['Risk'].apply(lambda x: ordenar(x))
    New_resultado.sort_values(by=['Risk3'], inplace=True)
    New_resultado.drop(columns=['Risk2', 'Risk3'], inplace=True)
    New_resultado.style.format({'Similaridade': "{:.2%}"})
    New_resultado.reset_index(drop=True, inplace=True)
    New_resultado = New_resultado.reindex(columns=['Risk', 'Similaridade', 'Part_numberA', 'Núm_saídas_diferentesA',
                                                   'Saídas_exclusivasA', 'De_Para_A', 'Núm_CktA', 'Part_numberB',
                                                   'Núm_saídas_diferentesB', 'Saídas_exclusivasB', 'De_Para_B',
                                                   'Núm_CktB', 'Checker'])
    New_resultado['Checker'] = New_resultado.apply(
        lambda x: checker(x.Núm_saídas_diferentesA, x.Núm_saídas_diferentesB, x.Saídas_exclusivasA,
                          x.Saídas_exclusivasB), axis=1)
    New_resultado['QA'] = New_resultado.apply(
        lambda x: QA(x.Núm_saídas_diferentesA, x.Núm_saídas_diferentesB, x.Saídas_exclusivasA, x.Saídas_exclusivasB,
                     x.Part_numberA, x.Part_numberB), axis=1)
    return New_resultado

def comparar(dataframe):
    # Calcular a quantidade de comparações
    lista_de_part_number, df = discriminada(dataframe)
    lista_de_comparacao = []
    Total = 0
    n_comb = 0
    resultado = []
    n = calculate_combinations(len(lista_de_part_number), 2)
    st.write('Quantidade de Part numbers: '+str(len(lista_de_part_number)))
    st.write('Quantidade de comparações: '+str(n))
    # Gera todas as combinações
    n_comb = 0
    latest_iteration = st.empty()
    bar = st.progress(0)
    for i in combinations(lista_de_part_number, 2):
        latest_iteration.text(f'{((n_comb*100)//n) + 1}% concluído!')
        bar.progress(((n_comb*100)//n) + 1)
        pnA = i[0]
        pnB = i[1]
        # print('Num: ',n_comb,' Comparativo: ',pnA,' vs ',pnB,'// % Concluídos: ','{:.2%}'.format(n_comb/n), end='\r', flush=True)
        nova_lista = analisar(df[(df['PROD_TERM'] == i[0]) | (df['PROD_TERM'] == i[1])], 50)
        nova_lista['Total'] = 1
        nova_lista['Delta'].loc[(nova_lista['Delta'] == 'DIF') & (nova_lista['PROD_TERM'] == pnA)] = 'Adicionar'
        nova_lista['Delta'].loc[(nova_lista['Delta'] == 'DIF') & (nova_lista['PROD_TERM'] == pnB)] = 'Excluir'

        nova_lista1 = nova_lista.copy()
        nova_lista2 = nova_lista.copy()
        nova_lista3 = pd.pivot_table(nova_lista1, index=['OT', 'CIRC_ESQ', 'CIR_DIR', 'TIPO', 'BITOLA', 'COR',
                                                         'COMP', 'COD_OP_01_ESQ', 'TERMINAL_ESQ', 'ACC_ESQ_1',
                                                         'COD_OP_01_DIR',
                                                         'TERMINAL_DIR', 'ACC_DIR_1', 'SOLDA', 'Delta'],
                                     values=["Total"], columns=['PROD_TERM'], aggfunc=[np.sum], fill_value=0, )

        nova_lista3.columns = [col[2] for col in nova_lista3.columns]
        nova_lista3.reset_index(inplace=True)
        cmn = list(nova_lista3['Delta'])
        if 'Comum' in cmn:
            cm = nova_lista3['Delta'].value_counts()['Comum']
        else:
             cm = 0
        perc = float(cm / nova_lista3.shape[0])
        nova_lista3[pnA] = nova_lista3[pnA].apply(lambda x: pnA if x == 1 else 0)
        nova_lista3[pnB] = nova_lista3[pnB].apply(lambda x: pnB if x == 1 else 0)
        nova_lista4 = processar(nova_lista3)
        cont = 0
        sesq_ant = 0
        sdir_ant = 0
        qtde_saidaA = 0
        qtde_saidaB = 0
        lista_de_saidasA = []
        lista2_de_saidasA = []
        lista_de_saidasB = []
        lista2_de_saidasB = []
        qtde_ckt_A = []
        qtde_ckt_B = []
        while cont < nova_lista4.shape[0]:
            if nova_lista4['Delta'][cont] != 'Comum' and nova_lista4['Perct_lig_esq'][cont] == '100%':
                if nova_lista4[pnA][cont] != 0:
                    if sesq_ant != nova_lista4['Saida_esq'][cont] and sdir_ant != nova_lista4['Saida_dir'][cont]:
                        sesq_ant = nova_lista4['Saida_esq'][cont]
                        sdir_ant = nova_lista4['Saida_dir'][cont]
                        qtde_saidaA += 1
                        lista_de_saidasA.append(nova_lista4['Saida_esq'][cont])
                        lista2_de_saidasA.append([nova_lista4['Saida_esq'][cont], nova_lista4['Saida_dir'][cont]])
                        qtde_ckt_A.append(nova_lista4['qtde_sds_esq'][cont])
                else:
                    if sesq_ant != nova_lista4['Saida_esq'][cont] and sdir_ant != nova_lista4['Saida_dir'][cont]:
                        sdir_ant = nova_lista4['Saida_dir'][cont]
                        sesq_ant = nova_lista4['Saida_esq'][cont]
                        qtde_saidaB += 1
                        lista_de_saidasB.append(nova_lista4['Saida_esq'][cont])
                        lista2_de_saidasB.append([nova_lista4['Saida_esq'][cont], nova_lista4['Saida_dir'][cont]])
                        qtde_ckt_B.append(nova_lista4['qtde_sds_esq'][cont])

            if nova_lista4['Delta'][cont] != 'Comum' and nova_lista4['Perct_lig_dir'][cont] == '100%':
                if nova_lista4[pnA][cont] != 0:
                    if sdir_ant != nova_lista4['Saida_dir'][cont] and sesq_ant != nova_lista4['Saida_esq'][cont]:
                        sesq_ant = nova_lista4['Saida_esq'][cont]
                        sdir_ant = nova_lista4['Saida_dir'][cont]
                        qtde_saidaA += 1
                        lista_de_saidasA.append(nova_lista4['Saida_dir'][cont])
                        lista2_de_saidasA.append([nova_lista4['Saida_dir'][cont], nova_lista4['Saida_esq'][cont]])
                        qtde_ckt_A.append(nova_lista4['qtde_sds_dir'][cont])
                else:
                    if sdir_ant != nova_lista4['Saida_dir'][cont] and sesq_ant != nova_lista4['Saida_esq'][cont]:
                        sesq_ant = nova_lista4['Saida_esq'][cont]
                        sdir_ant = nova_lista4['Saida_dir'][cont]
                        qtde_saidaB += 1
                        lista_de_saidasB.append(nova_lista4['Saida_dir'][cont])
                        lista2_de_saidasB.append([nova_lista4['Saida_dir'][cont], nova_lista4['Saida_esq'][cont]])
                        qtde_ckt_B.append(nova_lista4['qtde_sds_dir'][cont])
            cont += 1
        n_comb += 1
        resultado.append(
            [perc, pnA, qtde_saidaA, ', '.join(lista_de_saidasA), ', '.join(map(str,lista2_de_saidasA)),', '.join(map(str,qtde_ckt_A)), pnB, qtde_saidaB,
             ', '.join(lista_de_saidasB), ', '.join(map(str,lista2_de_saidasB)), ', '.join(map(str,qtde_ckt_B))])
    new_data = result(result(resultado))
    lista_QA = pd.DataFrame(set(result(resultado)['QA']), columns=['Testes_QA'])
    lista_CK = pd.DataFrame(set(result(resultado)['Checker']), columns=['PPC_Checker'])
    return lista_QA, lista_CK, new_data
