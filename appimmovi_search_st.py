# importando bibliotecas adicionais:
import streamlit as st
import pandas as pd
import bs4
from bs4 import BeautifulSoup
import requests
# importando bibliotecas padrão python:
import re
import string
import json

# ocultando o menu 'sanduiche' do streamlit:
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# escrevendo o titulo
st.title('Teste Appimmovi Search')

# escrevendo subtitulo
st.write('Esta é nossa primeira tentativa de rodar o codigo do jupyter notebook no streamlit')

# criando listas vazias:
name_site_vivareal = []
operacao_vivareal = []
codigo_imovel_vivareal = []
estado_vivareal = []
link_list_vivareal = []
address_list_vivareal = []
title_list_vivareal = []
price_list_vivareal = []
area_list_vivareal = []
equipamentos_vivareal = []
bedrooms_list_vivareal = []
bathroom_list_vivareal = []
garages_list_vivareal = []
condominio_list_vivareal = []
cep_vivareal = []
link_maps_endereço = []
link_maps_cep = []
nome_anunciante_vivareal = []
tel_anunciante_vivareal = []
iptu_vivareal = []
locais_proximos_vivareal = []
conservacao_vivareal = []
utilizacao_vivareal = []
complemento_vivareal = []
# latitude_vivareal = []
# longitude_vivareal = []
latitude_logr_vivareal = []
longitude_logr_vivareal = []
latitude_cep_vivareal = []
longitude_cep_vivareal = []

# definindo parametros para mudar a url de busca:
# definindo cabeçalho para resolver divergencia entre janela de inspeção e codigo-fonte html facilitando scrapping
headers = {
    'authority': 'www.vivareal.com.br',
    'Referer': 'https://www.google.com.br/',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    # 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0 Chrome/79.0.3945.88 Safari/537.36',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "Accept-Encoding": "gzip, deflate, br",
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    # 'accept-language': 'en-US,en;q=0.9',
    "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",

}

# fazendo requisição à url:
url_vivareal = st.text_input('Digite o link do vivareal aqui: ')

# colocando o codigo original abaixo do condicional
# para não dar erro ao carregar a aplicação:
if url_vivareal.title() != "":
    req_vivareal = requests.get(url_vivareal, headers=headers)
    content_vivareal = req_vivareal.content
    # trazendo o conteudo da pagina em html:
    soup_vivareal_html = BeautifulSoup(content_vivareal, 'html.parser')
    # definindo variavel para range variavel do 'for' de acordo com a quantidade total de anuncios na pagina representados por containers
    container_vivareal = soup_vivareal_html.find_all(
        "span", {"class": "property-card__title js-cardLink js-card-title"})
    # trazendo conteudo da pagina em java script:
    req_vivareal_js = requests.get(url_vivareal)
    soup_vivareal_js = BeautifulSoup(req_vivareal_js.content, 'html.parser').find_all('script')[2]
    # soup_vivareal_js_xml = BeautifulSoup(req_vivareal_js.content, 'lxml').find_all('script')[10]
    soup_vivareal_js_unicode = soup_vivareal_js.decode()
    # soup_vivareal_js_unicode_xml = soup_vivareal_js_xml.decode()
    # definindo os itens que queremos obter da pagina (html)
    for link in range(0, len(container_vivareal)):
        d = soup_vivareal_html.find_all(
            'a', "property-card__labels-container js-main-info js-listing-labels-link")[link]
        d0 = d.find_next(
            "span", {"class": "property-card__address"}).text.replace('', '')
        d1 = d.find_next("span", {
            "class": "property-card__title js-cardLink js-card-title"}).text.replace("", "")
        d2 = d.find_next("p", {"style": "display: block;"}).text.replace("", "")
        d3 = d.find_next("span", {
            "class": "property-card__detail-value js-property-card-value property-card__detail-area js-property-card-detail-area"}).text.replace(
            "", "")
        d4 = d.find_next("li", {
            "class": "property-card__detail-item property-card__detail-room js-property-detail-rooms"}).text.replace("", "")
        d5 = d.find_next("li", {
            "class": "property-card__detail-item property-card__detail-bathroom js-property-detail-bathroom"}).text.replace(
            "", "")
        d6 = d.find_next("li", {
            "class": "property-card__detail-item property-card__detail-garage js-property-detail-garages"}).text.replace("",
                                                                                                                         "")
        # .text.replace("","")
        d7 = d.find_next("strong", {"class": "js-condo-price"})
        d8 = soup_vivareal_html.find(
            "a", {"class": "breadcrumb__item-name"}).text.replace('', '')
        d9 = soup_vivareal_html.find(
            "a", {"class": "breadcrumb__item-name js-link"}).text.replace('', '')
        d10 = soup_vivareal_html.find(
            "span", {"class": "breadcrumb__item-name"}).text.replace('', '')
        d11 = soup_vivareal_html.find(
            "span", {"class": "js-location-uf"}).text.replace('', '')
        d12 = soup_vivareal_html.find(
            "li", {"class": "location__pill js-pill"}).text.replace('', '')[:-5]
        # .text.replace('','')
        d13 = d.find_next("ul", {"class": "property-card__amenities"})
        d14 = 'https://www.google.com/maps/search/?api=1&query=' + d0
        link_list_vivareal.append('https://www.vivareal.com.br' + d['href'])
        address_list_vivareal.append(d0)
        title_list_vivareal.append(d1)
        price_list_vivareal.append(d2)
        area_list_vivareal.append(d3)
        bedrooms_list_vivareal.append(d4)
        bathroom_list_vivareal.append(d5)
        garages_list_vivareal.append(d6)
        condominio_list_vivareal.append(d7)
        name_site_vivareal.append(d8)
        operacao_vivareal.append(d9)
        estado_vivareal.append(d11)
        equipamentos_vivareal.append(d13)
        link_maps_endereço.append(d14)

    # definindo os itens que queremos obter por Regex da pagina (tag <script>):

    # trazendo dados do CEP de cada anuncio
    regex_cep = r'"zipCode"+:+"([0-9]+)"'
    regex_cep_compile = re.compile(regex_cep)
    regex_cep_iter = regex_cep_compile.finditer(soup_vivareal_js_unicode)

    # iterando sobre o resultado do regex finditer e trazendo cep por anuncio
    for cep in regex_cep_iter:
        cep_vivareal.append(cep.group(1))
        link_maps_cep.append(
            'https://www.google.com/maps/search/?api=1&query=' + regex_cep_compile.findall(str(cep))[0])

    # trazendo dados do codigo do imovel de cada anuncio
    regex_codigo = r'"externalId"+:+"([|A-Z-À-ÿÀ-üç\s\wçãõôê\d\t\n\r\f\v_&0-9-.,‡+%()^$*#+?\040]+)"'
    regex_codigo_compile = re.compile(regex_codigo)
    regex_codigo_iter = regex_codigo_compile.finditer(soup_vivareal_js_unicode)

    # iterando sobre o resultado do regex finditer e trazendo codigo por anuncio
    for codigo in regex_codigo_iter:
        codigo_imovel_vivareal.append(codigo.group(1))

    # trazendo dados do nome do anunciante de cada anuncio (xml)
    regex_anunciante = r'-[0-9-a-z]{12}"+,"name"+:+"+([|A-Za-zÀ-ÿÀ-üç\s\wçãõôê\d\t\n\r\f\v_&0-9-.,‡+%()^$*#+?\040]+)"'
    regex_anunciante_compile = re.compile(regex_anunciante, flags=re.IGNORECASE)
    regex_anunciante_iter = regex_anunciante_compile.finditer(soup_vivareal_js_unicode)

    # iterando sobre o resultado do regex finditer e trazendo codigo por anuncio
    for anunciante in regex_anunciante_iter:
        nome_anunciante_vivareal.append(anunciante.group(1))

    # trazendo dados do telefone do anunciante de cada anuncio
    regex_tel_anunciante = r'"phones"+:+([+[0-9,""]+])'
    regex_tel_anunciante_compile = re.compile(regex_tel_anunciante)
    regex_tel_anunciante_iter = regex_tel_anunciante_compile.finditer(soup_vivareal_js_unicode)

    # iterando sobre o resultado do regex finditer e trazendo codigo por anuncio
    for tel in regex_tel_anunciante_iter:
        tel_anunciante_vivareal.append(tel.group(1))

    ##trazendo dados da latitude do anúncio:
    # regex_lat = r'"lat"+:+[-0-9.]+\.+[0-9]{6}'
    # regex_lat_compile = re.compile(regex_lat)
    # regex_lat_iter = regex_lat_compile.finditer(soup_vivareal_js_unicode)
    #
    ## iterando sobre o resultado do regex finditer e trazendo latitude por anuncio
    # for lat in regex_lat_iter:
    #    latitude_vivareal.append(lat.group(0)[6:])
    #
    #
    ##trazendo dados da longitude do anúncio:
    # regex_lon = r'"lon"+:+[-0-9.]+\.+[0-9]{6}'
    # regex_lon_compile = re.compile(regex_lon)
    # regex_lon_iter = regex_lon_compile.finditer(soup_vivareal_js_unicode)

    # iterando sobre o resultado do regex finditer e trazendo longitude por anuncio
    # for lon in regex_lon_iter:
    #    longitude_vivareal.append(lon.group(0)[6:])


    # trazendo dados do IPTU de cada anuncio
    regex_iptu = r'"yearlyIptu"+:+"([0-9]+)"'
    regex_iptu_compile = re.compile(regex_iptu)
    regex_iptu_iter = regex_iptu_compile.finditer(soup_vivareal_js_unicode)

    # iterando sobre o resultado do regex finditer e trazendo codigo por anuncio
    for iptu in regex_iptu_iter:
        iptu_vivareal.append(iptu.group(1))

    # trazendo dados dos locais próximos de cada anuncio
    regex_proximos = r'"poisList"+:+\[+([|A-Za-zÀ-ÿÀ-üç\s\wçãõôê\d\t\n\r\f\v_&0-9-.,:‡+%()""^$*#+?\040]+)\]'
    regex_proximos_compile = re.compile(regex_proximos)
    regex_proximos_iter = regex_proximos_compile.finditer(soup_vivareal_js_unicode)

    # iterando sobre o resultado do regex finditer e trazendo codigo por anuncio
    for proximo in regex_proximos_iter:
        locais_proximos_vivareal.append(proximo.group(1))

    # trazendo dados da conservação de cada anuncio
    regex_conservacao = r'"listingType"+:+"+([A-Za-zÀ-ÿÀ-üç\s\wçãõôê\d\t\n\r\f\v_]+)"'
    regex_conservacao_compile = re.compile(regex_conservacao)
    regex_conservacao_iter = regex_conservacao_compile.finditer(soup_vivareal_js_unicode)

    # iterando sobre o resultado do regex finditer e trazendo codigo por anuncio
    for conservacao in regex_conservacao_iter:
        conservacao_vivareal.append(conservacao.group(1))

    # trazendo dados da utilização de cada anuncio
    regex_utilizacao = r'"usageTypes"+:+\[+\"+([A-Za-zÀ-ÿÀ-üç\s\wçãõôê\d\t\n\r\f\v_]+)\"+\]'
    regex_utilizacao_compile = re.compile(regex_utilizacao)
    regex_utilizacao_iter = regex_utilizacao_compile.finditer(soup_vivareal_js_unicode)

    # iterando sobre o resultado do regex finditer e trazendo codigo por anuncio
    for utilizacao in regex_utilizacao_iter:
        utilizacao_vivareal.append(utilizacao.group(1))

    # trazendo dados do complemento (apartamento, etc) do endereço de cada anuncio
    regex_complemento = r'"complement"+:+"+([A-Za-zÀ-ÿÀ-üç\s\wçãõôê\d\t\n\r\f\v_&0-9]+)"'
    regex_complemento_compile = re.compile(regex_complemento)
    regex_complemento_iter = regex_complemento_compile.finditer(soup_vivareal_js_unicode)

    # iterando sobre o resultado do regex finditer e trazendo codigo por anuncio
    for complemento in regex_complemento_iter:
        complemento_vivareal.append(complemento.group(1))

    # gerando coordenadas geográficas a partir do LOGRADOURO de cada anúncio, consumindo API GOOGLE GEOCODING

    for logr_geo in address_list_vivareal:
        logr_geo_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + logr_geo + '&key=AIzaSyAScLbiaNZspmdwXhHhGjXHKbJFrGE52gA'
        logr_resp_geo = requests.get(logr_geo_url)
        logr_soup_geo = logr_resp_geo.json()
        if logr_soup_geo['status'] == 'OK':
            latitude_logr_vivareal.append(logr_soup_geo['results'][0]['geometry']['location']['lat'])
            longitude_logr_vivareal.append(logr_soup_geo['results'][0]['geometry']['location']['lng'])
        else:
            latitude_cep_vivareal.append('None')
            longitude_cep_vivareal.append('None')

    # gerando coordenadas geográficas a partir do CEP de cada anúncio, consumindo API GOOGLE GEOCODING


    for cep_geo in cep_vivareal:
        cep_geo_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + cep_geo + '&key=AIzaSyAScLbiaNZspmdwXhHhGjXHKbJFrGE52gA'
        cep_resp_geo = requests.get(cep_geo_url)
        cep_soup_geo = cep_resp_geo.json()
        if cep_soup_geo['status'] == 'OK':
            latitude_cep_vivareal.append(cep_soup_geo['results'][0]['geometry']['location']['lat'])
            longitude_cep_vivareal.append(cep_soup_geo['results'][0]['geometry']['location']['lng'])
        else:
            latitude_cep_vivareal.append('None')
            longitude_cep_vivareal.append('None')

    # armazenando o resultado em um dataframe:
    results_vivareal = {
        'Portal': name_site_vivareal, 'Anunciante': nome_anunciante_vivareal,
        'Contato Anunciante': tel_anunciante_vivareal,
        'Código Anúncio': codigo_imovel_vivareal,
        'Operação': operacao_vivareal,
        'Imóvel': title_list_vivareal,
        'Endereço': address_list_vivareal,
        'Complemento': complemento_vivareal,
        # 'Bairro': bairro_vivareal,
        # 'Bairro/Cidade': cidade_vivareal,
        'Estado': estado_vivareal,
        'CEP': cep_vivareal,
        'Mapa (Lograd.)': link_maps_endereço,
        'Mapa (CEP)': link_maps_cep,
        'Latitude (Lograd.)': latitude_logr_vivareal,
        'Longitude (Lograd.)': longitude_logr_vivareal,
        'Latitude (CEP)': latitude_cep_vivareal,
        'Longitude (CEP)': longitude_cep_vivareal,
        'Área(m2)': area_list_vivareal, 'Preço(R$)': price_list_vivareal,
        'Infraestrutura': equipamentos_vivareal, 'Utilização': utilizacao_vivareal,
        'Condição': conservacao_vivareal,
        'Quartos': bedrooms_list_vivareal,
        'Banheiros': bathroom_list_vivareal, 'Garagem': garages_list_vivareal,
        'Condomínio': condominio_list_vivareal, 'IPTU Anual': iptu_vivareal,
        'Proximidades': locais_proximos_vivareal,
        'Link Anúncio': link_list_vivareal,
    }

    # gerando dataframe invertido na horizontal com resultados preenchendo com 'None' os campos
    # vazios de diferentes tamanhos de coluna:
    df_consulta_vivareal = pd.DataFrame.from_dict(results_vivareal, orient='index')

    # para mostrar o texto completo nos campos sem truncar(...):
    pd.set_option('display.max_colwidth', None)
    pd.options.display.max_columns = None

    # retornando o dataframe resultante de forma transposta para a orientação correta:
    consulta_vivareal = df_consulta_vivareal.transpose()

    # criando a coluna 'Dado'  e aplicando ela como indice do dataframe:
    consulta_vivareal['Dado'] = range(0, len(consulta_vivareal))
    consulta_vivareal.set_index('Dado', inplace=True)

    # convertendo o dataframe em csv e armazenando no disco local
    # para contornar erro ao abrir o dataframe original no streamlit:
    consulta_vivareal_csv = consulta_vivareal.to_csv(r'C:\Users\trindade\Desktop\teste_search_st.csv',
                                                     encoding='utf-8', float_format="%.4f")

    # lendo o csv e convertendo-o em dataframe:
    consulta_vivareal_df = pd.read_csv(r'C:\Users\trindade\Desktop\teste_search_st.csv')

    # mostrando o total de anúncios na página:
    st.write('Total de anúncios de imóveis na pagina: ', len(container_vivareal), 'anúncios!')

    # carregando o dataframe como tabela dinamica do streamlit:
    st.dataframe(consulta_vivareal_df.style.format(formatter={'CEP': "{:.0f}"}))
