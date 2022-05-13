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
    columns = {'Latitude': 'lat',
               'Longitude': 'lon'}
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

price_min = 10000
price_max = 12000

#criando um slider para filtrar preços de aluguel
price = st.sidebar.slider('Veja os imóveis pelo valor de mercado', price_min, price_max)

#criando uma lista para selecionar o tipo de imovel
property_types = df_vivareal.Tipo.unique()
property_types_selected = st.sidebar.multiselect('Selecione o tipo de imóvel', property_types)
if not property_types_selected:
    property_types_selected = df_vivareal.Tipo.unique()

#mostrando a tabela dos dados do Vivareal
data_map = df_vivareal[(df_vivareal['Preço(R$)'] == price) & (df_vivareal['Tipo'].isin(property_types_selected))]
st.dataframe(data_map)

#criando um checkbox para mostrar/ocultar  mapa dos dados do Vivareal
if st.sidebar.checkbox('Mostrar Mapa'):
    st.markdown('### Mapa de Dados')
    map_vivareal = st.map(data_map)


#criando um segundo mapa para mostrar grafico de preços de mercado
#titulo do mapa
st.markdown('### Mapa de Preços de Mercado')
#usando biblioteca pydeck para gerar o mapa
st.pydeck_chart(pdk.Deck(
     #estilo do mapa
     map_style='mapbox://styles/mapbox/light-v9',
     #visualização padrão quando carregar o mapa (Madrid)
     initial_view_state={
         "latitude":-12.975056605825293,
         "longitude":-38.50146502854858,
         "zoom":10,
         "pitch":0,
        },
     #visualização dos preços a partir das coordenadas
     layers=[
         pdk.Layer(
            'HexagonLayer',
            #carregando o arquivo em csv
            data=file_vivareal,
            #coordenadas tem que ser no mesmo nome da coluna do csv
            get_position=['longitude', 'latitude'],
            radius=35,
            elevation_scale=4,
            elevation_range=[price_min, price_max],
            pickable=True,
            extruded=True,
         ),

     ],
 ))
