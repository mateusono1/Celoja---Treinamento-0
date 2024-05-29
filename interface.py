import streamlit as st
import pandas as pd
import datetime





st.set_page_config(page_title="Interface de busca",layout="wide",
                initial_sidebar_state="expanded", page_icon="Back.jpg",)


#Título da página
st.markdown('<h1 style="text-align: left; font-family: Helvetica; font-size: 22px;">Interface de busca </h1>',
    unsafe_allow_html=True)


#realize a extração
st.markdown('<h1 style="text-align: left; color:rgb(19, 85, 98); font-family: Helvetica; font-size: 40px;">Realize a extração </h1>',
    unsafe_allow_html=True)
if st.button("Minas Mais"):
    horario_inicial=datetime.datetime.now()
    horario_inicial=horario_inicial.strftime("%H:%M")
    st.write("Extraindo dados. Tempo aproximado de extração: 10 min. Início:",horario_inicial)

    import ThreadMinasMais
    ThreadMinasMais.thread()
    horario_final=datetime.datetime.now()
    horario_final=horario_final.strftime("%H:%M")
    st.success(f"Extração Concluída. Iniciada às {horario_inicial} Finalizada às {horario_final}")

if st.button("Vera Cruz"):
    horario_inicial=datetime.datetime.now()
    horario_inicial=horario_inicial.strftime("%H:%M")
    st.write("Extraindo dados. Tempo aproximado de extração: 15 min. Início:",horario_inicial)

    import ThreadVeraCruz
    ThreadVeraCruz.thread()
    horario_final=datetime.datetime.now()
    horario_final=horario_final.strftime("%H:%M")
    st.success(f"Extração Concluída. Iniciada às {horario_inicial} Finalizada às {horario_final}")
if st.button("Farma Ponte"):
    horario_inicial=datetime.datetime.now()
    horario_inicial=horario_inicial.strftime("%H:%M")
    st.write("Extraindo dados. Tempo aproximado de extração: 10 min. Início:",horario_inicial)


    import FarmaPonte
    FarmaPonte.main()
    horario_final=datetime.datetime.now()
    horario_final=horario_final.strftime("%H:%M")
    st.success(f"Extração Concluída. Iniciada às {horario_inicial} Finalizada às {horario_final}")




df_minas=pd.read_excel("MinasMaisThread.xlsx")
df_vera=pd.read_excel("VeraCruzThread.xlsx")
df_farma=pd.read_excel("FarmaPonte.xlsx")

#Insira infosque deseja selecionar
st.markdown('<h1 style="text-align: left; color:rgb(19, 85, 98); font-family: Helvetica; font-size: 40px;">Insira que deseja selecionar (pós extração) </h1>',
    unsafe_allow_html=True)

EAN1=df_minas["EAN"].unique()
EAN1=EAN1.tolist()
EAN2=df_vera["EAN"].unique()
EAN2=EAN2.tolist()
EAN3=df_farma["EAN"].unique()
EAN3=EAN3.tolist()

TODOS_EAN=list(set(EAN1 + EAN2 + EAN3))




###PEGANDO TODOS OS EAN DOS 2 SITES (EVITAR NOMES DIFERENTES)

df_temp1=df_minas[df_minas["EAN"].isin(TODOS_EAN)]
df_temp2=df_vera[df_vera["EAN"].isin(TODOS_EAN)]
df_temp3=df_farma[df_farma["EAN"].isin(TODOS_EAN)]
df_analise=pd.concat([df_temp1,df_temp2,df_temp3])
df_analise.reset_index(inplace=True,drop=True)
df_analise.drop(columns=["Unnamed: 0"],inplace=True)

df_analise.to_excel("df_mesclada_interface.xlsx")

NOME=[]
for elem in df_analise["Nome"]:
    NOME.append(elem)



produto_selecionado=st.selectbox("Produto",NOME)

ean=str(df_analise.loc[df_analise["Nome"]==produto_selecionado,"EAN"].iloc[0])
st.write(ean)



opções=["Nome","EAN","Preço com desconto","Preço sem desconto","Desconto","Drogaria"]
SELECIONADOS=st.multiselect("O que deseja buscar?",opções)


##############
#colunas=["Nome","EAN","Preço com desconto","Preço sem desconto","Desconto","Drogaria"]

#df_bi=pd.DataFrame()



if st.button("Finalizar seleção das informações"):
    linha=df_analise.loc[df_analise["EAN"]==ean,SELECIONADOS]
    print(linha)



if st.button("Enviar para o PowerBI"):
    linha=df_analise.loc[df_analise["EAN"]==ean,SELECIONADOS]
    linha.to_excel("DATAFRAME_POWERBI.xlsx")

########ARRUMAR COMO AS INFOS SÃO INSERIDAS NA DF FINAL
#MINHA IDEIA É FAZER VÁRIOS IF ELSE

#AAAAAAAAAAAAAa
