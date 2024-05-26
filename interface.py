import streamlit as st
import pandas as pd
import datetime


df_minas=pd.read_excel("MinasMaisThread.xlsx")
df_vera=pd.read_excel("VeraCruzThread.xlsx")


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
    st.write("TRÊS")



#Insira infosque deseja selecionar
st.markdown('<h1 style="text-align: left; color:rgb(19, 85, 98); font-family: Helvetica; font-size: 40px;">Insira que deseja selecionar (pós extração) </h1>',
    unsafe_allow_html=True)

opções=["Nome","EAN","Preço c/desconto","Preço s/desconto","Desconto"]
SELECIONADOS=st.multiselect("O que deseja buscar?",opções)





NOME=df_minas["Nome"].unique()
nome=st.selectbox("Produto",NOME)

for i in range(len(df_minas)):
    if df_minas.loc[i,"Nome"] == nome:
        marca=df_minas.loc[i,"Marca"]
        ean=df_minas.loc[i,"EAN"]
st.write("O ean é: ",ean)
st.write("A marca é: ",marca)