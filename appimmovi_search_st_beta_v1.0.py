import streamlit as st
import pandas as pd
import pydeck as pdk
#import numpy as np


#obtendo dados a partir de arquivo csv fornecido pelo site do Vivareal
file_vivareal = 'bd_salvador_9.csv'


# criando uma cache da função e não calcular ela toda vez que chama a função
@st.cache
#definindo a função para alterar o label da coluna de coordenadas
# com os nomes latitude e longitude para lat e lon
def load_data():
    columns = {'Latitude': 'latitude',
               'Longitude': 'longitude'}
    #lendo o arquivo csv gerado pelo Excel e informado separador e codificação
    df_vivareal = pd.read_csv(file_vivareal, sep=';', encoding='ansi')
    df_vivareal = df_vivareal.rename(columns=columns)
    return df_vivareal


#Chamando a função recém criada e carregando os dados em um dataframe
df_vivareal = load_data()


#criando os rótulos de texto da pagina
st.title('Appimmovi Search (beta)')
st.markdown(
    """
    Pesquise elementos comparativos para sua avaliação de imóveis
    """
)


#criando uma lista para selecionar o tipo de imovel
property_types = df_vivareal['TipoImovel'].sort_values().unique()
property_types_selected = st.sidebar.multiselect('Selecione o Tipo de imóvel',
                                                 property_types, key='type_selected')

#criando uma lista para selecionar o logradouro do imovel
property_address = df_vivareal['Logradouro'].sort_values().unique()
property_address_selected = st.sidebar.multiselect('Logradouro do imóvel', property_address)

#criando uma lista para selecionar o bairro do imovel
property_neighborhoods = df_vivareal['Bairro'].sort_values().unique()
property_neighborhoods_selected = st.sidebar.multiselect('Selecione o bairro do imóvel',
                                                         property_neighborhoods, key='neighborhoods_selected')

#criando uma lista para filtrar numero de quartos
#usando sort_values() do pandas para classificar em ordem alfabetica
bedrooms = df_vivareal['Quarto'].sort_values().unique()
bedrooms_selected = st.sidebar.multiselect('Número de quartos', bedrooms)

#condicional para o caso do multiselect não estar selecionado
#deixar mostrando os bairros no dataframe
if not property_types_selected:
    property_types_selected = df_vivareal.TipoImovel.unique()

if not property_address_selected:
    property_address_selected = df_vivareal.Logradouro.unique()

if not property_neighborhoods_selected:
    property_neighborhoods_selected = df_vivareal.Bairro.unique()

if not bedrooms_selected:
    bedrooms_selected = df_vivareal.Quarto.unique()

#mostrando o dataframe dos dados do Vivareal
data_map = df_vivareal[
                       (df_vivareal['TipoImovel'].isin(property_types_selected)) &
                       (df_vivareal['Logradouro'].isin(property_address_selected)) &
                       (df_vivareal['Bairro'].isin(property_neighborhoods_selected)) &
                       (df_vivareal['Quarto'].isin(bedrooms_selected))
                       ]

#criando CSS para não mostrar  o index padrão
#do dataframe do streamlit
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """

# Injetando o CSS no dataframe através de markdown
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
st.dataframe(data_map)


#criando novo dataframe para exibir dados especificos no mapa (pydeck)
df = df_vivareal[['Dado', 'TipoImovel', 'Bairro', 'Logradouro', 'latitude', 'longitude', 'Preço/m2', 'Quarto']]
data_map_1 = df[
                       (df['TipoImovel'].isin(property_types_selected)) &
                       (df['Logradouro'].isin(property_address_selected)) &
                       (df['Bairro'].isin(property_neighborhoods_selected)) &
                       (df['Quarto'].isin(bedrooms_selected))
                       ]


#definindo o local da visualização inicial (viewport)
view_state = pdk.ViewState(latitude=-12.975056605825293, longitude=-38.50146502854858,
                           zoom=10, bearing=None, pitch=None)

#definindo o layer para mostrar no mapa
layer = pdk.Layer(
    "ScatterplotLayer",
    data_map_1,
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


#criando um checkbox para mostrar/ocultar  mapa dos dados do Vivareal
if st.sidebar.checkbox('Mostrar Mapa'):
    st.markdown('### Mapa de Imóveis')
    #definindo o mapa para apenas mostrar os dados
    # se o tipo de imovel for selecionado, usando o
    # parametro 'key' do multiselect
    if st.session_state['neighborhoods_selected']:
        map_vivareal = st.pydeck_chart(pdk.Deck(layers=[layer], map_style='mapbox://styles/mapbox/light-v10',
                      initial_view_state=view_state, height=500, width='100%',
                            views=[pdk.View(type="MapView", controller=True)],
                                tooltip={"text": "Dado: {Dado}\nTipo: {TipoImovel}\nBairro: {Bairro}"
                                                 "\nPreço unitário: R$ {Preço/m2}/m²\nCoordenadas: {latitude} {longitude}"}))
    else:
        map_vivareal = st.pydeck_chart(pdk.Deck(layers=None, map_style='mapbox://styles/mapbox/light-v10',
                                                initial_view_state=view_state, height=500, width='100%',
                                                views=[pdk.View(type="MapView", controller=True)],
                                                tooltip={"text": "Dado: {Dado}\nTipo: {TipoImovel}\nBairro: {Bairro}"
                                                                 "\nPreço unitário: R$ {Preço/m2}/m²\nCoordenadas: {latitude} {longitude}"}))

