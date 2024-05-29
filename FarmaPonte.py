import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import json

# Definindo a classe Scraper
class Scraper:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.farmaponte.com.br/saude/medicamentos"

    def get_html(self, url):
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                return response.text
            else:
                return None
        except requests.RequestException:
            return None
    
    def get_links(self, page_number):
        url_completa = f"{self.base_url}?p={page_number}"
        html = self.get_html(url_completa)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            elementos = soup.find_all('a', class_='item-image')
            links = ['https://www.farmaponte.com.br' + elemento.get('href') for elemento in elementos]
            return links
        else:
            return []
        
    def parse_data(self, link):
        html = self.get_html(link)
        if html:
            soup = BeautifulSoup(html, 'html.parser')

            titulo_tag = soup.find('h1', {'itemprop': 'name'})
            gtin13_tag = soup.find('meta', {'itemprop': 'gtin13'})
            marca_tag = soup.find('a', class_='text-primary font-weight-bold')
            preco_sem_desconto_tag = soup.find('p', class_='unit-price')
            preco_com_desconto_tag = soup.find('div', class_='pix-price')

            titulo = titulo_tag.get_text().strip() if titulo_tag else 'Título não encontrado'
            gtin13 = gtin13_tag.get('content') if gtin13_tag else 'EAN não encontrado'
            marca = marca_tag.get_text().strip() if marca_tag else 'Marca não encontrada'
            preco_sem_desconto = preco_sem_desconto_tag.get_text().strip() if preco_sem_desconto_tag else 'Preço sem desconto não encontrado'
            preco_com_desconto = preco_com_desconto_tag.get_text().strip() if preco_com_desconto_tag else 'Preço com desconto não encontrado'

            if "R$" in preco_com_desconto and "R$" in preco_sem_desconto:
                preco_sem_desconto = preco_sem_desconto.replace('R$','')
                preco_sem_desconto = preco_sem_desconto.replace('.','')
                preco_sem_desconto = preco_sem_desconto.replace(',','.')
                preco_sem_desconto = float(preco_sem_desconto)

                preco_com_desconto = preco_com_desconto.replace('R$','')
                preco_com_desconto = preco_com_desconto.replace('no pix','')
                preco_com_desconto = preco_com_desconto.replace('.','')
                preco_com_desconto = preco_com_desconto.replace(',','.')
                preco_com_desconto = float(preco_com_desconto)

                discount = preco_sem_desconto - preco_com_desconto

            else:
                discount = 0.0

            return {
                'EAN' : gtin13,
                'Marca': marca,
                'Nome': titulo,
                'Preço com desconto': preco_com_desconto,
                'Preço sem desconto': preco_sem_desconto,
                'Desconto' : discount
            }
        else:
            return None
        
    def extract_all_data(self, num_pages):
        links = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for page_links in executor.map(self.get_links, range(1, num_pages + 1)):
                links.extend(page_links)

        products = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            for product_data in executor.map(self.parse_data, links):
                if product_data:
                    products.append(product_data)

        return products
    
    # Uso da classe Scraper
def main():
    scraper = Scraper()
    numero_paginas = 229
    informacoes_produtos = scraper.extract_all_data(numero_paginas)
    df = pd.DataFrame(informacoes_produtos)
    df["Drogaria"]="Farma Ponte"
    #print(df.to_string())
    df.to_excel('FarmaPonte.xlsx')

