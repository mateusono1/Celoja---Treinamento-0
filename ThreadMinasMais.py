from bs4 import BeautifulSoup
import requests
import json
import re
import pandas as pd
import math
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor

def pegar_html(link):  
    req=requests.get(link)
    html=BeautifulSoup(req.text,"html.parser")
    return html


def achar_marcas(html):
    
    marcas=html.find_all("label", attrs={"class":"vtex-checkbox__label w-100 c-on-base pointer"})
    strmarcas=[]
    POP=[]
    REMOVER=[]

    #transformar ps códigos <label ...  em strings
    for elem in marcas:
        strmarcas.append(str(elem))
    

    #achar os índices das labels(em string) que possuem for="category-2...", que não representam marcas
    for i in range(len(strmarcas)):
        if "category-2" in strmarcas[i]:
            POP.append(i)

    #Achar a correlação entre as labels(em string) e as labels normais. Saber qual label normal deve ser removida
    for indice in POP:
        REMOVER.append(marcas[indice])

    for indesejado in REMOVER:
        marcas.remove(indesejado)

    #pegando somente o nome das marcas (retirando toda a estrutura do label)
    TEXTO=[]
    for label in marcas:
        TEXTO.append(label.string)

    #analisando o sorted(TEXTO), percebi que diversos elementos da lista eram duplicados

    #Tirando os nomes duplicados
    TEXTO_S_DUPL=[]
    for elem in TEXTO:
        if elem not in TEXTO_S_DUPL:
            TEXTO_S_DUPL.append(elem) 


    #formatando o nome da marca
    MARCA_PARA_LINK=[]
    for elem in TEXTO_S_DUPL:
        elem=elem.replace(" ","-")
        elem=elem.replace("/","-")
        elem=elem.lower()
        MARCA_PARA_LINK.append(elem)

    #print(strmarcas)
    #print(POP)
    #print(REMOVER)
    return MARCA_PARA_LINK


def achar_marcas_sem_link(html):
    
    marcas=html.find_all("label", attrs={"class":"vtex-checkbox__label w-100 c-on-base pointer"})
    strmarcas=[]
    POP=[]
    REMOVER=[]

    #transformar ps códigos <label ...  em strings
    for elem in marcas:
        strmarcas.append(str(elem))
    

    #achar os índices das labels(em string) que possuem for="category-2...", que não representam marcas
    for i in range(len(strmarcas)):
        if "category-2" in strmarcas[i]:
            POP.append(i)

    #Achar a correlação entre as labels(em string) e as labels normais. Saber qual label normal deve ser removida
    for indice in POP:
        REMOVER.append(marcas[indice])

    for indesejado in REMOVER:
        marcas.remove(indesejado)

    #pegando somente o nome das marcas (retirando toda a estrutura do label)
    TEXTO=[]
    for label in marcas:
        TEXTO.append(label.string)

    #analisando o sorted(TEXTO), percebi que diversos elementos da lista eram duplicados

    #Tirando os nomes duplicados
    TEXTO_S_DUPL=[]
    for elem in TEXTO:
        if elem not in TEXTO_S_DUPL:
            TEXTO_S_DUPL.append(elem)

    return TEXTO_S_DUPL



def link (MARCA_LINK):
    LINK=[]
    for i in MARCA_LINK:
        link=f"https://www.drogariasminasmais.com.br/medicamentos/{i}?initialMap=c&initialQuery=medicamentos&map=category-1,brand"
        link+="&page="
        LINK.append(link)
    return(LINK)


def qtd_produtos(json_pag,marca):
    nome='$ROOT_QUERY.facets({"behavior":"Static","categoryTreeBehavior":"default","hideUnavailableItems":true,"initialAttributes":"c","query":"medicamentos/hypera","selectedFacets":[{"key":"category-1","value":"medicamentos"},{"key":"brand","value":"hypera"}]})@context({"provider":"vtex.search-graphql"})@runtimeMeta({"hash":"d0cbc665c0364a2c77575f998051aa1a9f8a04a60174d78356b18b0406fe48b6"}).facets.3.values({}).'
    for key,values in json_pag.items():
        if key.startswith(nome):
            

            #alterar a formatação da marca
            marca=marca.upper()
            for sub_key,sub_value in values.items():
                if sub_key=='quantity':
                    quantidade=sub_value
                if sub_key=='name' and sub_value==marca:
                    return quantidade
                
def get_json(url):
        requisicao = requests.get(url)
        soup = BeautifulSoup(requisicao.text, 'html.parser')

        string = soup.find_all('script')[-34].text #Converter para arquivo de texto (retira as tags)

        json_file = string.split("__STATE__ = ", 1) #1 é o indice (lista é criada com o split)
        
        return json.loads(json_file[1])



def get_ean(json_pag):
    EAN=[]
    for key,value in json_pag.items():
        if key.startswith('Product:sp-'):
            for sub_key,sub_value in value.items():
                if sub_key == "ean":
                    EAN.append(sub_value)

    return(EAN)


def get_name(json_pag):
    NOMES=[]
    for key,value in json_pag.items():
        if key.startswith('Product:sp-'):
            for sub_key,sub_value in value.items():
                if sub_key=='productName':
                    sub_value=sub_value.split(" -")[0]
                    NOMES.append(sub_value)
    return NOMES


def get_preço_c_desconto(json_pag):
    VENDA=[]
    for key,value in json_pag.items():
        if '$Product:sp-' and '.priceRange.sellingPrice' in key:
            for sub_key,sub_value in value.items():
                if sub_key == 'highPrice':
                    VENDA.append(sub_value)
    return VENDA


def get_preço_s_desconto(json_pag):
    CHEIO=[]
    for key,value in json_pag.items():
        if '$Product:sp-' and '.priceRange.listPrice' in key:
            for sub_key,sub_value in value.items():
                if sub_key == 'highPrice':
                    CHEIO.append(sub_value)
    return CHEIO


def desconto(A,B):
    DESCONTO=[]
    for i in range(len(A)):
        x= B[i] - A[i]
        if x<0:
            x=(-1)*x
            x=round(x,2)
            DESCONTO.append(x)
        else:
            x=round(x,2)
            DESCONTO.append(x)
    return DESCONTO




def main(inicio,fim):
    colunas=['EAN','Marca','Nome','Preço com desconto','Preço sem desconto','Desconto']
    df=pd.DataFrame(columns=colunas)


    url='https://www.drogariasminasmais.com.br/medicamentos'
    html=pegar_html(url)
    marcas=achar_marcas(html)
    LINKS=link(marcas)
    MARCAS=achar_marcas_sem_link(html)
    E=[]
    M=[]
    PC=[]
    PV=[]
    N=[]
    D=[]

    for j in range(inicio,fim):
        json_pag=get_json(LINKS[j] + "1")
        json_generico=get_json(LINKS[0] + "1")
        pag=qtd_produtos(json_generico,MARCAS[j])
        print(pag,MARCAS[j])
        pag=pag/15
        pag=math.ceil(pag) + 1
        
        for i in range(1,pag):

            colunas =['EAN','Marca','Nome','Preço com desconto','Preço sem desconto','Desconto']
            df1=pd.DataFrame(columns=colunas)


            json_pag=get_json(LINKS[j] + str(i))
            ean=get_ean(json_pag)
            nomes_produtos=get_name(json_pag)
            p_des=get_preço_c_desconto(json_pag)
            p_s_des=get_preço_s_desconto(json_pag)
            DESCONTO=desconto(p_s_des,p_des)

            df1['EAN']=ean
            df1['Marca']=marcas[j]
            df1['Nome']=nomes_produtos
            df1['Preço com desconto']=p_des
            df1['Preço sem desconto']=p_s_des
            df1['Desconto']=DESCONTO

            df=pd.concat([df,df1])  

    return df


pool=ThreadPoolExecutor(6)
df1=pool.submit(main,0,3)
df2=pool.submit(main,3,8)
df3=pool.submit(main,8,20)
df4=pool.submit(main,20,65)
df5=pool.submit(main,65,115)
df6=pool.submit(main,115,216)

df1f=df1.result()
df2f=df2.result()
df3f=df3.result()
df4f=df4.result()
df5f=df5.result()
df6f=df6.result()

df=pd.concat([df1f,df2f,df3f,df4f,df5f,df6f])
df.reset_index(inplace=True,drop=True)

df.to_excel("MinasMaisThread.xlsx")

