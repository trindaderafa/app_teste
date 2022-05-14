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

#criando um slider para filtrar numero de quartos
bedrooms = st.sidebar.slider('Veja os imóveis pelo número de quartos', bedroom_min, bedroom_max)

#criando uma lista para selecionar o tipo de imovel
property_types = df_vivareal.Tipo.unique()
property_types_selected = st.sidebar.multiselect('Selecione o tipo de imóvel', property_types)
if not property_types_selected:
    property_types_selected = df_vivareal.Tipo.unique()

#mostrando a tabela dos dados do Vivareal
data_map = df_vivareal[(df_vivareal['Quartos'] == bedrooms) & (df_vivareal['Tipo'].isin(property_types_selected))]
st.dataframe(data_map)

#criando um checkbox para mostrar/ocultar  mapa dos dados do Vivareal
if st.sidebar.checkbox('Mostrar Mapa'):
    st.markdown('### Mapa de Dados')
    map_vivareal = st.map(data_map)


df = data_map

# Define a layer to display on a map
layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=6,
    radius_min_pixels=1,
    radius_max_pixels=100,
    line_width_min_pixels=1,
    get_position=['longitude', 'latitude'],
    get_radius="exits_radius",
    get_fill_color=[25, 74, 215],
    get_line_color=[0, 0, 0],
)

# Set the viewport location
view_state = pdk.ViewState(latitude=-12.975056605825293, longitude=-38.50146502854858, zoom=10, bearing=0, pitch=0)

# Render
r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{Item}\n{Tipo}"})
r.to_html("scatterplot_layer_1.html")
