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
    st.write("TRÊSTESTE")



#Insira infosque deseja selecionar
st.markdown('<h1 style="text-align: left; color:rgb(19, 85, 98); font-family: Helvetica; font-size: 40px;">Insira que deseja selecionar (pós extração) </h1>',
    unsafe_allow_html=True)

NOME=df_minas["Nome"].unique()
nome=st.selectbox("Produto",NOME)

for i in range(len(df_minas)):
    if df_minas.loc[i,"Nome"] == nome:
        marca=df_minas.loc[i,"Marca"]
        ean=df_minas.loc[i,"EAN"]
st.write("O ean é: ",ean)
st.write("A marca é: ",marca)





opções=["Nome","EAN","Preço com desconto","Preço sem desconto","Desconto"]
SELECIONADOS=st.multiselect("O que deseja buscar?",opções)




##############
df_bi=pd.DataFrame()
for item_escolhido in SELECIONADOS:
    print(item_escolhido)
    df_bi_temp=df_minas.loc[df_minas["EAN"]==ean,item_escolhido]
    df_bi=pd.concat([df_bi,df_bi_temp])
    df_bi_temp=df_vera.loc[df_vera["EAN"]==ean,item_escolhido]
    df_bi=pd.concat([df_bi,df_bi_temp])

if st.button("Enviar para o PowerBI"):
    df_bi.to_excel("DATAFRAME_POWERBI.xlsx")

########ARRUMAR COMO AS INFOS SÃO INSERIDAS NA DF FINAL
#MINHA IDEIA É FAZER VÁRIOS IF ELSE
