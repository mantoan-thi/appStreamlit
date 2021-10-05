import pandas as pd
import numpy as np

def criar_listas(ckt,tb,cp,sz):
  ckt_new = ckt[['PROD_TERM', 'OT', 'OT_DISCRIMINADA', 'CIRC_ESQ','CIR_DIR', 'TIPO',
                                  'BITOLA', 'COR', 'COMP', 'COD_OP_01_ESQ', 'TERMINAL_ESQ','ACC_ESQ_1',
                                  'COD_OP_01_DIR','TERMINAL_DIR','ACC_DIR_1','SOLDA']].copy()
  # Removendo Ot's discrininadas
  indexNames = ckt_new[ ckt_new['OT_DISCRIMINADA'] == 'SIM' ].index
  ckt_new.drop(indexNames , inplace=True)
  ckt_new.drop(columns=['OT_DISCRIMINADA'],axis=1,inplace=True)
  ckt_new.fillna(value='',inplace=True)
  ckt_new['Total']=1
  lista_ckt = pd.pivot_table(ckt_new,index=['OT', 'CIRC_ESQ', 'CIR_DIR', 'TIPO', 'BITOLA', 'COR',
        'COMP', 'COD_OP_01_ESQ', 'TERMINAL_ESQ', 'ACC_ESQ_1', 'COD_OP_01_DIR',
        'TERMINAL_DIR', 'ACC_DIR_1', 'SOLDA'],values=["Total"],columns=['PROD_TERM'],aggfunc=[np.sum],fill_value=0)
  lista_ckt.columns = [col[2] for col in lista_ckt.columns]
  lista_ckt.reset_index(inplace=True)


  # Tubos
  tb_new_sem_datasul = tb[['PROD_TERM','LINHA', 'TIPO',
       'DIAMETRO', 'COR', 'COMP']].copy()
  tb_new_com_datasul = tb[['PROD_TERM','NUMERO_EMS','LINHA', 'TIPO',
       'DIAMETRO', 'COR', 'COMP']].copy()
  tb_new_sem_datasul['Total']=1
  tb_new_com_datasul['Total']=1
  lista_tb_s_ds = pd.pivot_table(tb_new_sem_datasul,index=['TIPO', 'DIAMETRO', 'COR', 'COMP','LINHA'],values=["Total"],columns=['PROD_TERM'],aggfunc=[np.sum],fill_value=0)
  lista_tb_s_ds.columns = [col[2] for col in lista_tb_s_ds.columns]
  lista_tb_s_ds.reset_index(inplace=True)

  lista_tb_c_ds = pd.pivot_table(tb_new_com_datasul,index=['TIPO', 'DIAMETRO', 'COR', 'COMP','LINHA','NUMERO_EMS'],values=["Total"],columns=['PROD_TERM'],aggfunc=[np.sum],fill_value=0)
  lista_tb_c_ds.columns = [col[2] for col in lista_tb_c_ds.columns]
  lista_tb_c_ds.reset_index(inplace=True)
  # Componentes
  cp_new = cp[['PROD_TERM', 'OT', 'LINHA', 'PARTE_OES', 'QTDE',
       'DESCRICAO']].copy()
  cp_new['Total']=1
  lista_cp = pd.pivot_table(cp_new,index=['PARTE_OES', 'QTDE', 'DESCRICAO','LINHA'],values=["Total"],columns=['PROD_TERM'],aggfunc=[np.sum],fill_value=0)
  lista_cp.columns = [col[2] for col in lista_cp.columns]
  lista_cp.reset_index(inplace=True)
  # Sumarizado
  sz_new = sz[['PA', 'NIVEL', 'PROJETO', 'DESCRICAO_PA', 'DESCRICAO_MP',
       'MP', 'QTDE', 'UM']].copy()
  sz_new['Total']=1
  lista_sz = pd.pivot_table(sz_new,index=[ 'MP','DESCRICAO_MP','QTDE','UM'],values=["Total"],columns=['PROJETO','DESCRICAO_PA','NIVEL','PA'],aggfunc=[np.sum],fill_value=0).sort_index()
  lista_sz.columns = [col[5] for col in lista_sz.columns]
  lista_sz.reset_index(inplace=True)
  return lista_ckt,lista_tb_s_ds,lista_tb_c_ds,lista_cp,lista_sz