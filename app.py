import streamlit as st
import requests
import pandas as pd
import plotly.express as px
base="dark"
backgroundColor="#652e69"

st.set_page_config(layout="wide",
                   page_icon="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png",
                   page_title = "Web app Diplomado")

@st.cache
def cargar_datos(filename: str):
    return pd.read_csv(filename)

datos = cargar_datos("cordoba_limpio.csv")
# Sidebar
st.sidebar.image("logo-DANE.png")
st.sidebar.markdown("<p style='text-align: justify;'>Estudio realizado para conocer las condiciones de vida de los hogares del departamento de Córdoba.</p>", unsafe_allow_html=True)
#st.sidebar.markdown("Estudio realizado para conocer las condiciones de vida de los hogares del departamento de Córdoba.")
st.sidebar.markdown("### Selector de opcion para Grafico 2")
opcionPie = st.sidebar.selectbox(label="Servicios basicos", 
                                 options =["descripcion_tipo_vivienda","descripcion_material_pared","descripcion_tipo_servicio_sanitario"])
st.sidebar.markdown("---")
st.sidebar.markdown("Selección de estrato para el análisis del uso de servicios básicos en el departamento de Córdoba.")
OpcE = st.sidebar.number_input("Escoja un estrato", min_value=1, max_value=6)
st.sidebar.markdown("---")
st.markdown("Datos de referencia utilizados para la predicción de calidad de vida de los habitantes del departamento de Córdoba en base al acceso de servicios básicos")
st.markdown("---")
st.write(datos)
st.markdown("---")
st.markdown("Figura 1.")

@st.cache
def graficobarras(datos):
    
    fig = px.bar(
        datos.groupby(["estrato"])
        .sum()
        .reset_index()
        .sort_values(by="total_hogares", ascending=False),
        color_discrete_sequence=["#86C7BE","white"],
        x ="estrato",
        y ="total_hogares"
    )
    return fig
varfig = graficobarras(datos)
st.plotly_chart( 
    varfig , 
    use_container_width=True,  
)
def graficobarras1(datos):
    df=px.data.datos()   
    fig = px.bar(
        datos,  
        x ="estrato",
        y ="servicio_internet",
        color= 'medal'
    )
    return fig
varfig = graficobarras1(datos)
st.plotly_chart( 
    varfig , 
    use_container_width=True,  
)

st.markdown("---")

st.markdown("## Gráfico 2")
@st.cache
def pieFig(df,x):
    sizes = datos[x].value_counts().tolist()
    labels = datos[x].unique()
    return [sizes,labels]
fig = px.pie(datos, 
             values=pieFig(datos,opcionPie)[0], 
             names=pieFig(datos,opcionPie)[1], 
             title='Información Adicional del censo realizado para todos los estratos',
            color_discrete_sequence=px.colors.sequential.Aggrnyl)
st.plotly_chart(fig)
st.markdown("---")
st.write("## Gráficas por estrato")
col1,col2=st.columns(2)
st.write("### Estrato: ", OpcE)
st.write("### Descripción Tipo de vivienda")
st.markdown("Este gráfico muestra el tipo de vivienda para cada hogar encuestado del departamento de Córdoba dependiendo del estrato")
df1 = datos[(datos['estrato'] == OpcE)]
#@st.cache
#def pieFig1(df,x):
#    sizes = df1[x].value_counts().tolist()
#    labels = df1[x].unique()
#    return [sizes,labels]
fig = px.pie(df1, 
             values='estrato', 
             names='descripcion_tipo_vivienda',
             color_discrete_sequence=px.colors.sequential.Aggrnyl)
st.plotly_chart(fig)
st.markdown("---")
#fig = px.pie(datos,
#            values='estrato',
#            names=opcionPie,
#            color_discrete_sequence=px.colors.sequential.Aggrnyl)
#st.plotly_chart(fig)
st.write("### Descripción materiales de la pared")
st.markdown("Este gráfico muestra los materiales de construcción para los hogares del departamento de Córdoba dependiendo del estrato")

fig2 = px.pie(df1, 
             values='estrato', 
             names='descripcion_material_pared',
             color_discrete_sequence=px.colors.sequential.Aggrnyl)
st.plotly_chart(fig2)
st.markdown("---")
st.write("### Descripción del tipo de servicio sanitario")
st.markdown("Este gráfico muestra el acceso de los hogares del departamento de Córdoba al servicio de acceso a sanitarios dependiendo del estrato")
fig2 = px.pie(df1, 
             values='estrato', 
             names='descripcion_tipo_servicio_sanitario',
             color_discrete_sequence=px.colors.sequential.Aggrnyl)
st.plotly_chart(fig2)
