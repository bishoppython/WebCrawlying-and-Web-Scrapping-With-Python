from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import time

from termcolor import colored as corzinha

import smtplib
import email.message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def envia_email(conteudo):

    #configuração
    host = 'smtp.gmail.com'
    port = '587'
    user = 'email@gmail.com'
    password = 'passwd'

    #Criando Objeto
    print(corzinha('Criando objeto Servidor...', "red"))
    server = smtplib.SMTP(host, port)

    #Login com Servidor
    print(corzinha('Logando...', "blue"))
    server.ehlo()
    server.starttls()
    server.login(user, password)

    #Criando Mensagem
    message = conteudo
    print(corzinha('Criando Mensagem Personalizada...',"green"))
    email_msg = MIMEMultipart()
    email_msg['From'] = user
    email_msg['To'] = 'email@gmail.com'#email destinatário
    email_msg['Subject'] = ':: Amazon :: Alerta de Produto em Preço Acessível, Compra Logo Pow!' #Mensagem personalizada
    print('Adicionando Texto...')
    email_msg.attach(MIMEText(message, 'plain'))

    #Enviando Mensagem
    print(corzinha('Enviando Mensagem...', "yellow"))
    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
    print(corzinha('Enviando finalmente essa budega!',"green"))
    server.quit()

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)

url = ("https://www.amazon.com.br/Novo-Echo-Dot-4%C2%AA-gera%C3%A7%C3%A3o/dp/B084DWCZY6")

driver.get(url)

time.sleep(5)

div_mae = driver.find_element(By.XPATH, "//*[@id='ppd']") #//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]

html_content = div_mae.get_attribute('outerHTML')

soup = BeautifulSoup(html_content, 'html.parser')

#print(soup.prettify()) # Traz no terminal todo o html para ser analisado (É mais fácil e rápido fazer no inspecionar)

lista_descricao = soup.select("span[id^=productTitle]") #neste metodo sempre retornar uma lista, mesmo que contenha apenas um elemento
lista_preco_produto = soup.find_all("span", class_="a-offscreen")

driver.close() #fecha a pagina após rodar os code acima


descricao = lista_descricao[0].get_text()
preco = lista_preco_produto[0].get_text()

#print("Descrição: ",descricao , "Preço: ",preco) #testando para ver se imprime a informação que preciso

preco_email = preco #salvando apenas para fins de envio de email

# o Replace faz a substituição/remoção de elementos que não queremos na string
preco = preco.replace("R$", "") # Removendo o R + cifrão
preco = preco.replace(",", ".") # Substituindo a ',' por '.'
# O método remove quaisquer caracteres que seguem (caracteres no final de uma sequência), o espaço é o caractere de saída padrão para remover.rstrip()
descricao = descricao.rstrip()#Remove o espaço após o final da string
# O método remove quaisquer caracteres que seguem (caracteres no final de uma sequência), o espaço é o caractere de entrada padrão para remover.lstrip()
descricao = descricao.lstrip()#Remove o espaço antes da string

preco = float(preco)

if preco < 300:
    print(corzinha("Finalmente chegou no precinho, huuummmmmm!!! Enviando o Email", "blue"))
    envia_email(f"{descricao}, o preço está: {preco_email}")
else:
    print(corzinha("Ainda não foi o momento de comprar!!","green"))