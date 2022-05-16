import streamlit as st
import pandas as pd
import pydeck as pdk
#import numpy as np


#obtendo dados a partir de arquivo csv fornecido pelo site do Vivareal
file_vivareal = 'bd_salvador.csv'


# criando uma cache da função e não calcular ela toda vez que chama a função
@st.cache
#definindo a função para alterar o label da coluna de coordenadas
# com os nomes latitude e longitude para lat e lon
def load_data():
    columns = {'Latitude': 'latitude',
               'Longitude': 'longitude'}
    df_vivareal = pd.read_csv(file_vivareal)
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


#criando a barra lateral e nomeando ela
st.sidebar.header('Filtros')

bedroom_min = 0
bedroom_max = 4


#criando uma lista para filtrar numero de quartos
#usando sort_values() do pandas para classificar em ordem alfabetica
bedrooms = df_vivareal.sort_values(by='Quartos').Quartos.unique()
bedrooms_selected = st.sidebar.multiselect('Veja os imóveis pelo número de quartos', bedrooms)

#criando uma lista para selecionar o tipo de imovel
property_types = df_vivareal.sort_values(by='Tipo').Tipo.unique()
property_types_selected = st.sidebar.multiselect('Selecione o tipo de imóvel', property_types)

#criando uma lista para selecionar o bairro do imovel
property_neighborhoods = df_vivareal.sort_values(by='Bairro').Bairro.unique()
property_neighborhoods_selected = st.sidebar.multiselect('Selecione o bairro do imóvel', property_neighborhoods)


#condicional para o caso do multiselect não estar selecionado
#deixar mostrando os bairros no dataframe
if not bedrooms_selected:
    bedrooms_selected = df_vivareal.Quartos.unique()

if not property_types_selected:
    property_types_selected = df_vivareal.Tipo.unique()

if not property_neighborhoods_selected:
    property_neighborhoods_selected = df_vivareal.Bairro.unique()

#mostrando o dataframe dos dados do Vivareal
data_map = df_vivareal[(df_vivareal['Quartos'].isin(bedrooms_selected)) &
                       (df_vivareal['Tipo'].isin(property_types_selected)) &
                       (df_vivareal['Bairro'].isin(property_neighborhoods_selected))]
st.dataframe(data_map)


#criando novo dataframe para exibir dados especificos no mapa (pydeck)
df = df_vivareal[['Item', 'Tipo', 'Bairro', 'latitude', 'longitude', 'Preço/m2', 'Quartos']]
data_map_1 = df[(df['Quartos'].isin(bedrooms_selected)) &
                (df['Tipo'].isin(property_types_selected)) &
                (df['Bairro'].isin(property_neighborhoods_selected))]


#definindo o layer para mostrar no mapa
layer = pdk.Layer(
    "ScatterplotLayer",
    data_map_1,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=60,
    radius_min_pixels=1,
    radius_max_pixels=100,
    line_width_min_pixels=1,
    get_position=['longitude', 'latitude'],
    get_radius="exits_radius",
    get_fill_color=[200, 30, 0],
    get_line_color=[200, 30, 0],
)


#definindo o local da visualização inicial (viewport)
view_state = pdk.ViewState(latitude=-12.975056605825293, longitude=-38.50146502854858,
                           zoom=10, bearing=None, pitch=None)


#criando um checkbox para mostrar/ocultar  mapa dos dados do Vivareal
if st.sidebar.checkbox('Mostrar Mapa'):
    st.markdown('### Mapa de Dados')
    map_vivareal = st.pydeck_chart(pdk.Deck(layers=[layer], map_style='mapbox://styles/mapbox/light-v10',
                  initial_view_state=view_state, height=500, width='100%',
                        views=[pdk.View(type="MapView", controller=True)],
                            tooltip={"text": "{Item}\n{Tipo}\n{Bairro}\nR$ {Preço/m2}/m²\n{latitude} {longitude}"}))
