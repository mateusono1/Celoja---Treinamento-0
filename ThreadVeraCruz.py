from bs4 import BeautifulSoup
import requests
import json
import re
import pandas as pd
import math
from unidecode import unidecode
from concurrent.futures import ThreadPoolExecutor

def pegar_html(link):  
    req=requests.get(link)
    html=BeautifulSoup(req.text,"html.parser")
    return html
url='https://www.drogariaveracruz.com.br/medicamentos/'


def num_pag(html):
    string=html.find_all('div',{'class':'text-center pt-3'})[1].text
    lista=string.split()
    paginas= int(lista[-1])
    return paginas


def get_links_produtos(html):
    div=html.find_all('div',{'class':'item-product'})
    LINKS=[]
    for caixa  in div:
        link_tag=caixa.find('a',{'class':'item-image position-relative'})
        link=link_tag.get('href')
        link="https://www.drogariaveracruz.com.br/"+link
        LINKS.append(link)
    return LINKS

def get_ean(html):
    div=html.find('div',{'class':'d-flex flex-wrap text-muted mb-3'})
    tag_gtin=div.find('meta',{'itemprop':'gtin13'})
    if tag_gtin == None:
        gtin="SEM EAN"
    else:
        gtin=tag_gtin.get('content')
        gtin=int(gtin)
    return gtin

def get_marca(html):
    div=html.find('div',{'class':'d-flex flex-wrap text-muted mb-3'})
    tag_marca=div.find('meta',{'itemprop':'brand'})
    if tag_marca == None:
        return "SEM MARCA REGISTRADA"
    else:
        marca=tag_marca.get('content')
        return marca


def get_preço_cheio(html):
    div=html.find('div',{'class':'position-relative'})
    if div.find('h2') != None:
        return "PRODUTO ESGOTADO"
    elif div.find('p',{'class':'unit-price'})==None:
        cheio = div.find('p',{'class':'sale-price'})
        
    else:
        cheio=div.find('p',{'class':'unit-price'}).text
        cheio=cheio.replace('\n                                                    R$ ','')
        cheio=cheio.replace('\n','')
        cheio=cheio.replace('.','')
        cheio=float(cheio.replace(',','.'))
        return cheio

def get_preço_venda(html):
    div=html.find('div',{'class':'position-relative'})
    if div.find('h2',) != None:
        return "PRODUTO ESGOTADO"
    else:
        venda=div.find('p',{'class':'sale-price'}).text
        venda=venda.replace('R$ ','')
        venda=venda.replace('\n','')
        venda=venda.replace('.','')
        venda=float(venda.replace(',','.'))
        return venda

def get_nome(html):
    nome=html.find('h1',{'class':'name','itemprop':'name'}).text
    return nome

def get_desconto(cheio,venda):
    if cheio == "PRODUTO ESGOTADO":
        return cheio
    else:
        dis=cheio-venda
        if dis<0:
            dis=dis*(-1)
        return dis


url='https://www.drogariaveracruz.com.br/medicamentos/'
html=pegar_html(url)

numero_paginas=num_pag(html)


E=[]
M=[]
PC=[]
PV=[]
N=[]
D=[]
i=1

def main(inicio,fim):
    for pagina in range (inicio,fim):

        url=f'https://www.drogariaveracruz.com.br/medicamentos/?p={pagina}'
        html=pegar_html(url)
        LINKS_PRODUTOS=get_links_produtos(html)

        for url in LINKS_PRODUTOS:
            produto=pegar_html(url)
            ean=get_ean(produto)
            marca=get_marca(produto)
            preço_cheio=get_preço_cheio(produto)
            preço_venda=get_preço_venda(produto)
            nome=get_nome(produto)
            desconto=get_desconto(preço_cheio,preço_venda)

            E.append(ean)
            M.append(marca)
            PC.append(preço_cheio)
            PV.append(preço_venda)
            N.append(nome)
            D.append(desconto)
        #print(f'{i}/153 paginas lidas')
        #i+=1
    df=pd.DataFrame({
        "EAN":E,
        "Marca":M,
        "Nome":N,
        "Preço sem desconto":PC,
        "Preço com desconto":PV,
        "Desconto":D
    })  
    return df

#print(numero_paginas) #6 pools de 26 paginas cada
#1,27
#27,53
#53,79
#79,105
#105,131
#131,157

pool=ThreadPoolExecutor(6)
df1=pool.submit(main,1,27)
df2=pool.submit(main,27,53)
df3=pool.submit(main,53,79)
df4=pool.submit(main,79,105)
df5=pool.submit(main,105,131)
df6=pool.submit(main,131,157)

df1.result().to_excel("Teste1Vera.xlsx")
df2.result().to_excel("Teste2Vera.xlsx")

print("Terminou a execução")












