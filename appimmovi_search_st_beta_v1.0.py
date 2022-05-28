import streamlit as st
import pandas as pd
import pydeck as pdk
#import numpy as np


#obtendo dados a partir de arquivo csv fornecido pelo site do Vivareal
file_vivareal = 'bd_salvador_25.csv'


#definindo a função para alterar o label da coluna de coordenadas
# com os nomes latitude e longitude para lat e lon
# criando uma cache da função e não calcular ela toda vez que chama a função
# e adicionando um ttl pra armazenar o cache por no maximo 24h
@st.cache(ttl=24*3600)
def load_data():
    columns = {'Latitude': 'latitude',
               'Longitude': 'longitude'}
    #lendo o arquivo csv gerado pelo Excel e informado separador e codificação
    df_vivareal = pd.read_csv(file_vivareal, sep=';', encoding='ansi', index_col='Dado')
    df_vivareal = df_vivareal.rename(columns=columns)
    return df_vivareal


#Chamando a função recém criada e carregando os dados em um dataframe
df_vivareal = load_data()

#criando os rótulos de texto da pagina
st.title('Appimmovi Search (beta)')
st.write(
    """
    Pesquise elementos comparativos para sua avaliação de imóveis
    """
)
st.caption('Última atualização: 25 de Maio de 2022')

#criando uma lista para selecionar o tipo de imovel
#usando sort_values() do pandas para classificar em ordem alfabetica
property_types = df_vivareal['TipoImovel'].sort_values().unique()
property_types_selected = st.sidebar.multiselect('Selecione o Tipo de imóvel',
                                                 property_types, key='type_selected')

#criando uma lista para selecionar o Estado do imovel
property_state = df_vivareal['Estado'].sort_values().unique()
property_state_selected = st.sidebar.multiselect('Selecione o Estado',
                                                         property_state, key='state_selected')

#criando uma lista para selecionar a cidade do imovel
property_city = df_vivareal['Cidade'].sort_values().unique()
property_city_selected = st.sidebar.multiselect('Selecione a Cidade',
                                                         property_city, key='city_selected')

#criando uma lista para selecionar o bairro do imovel
property_neighborhoods = df_vivareal['Bairro'].sort_values().unique()
property_neighborhoods_selected = st.sidebar.multiselect('Selecione o Bairro',
                                                         property_neighborhoods, key='neighborhoods_selected')

#criando uma lista para selecionar o logradouro do imovel
property_address = df_vivareal['Logradouro'].sort_values().unique()
property_address_selected = st.sidebar.multiselect('Selecione o Logradouro (opcional)',
                                                   property_address, key='address_selected')

#criando uma lista para filtrar numero de quartos e vagas de garagem
#usando colunas no sidebar para os controles aparecerem lado a lado
col_data_3, col_data_4 = st.sidebar.columns(2)

with col_data_3:
    bedrooms = df_vivareal['Quarto'].sort_values().unique()
    bedrooms_selected = st.multiselect('Número de quartos', bedrooms)

with col_data_4:
    garage = df_vivareal['VagaGaragem'].sort_values().unique()
    garage_selected = st.multiselect('Vagas de Garagem', garage)


#condicional para o caso do multiselect não estar selecionado
#ele continuar mostrando o dataframe
if not property_types_selected:
    property_types_selected = df_vivareal.TipoImovel.unique()

if not property_address_selected:
    property_address_selected = df_vivareal.Logradouro.unique()

if not property_neighborhoods_selected:
    property_neighborhoods_selected = df_vivareal.Bairro.unique()

if not property_city_selected:
    property_city_selected = df_vivareal.Cidade.unique()

if not property_state_selected:
    property_state_selected = df_vivareal.Estado.unique()

if not bedrooms_selected:
    bedrooms_selected = df_vivareal.Quarto.unique()

if not garage_selected:
    garage_selected = df_vivareal.VagaGaragem.unique()

#criando o dataframe dos dados do Vivareal
data_table = df_vivareal[
                       (df_vivareal['TipoImovel'].isin(property_types_selected)) &
                       (df_vivareal['Logradouro'].isin(property_address_selected)) &
                       (df_vivareal['Bairro'].isin(property_neighborhoods_selected)) &
                       (df_vivareal['Cidade'].isin(property_city_selected)) &
                       (df_vivareal['Estado'].isin(property_state_selected)) &
                       (df_vivareal['Quarto'].isin(bedrooms_selected)) &
                       (df_vivareal['VagaGaragem'].isin(garage_selected))
                       ]


#criando caixas de texto para filtrar por area minima e maxima
#criando variaveis de area minima e maxima
area_min = st.sidebar.number_input('Area minima', value=0)
area_max = st.sidebar.number_input('Area maxima', value=0)
#criando variavel para filtrar a area de acordo com o valor
#digitado nas caixas de texto de area
data_table_area = data_table[data_table['Área'].between(area_min, area_max)]

#condicional para mostrar o as 100 primeiras linhas
#do dataframe de acordo com as areas digitadas
#usando 'write' para mostrar o dataframe como tabela
if (area_min == 0) or (area_max == 0):
    #mostrando o dataframe sem filtrar area
    st.write(data_table.head(100))
elif (area_min > 0) or (area_max > 0):
    #mostrando dataframe com area filtrada
    st.write(data_table_area.head(100))


#criando variaveis para contagem dos dados localizados
#e para definir quantidade de dados que podem ser exportados
count_data = data_table
count_data_area = data_table_area

#************************************#
#preparando variavel para exportação das 100 primeiras
#linhas do dataframe (depois sera ajustado por caixa de texto
export_data = data_table.head(100)

#criando layout de coluna para mostrar controles na horizontal
col_data_5, col_data_6 = st.columns(2)

#inserindo checkbox à primeira coluna (esquerda)
with col_data_5:
    # criando um checkbox para mostrar/ocultar  mapa dos dados do Vivareal
    check_map = st.checkbox('Mostrar no Mapa', disabled=False)

#criando condicional para mostrar quantos dados foram localizados
#de acordo com o tipo/logradouro e bairro que foram selecionados no filtro
if (
            (st.session_state['type_selected'] and st.session_state['neighborhoods_selected']) or
            (st.session_state['type_selected'] and st.session_state['address_selected'])
        ):
    # inserindo checkbox à segunda coluna (direita)
    with col_data_6:
        if (area_min == 0) or (area_max == 0):
            st.write('Localizamos ', len(count_data), 'dados para este tipo de imóvel.')
        elif (area_min > 0) or (area_max > 0):
            st.write('Localizamos ', len(count_data_area), 'dados para este tipo de imóvel.')


#criando novo dataframe para exibir dados especificos no mapa (pydeck)
df = df_vivareal[['TipoImovel', 'Área', 'Bairro', 'Logradouro', 'Cidade', 'Estado',
                  'latitude', 'longitude', 'Preçototal', 'PreçoUnitario', 'Quarto', 'VagaGaragem']]

#criando a coluna 'Dado' para usar no mapa após ter transformado ela
#no indice do dataframe original
df['Dado'] = range(1, len(df)+1)

data_map = df[
                        (df['TipoImovel'].isin(property_types_selected)) &
                        (df['Logradouro'].isin(property_address_selected)) &
                        (df['Bairro'].isin(property_neighborhoods_selected)) &
                        (df['Cidade'].isin(property_city_selected)) &
                        (df['Estado'].isin(property_state_selected)) &
                        (df['Quarto'].isin(bedrooms_selected)) &
                        (df['VagaGaragem'].isin(garage_selected))
                           ]

#definindo o local da visualização inicial (viewport)
view_state = pdk.ViewState(latitude=-12.975056605825293, longitude=-38.50146502854858,
                           zoom=10, bearing=None, pitch=None)

#definindo o layer para mostrar no mapa

data_map_area = data_map[data_map['Área'].between(area_min, area_max)]

if (area_min == 0) or (area_max == 0):
    # mostrando o mapa sem filtrar area
    layer = pdk.Layer(
        "ScatterplotLayer",
        data_map,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=40,
        radius_min_pixels=1,
        radius_max_pixels=100,
        line_width_min_pixels=1,
        get_position=['longitude', 'latitude'],
        get_radius="exits_radius",
        get_fill_color=[200, 30, 0],
        get_line_color=[200, 30, 0],
    )

elif (area_min > 0) or (area_max > 0):
    # mostrando mapa com area filtrada
    layer = pdk.Layer(
        "ScatterplotLayer",
        data_map_area,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=40,
        radius_min_pixels=1,
        radius_max_pixels=100,
        line_width_min_pixels=1,
        get_position=['longitude', 'latitude'],
        get_radius="exits_radius",
        get_fill_color=[200, 30, 0],
        get_line_color=[200, 30, 0],
    )


if check_map:
    st.markdown('### Mapa de Imóveis')
    #definindo o mapa para apenas mostrar os dados
    # se o tipo de imovel for selecionado, usando o
    # parametro 'key' do multiselect
    if (
            (st.session_state['type_selected'] and st.session_state['neighborhoods_selected']) or
            (st.session_state['type_selected'] and st.session_state['address_selected'])
        ):
        map_vivareal = st.pydeck_chart(pdk.Deck(layers=[layer], map_style='mapbox://styles/mapbox/light-v10',
                      initial_view_state=view_state, height=500, width='100%',
                            views=[pdk.View(type="MapView", controller=True)],
                                tooltip={"text": "Dado: {Dado}\nTipo: {TipoImovel}\nBairro: {Bairro}"
                                "\nÁrea: {Área}m²\nPreço total: {Preçototal}\nPreço unitário: R$ {PreçoUnitario}/m²"
                                                 "\nCoordenadas: {latitude} {longitude}"}))
    else:
        map_vivareal = st.pydeck_chart(pdk.Deck(layers=None, map_style='mapbox://styles/mapbox/light-v10',
                        initial_view_state=view_state, height=500, width='100%',
                        views=[pdk.View(type="MapView", controller=True)],
                        tooltip={"text": "Dado: {Dado}\nTipo: {TipoImovel}\nBairro: {Bairro}"
                             "\nÁrea: {Área}m²\nPreço total: {Preçototal}\nPreço unitário: R$ {PreçoUnitario}/m²"
                                                 "\nCoordenadas: {latitude} {longitude}"}))


