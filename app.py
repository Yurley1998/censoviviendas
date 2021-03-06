import streamlit as st
import requests
import pandas as pd
import plotly.express as px
base="dark"
backgroundColor="#652e69"

st.set_page_config(layout="wide",
                   page_icon="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png",
                   page_title = "Web app Diplomado")

@st.cache(allow_output_mutation=True)
def cargar_datos(filename: str):
    return pd.read_csv(filename)

datos = cargar_datos("cordoba_limpio.csv")
# Sidebar
st.sidebar.image("logo-DANE.png")
st.sidebar.markdown("---")
st.sidebar.markdown("<p style='text-align: justify;'>Estudio realizado para conocer las condiciones de vida de los hogares del departamento de Córdoba.</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.markdown("## Exploración de datos")
st.markdown("---")
st.markdown("<p style='text-align: justify;'>Este proyecto trata de darle una mejor forma de visualización a los datos registrados en el censo nacional realizado por el DANE entidad del estado encargada para estadisticas de nuestro pais, del censo realizado, se tomaron solo datos del departamento de cordoba, para un analisis de nuestra region, algunas de las columnas estudiadas y mostradas en las siguientes graficas son: </p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: justify;'>Descripcion_tipo_vivienda: Contiene los tipos de residencias de cada hogar encuestado.</p>",unsafe_allow_html=True)
st.markdown("<p style='text-align: justify;'>Descripcion_material_pared: Esta columna contiene los elementos de los que estan contruidas las residencias visitadas.</p>",unsafe_allow_html=True)
st.markdown("<p style='text-align: justify;'>Descripcion_tipo_servicio_sanitario: En esta columna podemos encontrar el tipo de conexion del servicio sanitario que tiene la residencia o si por el contrario no cuenta con el servicio</p>",unsafe_allow_html=True)
st.markdown("<p style='text-align: justify;'>Servicio_internet: siendo cordoba una region en desarrollo tecnologico, usar esta columna nos permite ver que tanto ha avanzado la region con respecto a la cobertura de los estratos mas bajos de la region</p>",unsafe_allow_html=True)

st.markdown("---")
@st.cache
def graficobarras(datos):
    fig = px.bar(
        datos.groupby(["estrato"])
        .sum()
        .reset_index()
        .sort_values(by="total_hogares", ascending=False),
        color_discrete_sequence=["#86C7BE","white"],
        x ="estrato",
        y ="total_hogares",
        width=400,
        title="Gráfico de estrato por hogares"
        
    )
    return fig
varfig = graficobarras(datos)
st.plotly_chart( 
    varfig , 
    use_container_width=True,  
)

st.markdown("---")

st.markdown("Selección de variables para conocer las condiciones de vida de los hogares del departamento de Córdoba.")
opcionPie = st.selectbox(label="", 
                                 options =["descripcion_tipo_vivienda","descripcion_material_pared","descripcion_tipo_servicio_sanitario"])
@st.cache
def pieFig(df,x):
    sizes = datos[x].value_counts().tolist()
    labels = datos[x].unique()
    return [sizes,labels]
fig = px.pie(datos, 
             values=pieFig(datos,opcionPie)[0], 
             names=pieFig(datos,opcionPie)[1], 
             title='Descripción de hogares',
            color_discrete_sequence=px.colors.sequential.Aggrnyl)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("A continuación se muestra el comportamiento de las variables descriptivas de las condiciones de los hogares teniendo en cuenta el estrato seleccionado")
OpcE = st.selectbox(label = "Selección de estratos",options =[1,2,3,4,5,6])
st.write("Estrato: ", OpcE)
col1,col2=st.columns(2)
with col1:
    
    df1 = datos[(datos['estrato'] == OpcE)]
    fig1 = px.pie(df1, 
             values='estrato', 
             names='descripcion_tipo_vivienda',
             color_discrete_sequence=px.colors.sequential.Aggrnyl,
             title="Descripción del tipo vivienda")

    st.plotly_chart(fig1,use_container_width=True)
with col2:
    fig3 = px.pie(df1, 
             values='estrato', 
             names='descripcion_tipo_servicio_sanitario',
             color_discrete_sequence=px.colors.sequential.Aggrnyl,
             title="Descripción del tipo sanitario",
             width=580)
    st.plotly_chart(fig3)     
st.markdown("---")
def pFig(df,x):
    sizes = df1[x].value_counts().tolist()
    labels = df1[x].unique()
    return [sizes,labels]
fig3 = px.bar(df1,  x= pFig(df1,"descripcion_material_pared")[1] ,y=pFig(df1,"descripcion_material_pared")[0]  ,color_discrete_sequence=["#86C7BE"],
              title="Tipo de materiales usados en viviendas y conteo de los mismos por estrato escogido")
st.plotly_chart(fig3, use_container_width=True)

st.write("---")
st.markdown("A continuación se muestra la relación de los hogares de Córdoba que cuentan con acceso al servicio de internet")
E = st.selectbox(
    label = "Selección de estrato", options=[1,2,3,4,5,6])
dfE = datos[(datos['estrato'] == E)]
fig4 = px.histogram(dfE, x="servicio_internet",color_discrete_sequence=["#86C7BE"], width=500)
st.plotly_chart(fig4,use_container_width=True)
st.write("De la anterior grafica destacamos los siguiente: para entender mejor el valor 1 significa que la residencia cuenta con servicio de internet")
st.write("el valor 2 significa que NO tiene servicio de internet, y el valor  9 el comodin NO informa.")





#fig4 = px.bar(datos, x="estrato", y=datos['servicio_internet']==1.0, color="servicio_internet", title="Graficas de internet")
#st.plotly_chart(fig4)
