import streamlit as st
import pandas as pd

df_minas=pd.read_excel("MINAS_MAIS.xlsx")
df_vera=pd.read_excel("VERACRUZDEUCERTO.xlsx")

EAN=df_minas["EAN"].unique()
print(EAN)




st.set_page_config(page_title="Interface de busca",layout="wide",
                initial_sidebar_state="expanded", page_icon="Back.jpg",)


st.markdown('<h1 style="text-align: left; font-family: Helvetica; font-size: 22px;">Interface de busca </h1>',
    unsafe_allow_html=True)
st.markdown('<h1 style="text-align: left; color:rgb(19, 85, 98); font-family: Helvetica; font-size: 40px;">Insira informações do produto </h1>',
    unsafe_allow_html=True)

numero=st.selectbox("ean",EAN)

for i in range(len(df_minas)):
    if df_minas.loc[i,"EAN"] == numero:
        marca=df_minas.loc[i,"Marca"]
for i in range(len(df_minas)):
    if df_minas.loc[i,"EAN"] == numero:
        nome=df_minas.loc[i,"Nome"]
st.write("O nome é: ",nome)
st.write("A marca é: ",marca)



