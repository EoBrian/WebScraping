import apps
import os

TELEFONES = []
LINKS = []

URL_AUTOMOVEIS = 'https://django-anuncios.solyd.com.br/automoveis/'
DOMINIO = 'https://django-anuncios.solyd.com.br'


if __name__ == '__main__':
    os.system('cls')

    buscando_site = apps.requisiçãoWeb(URL_AUTOMOVEIS)
    if buscando_site:

        site_texto = apps.parsingHTML(buscando_site)
        if site_texto:

            LINKS = apps.takeLinks(site_texto)
            apps.processos(apps.descobrirTelefone(LINKS,DOMINIO,TELEFONES))

            print(TELEFONES)