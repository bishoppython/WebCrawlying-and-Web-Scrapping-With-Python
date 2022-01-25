"""
Main script, desenvolvido por
Anderson Bispo, Analista de Suporte jr. da Assertiva Soluções,
criado no intuito de "raspar" (ou fazer scrapy) Qualquer comentário de Videos do Youtube.

Exemplo de Execução:
    $ python main.py YOUTUBE_VIDEO_URL
"""

import csv
import io
from selenium import webdriver
from selenium.common import exceptions
import sys
import time

def scrape(url):
    """
    Extrai os comentários do vídeo do Youtube fornecidos pela URL.

    Args:
        url (str): A URL para o Video do Youtube.

    Raises:
        selenium.common.exceptions.NoSuchElementException:
        Sempre que certos elementos para busca não podem ser encontrados!
    """

    # Note: Baixe e substitua o argumento pelo caminho para o executável do driver.
    # Basta baixar o executável e movê-lo para a pasta webdrivers.
    driver = webdriver.Chrome('./webdrivers/chromedriver')

    # Navega para o URL, maximiza a janela atual e
    # então suspende a execução por (pelo menos) 5 segundos (este dá tempo para a página carregar).
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)

    try:
        # Extraia os elementos que armazenam o título do vídeo e a seção de comentários.
        title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
        comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
    except exceptions.NoSuchElementException:
        # Nota: O Youtube pode ter alterado seus layouts HTML para vídeos, então gere um erro por questões de bom senso caso o
        # os elementos fornecidos não podem mais ser encontrados.
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    # Role para ver a seção de comentários e aguarde algum tempo para que tudo seja carregado conforme necessário.
    driver.execute_script("arguments[0].scrollIntoView();", comment_section)
    time.sleep(7)

    # Role até o final para carregar todos os elementos (já que o Youtube os carrega dinamicamente).
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # Role para baixo até "próximo carregamento".
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Aguarde para carregar tudo até agora.
        time.sleep(2)

        # Calcule a nova altura de rolagem e compare com a última altura de rolagem.
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Um último rolo apenas no caso.
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    try:
        # Extraia os elementos que armazenam os nomes de usuário e comentários.
        username_elems = driver.find_elements_by_xpath('//*[@id="author-text"]')
        comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
    except exceptions.NoSuchElementException:
        error = "Error: verifique novamente o seletor OU "
        error += "elemento pode ainda não estar na tela no momento da operação de busca"
        print(error)

    print("> TÍTULO DO VIDEO: " + title + "\n")

    with io.open('Comentarios_Extraidos.csv', 'w', newline='', encoding="utf-16") as file:
        writer = csv.writer(file, delimiter =",", quoting=csv.QUOTE_ALL)
        writer.writerow(["Usuários", "Commentários"])
        for username, comment in zip(username_elems, comment_elems):
            writer.writerow([username.text, comment.text])

    driver.close()

if __name__ == "__main__":
    scrape(sys.argv[1])
