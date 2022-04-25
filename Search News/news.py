import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

lista_noticias = []

response = requests.get('https://g1.globo.com/')

content = response.content

site = BeautifulSoup(content, 'html.parser')

noticias = site.findAll('div', attrs={'class':'feed-post-body'})

for noticia in noticias:
    #Titulo em Vermelho - #Link da Noticia
    titulo = noticia.find('a', attrs={'class': 'feed-post-link'})
    #Descrição da Noticia
    subtitulo = noticia.find('div', attrs={'class':'feed-post-body-resumo'})
    #Tempo que foi postada
    postadoA = noticia.find('span', attrs={'class':'feed-post-datetime'})

    #if (titulo):
        #print(titulo.text)
    if (subtitulo):
        #print(subtitulo.text)
        lista_noticias.append([titulo.text, subtitulo.text, titulo['href'], postadoA.text])
    #print('Acesse: ', titulo['href'])
    #print('Postado ', postadoA.text)
    #print('\n')
    else:
        lista_noticias.append([titulo.text, '', titulo['href'], postadoA.text])

#Transformando em uma tabela
news = pd.DataFrame(lista_noticias, columns=['Titulos', 'Subtitulos', 'Link', 'Postado há'])

#Exportar para formato Excel
news.to_excel('Noticias_G1.xlsx', index=False) # o index=False remove os números que antecedem a noticia, logo o indice.

#print(news)
