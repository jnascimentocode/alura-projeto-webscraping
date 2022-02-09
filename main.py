from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import os
import pandas as pd

def trata_html(input):
    return " ".join(input.split()).replace('> <', '><')

os.system('cls')

#declarando variavel cards
cards = []

#Obtendo o HTML e o total de paginas
url = 'https://alura-site-scraping.herokuapp.com/index.php'
response = urlopen(url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
pages = int(soup.find('span', class_='info-pages').get_text().split()[-1])

## iterando todas as paginas do site
for i in range(pages):

    #Obtendo o HTML
    url = 'https://alura-site-scraping.herokuapp.com/index.php?page=' + str(i + 1)
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    #obtendo as tags de interesse 
    anuncios = soup.find('div', {"id": "container-cards"}).findAll('div', class_="card")

    #Coletando as informações dos Cards
    for anuncio in anuncios:
        card = {}
        
        # Valor
        card['value'] = anuncio.find('p', {'class': 'txt-value'}).getText()

        # Informações
        infos = anuncio.find('div', {'class': 'body-card'}).findAll('p')
        for info in infos:
            card[info.get('class')[0].split('-')[-1]] = info.get_text()

        # Acessórios
        items = anuncio.find('div', {'class': 'body-card'}).ul.findAll('li')
        items.pop()
        acessorios = []
        for item in items:
            acessorios.append(item.get_text().replace('► ', ''))
        card['items'] = acessorios

        #Adicionando uma lista de cards
        cards.append(card)

        # Imagens
        image = anuncio.find('div', {'class': 'image-card'}).img
        urlretrieve(image.get('src'), 'output/img/' + image.get('src').split('/')[-1]) 

#criando um Dataset a partir do dicionario criado
dataset = pd.DataFrame(cards)
dataset.to_csv('output/data/dataset.csv', sep=';', index= False, encoding='utf-8-sig')




