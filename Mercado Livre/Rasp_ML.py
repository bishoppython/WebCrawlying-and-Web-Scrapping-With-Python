import requests
from bs4 import BeautifulSoup

#url_base = 'https://lista.mercadolivre.com.br/'

url_baseML = 'https://lista.mercadolivre.com.br/'


produto_nome = input('Qual o produto que deseja pesquisar? ')

#print(url_base + produto_nome) #- Tras a URL formada

response = requests.get(url_baseML + produto_nome)

site = BeautifulSoup(response.text, 'html.parser') #obtem a página completa da pesquisa realizada

#produtos = site.findAll('div', attrs={'class':'andes-card andes-card--flat andes-card--default ui-search-result ui-search-result--core andes-card--padding-default'})

produtos = site.findAll('div', attrs={'class':'ui-search-result__wrapper'})

for produto in produtos:
    titulo = produto.find('h2', attrs={'class': 'ui-search-item__title'})
    #link = produto.find('a', attrs={'class': 'ui-search-item__group__element ui-search-link'})
    link = produto.find('a', attrs={'class': 'ui-search-link'})
    symbol = produto.find('span', attrs={'class': 'price-tag-symbol'})
    preco = produto.find('span', attrs={'class': 'price-tag-fraction'})
    cents = produto.find('span', attrs={'class': 'price-tag-cents'})

    #print(site.prettify())
    print('Produto: ', titulo.text)
    print('Link do Produto: ', link['href'])
    if (cents):
        print('Preço: ', symbol.text + preco.text + ',' + cents.text)
    else:
        print('Preço: ', symbol.text + preco.text)

    print('\n\n')
