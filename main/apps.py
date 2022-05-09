import re
from threading import Thread

from bs4 import BeautifulSoup
from requests import get


#FAZENDO A REQUISIÇÃO
def requisiçãoWeb(url):
    try:
        requisição = get(url)
        if requisição.status_code == 200:
            return requisição.text
        
        else:
            print('ERRO AO FAZER REQUISIÇÃO!')
    
    except Exception as error:
        print(f'\n>>> O ERRO ({error}) OCORREU!')

#TRANSFORMA A PÁGINA HTML EM OBJETOS EM PYTHON
def parsingHTML(text_html):
    try:
        html = BeautifulSoup(text_html, 'html.parser')
        return html
    
    except Exception as error:
        print('\n>>>> ERRO AO FAZER PARSING')
        print(error)

#RETORNA UMA LISTA COM OS LINKS DOS VEICULOS
def takeLinks(parsing):
    links = []

    text_html = parsing.find('div', class_='ui three doubling link cards')
    cards = text_html.find_all('a')
    
    for card in cards:
        link = card['href']
        links.append(link)
        
    return links

#IDENTIFICA O NÚMERO NO SITE DO ANUNCIO COM A FUNÇÃO REGEX
def buscar_telefone(text):
    try:
        telefone = text.find_all('div', class_='sixteen wide column')[2].p.get_text().strip()

    except Exception as error:
        print(f'\n>>> O ERRO ({error}) OCORREU!')
    
    regex = re.findall(r"\(?0?([1-9]{2})[ \-\.\)]{0,2}(9[ \-\.]?\d{4})[ \-\.]?(\d{4})", telefone)
    if regex:
        return regex

#PEGA O TELEFONE E O COLOCA NA LISTA 'TELEFONE'
def descobrirTelefone(lista_links, dominio, lista_telefone):
    
    while True:
        try:
            link_anuncio = lista_links.pop(0)
        
        except:
            return None

        procurar_telefone = requisiçãoWeb(dominio + link_anuncio)
            
        if procurar_telefone:
            telefone_texto = parsingHTML(procurar_telefone)
            
            if telefone_texto:
                telefones = buscar_telefone(telefone_texto)

                if telefones:
                    for telefone in telefones:
                        lista_telefone.append(telefone)

#FAZENDO MAIS DE UMA REQUISIÇÃO AO MESMO TEMPO
def processos(função):
    processo_1 = Thread(target= função)
    processo_2 = Thread(target= função)

    processo_1.start()
    processo_2.start()
    
    processo_1.join()
    processo_2.join()


