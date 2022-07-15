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

datos = cargar_datos("Cordoba_limpio.csv")
# Sidebar
st.sidebar.image("logo-DANE.png")
st.sidebar.markdown("# Seleccion de estrato, para el departamento de cordoba, en todos los municipios")

st.sidebar.markdown("---")

st.sidebar.markdown("---")
st.header("Exploracion de datos")
st.markdown("---")
st.write("Este proyecto trata de darle una mejor forma de visualización a los datos registrados en el censo nacional realizado")
st.write("por el DANE entidad del estado encargada para estadisticas de nuestro pais, del censo realizado, se tomaron solo datos")
st.write("del departamento de cordoba, para un analisis de nuestra region, algunas de las columnas estudiadas y mostradas en las ")
st.write("siguientes graficas son:")
st.write("Descripcion_tipo_vivienda: Contiene los tipos de lugares que utilizan los cordobeces como residencias.")
st.write("Descripcion_material_pared: Esta columna contiene los elementos de los que estan contruidas las residencias visitadas.")
st.write("Descripcion_tipo_servicio_sanitario: En esta columna podemos encontrar el tipo de conexion del servicio sanitario que ")
st.write("tiene la residencia o si por el contrario no cuenta con el servicio")
st.write("Servicio_internet: siendo cordoba una region en desarrollo tecnologico, usar esta columna nos permite ver que tanto ")
st.write("ha avanzado la region con respecto a la cobertura de los estratos mas bajos de la region")

st.markdown("---")
st.markdown("Figura 1.")
@st.cache
def graficobarras(datos):
    fig = px.bar(
        datos.groupby(["estrato"])
        .sum()
        .reset_index()
        .sort_values(by="total_hogares", ascending=False),
        color_discrete_sequence=["#B0C4DE","white"],
        x ="estrato",
        y ="total_hogares"
    )
    return fig
varfig = graficobarras(datos)
st.plotly_chart( 
    varfig , 
    use_container_width=True,  
)

st.markdown("---")

st.markdown("# Selector de opcion para Grafico 2")
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
             title='Informacion Adicional del censo realizado para todos los estratos',
            color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig, use_container_width=True)

#def graficobarras(datos,opt):
    
 #   fig = px.bar(
       # x = datos([opt]).value_counts().tolist()
        #.mean()
        #.reset_index()
        #.sort_values(by="Consumo_agua", ascending=False),
        #color_discrete_sequence=["#00EAD3","black"],
  #      color = opt,
   #     y ="estrato",
    #    orientation='h'
    #)
    #return fig
#varfig = graficobarras(datos)
#gfapilada = px.bar(datos,
     #              x = "estrato",
    #               y = datos[opcionPie],
   #               color = datos[opcionPie], 
  #                orientation = 'h'
 #                 )
#st.plotly_chart(gfapilada, use_container_width=True)
#def p_simple(df: pd.DataFrame, x: pd.DataFrame, y, N_filter: str):
    #data = df.copy()
    #data = data[data["municipio"]]
 #   fig = px.histogram(datos, x=x, y=y, color_discrete_sequence=px.colors.sequential.Aggrnyl, color='estrato')
  #  return fig


#p, c = p_simple(datos, opcionPie, "total_hogares", "municipio")
#st.plotly_chart(p, use_container_width=True)
st.markdown("---")
OpcE = st.selectbox(label = "Estratos",options =[1,2,3,4,5,6])
st.write("# Graficas por estrato")
st.write("## Estrato: ", OpcE)
col1,col2=st.columns(2)
with col1:
    
    st.write("### Descripcion Tipo de vivienda")
    df1 = datos[(datos['estrato'] == OpcE)]
    fig1 = px.pie(df1, 
             values='estrato', 
             names='descripcion_tipo_vivienda',
             color_discrete_sequence=px.colors.sequential.ice)

    st.plotly_chart(fig1,use_container_width=True)

st.markdown("---")

with col2:
    st.write("### Descripcion del tipo de servicio sanitario")
    fig3 = px.pie(df1, 
             values='estrato', 
             names='descripcion_tipo_servicio_sanitario',
             color_discrete_sequence=px.colors.sequential.Plasma)
    st.plotly_chart(fig3) 
    
st.markdown("---")
def pFig(df,x):
    sizes = df1[x].value_counts().tolist()
    labels = df1[x].unique()
    return [sizes,labels]
fig3 = px.bar(df1,  x= pFig(df1,"descripcion_material_pared")[1] ,y=pFig(df1,"descripcion_material_pared")[0]  ,color_discrete_sequence=["#86C7BE"],
              title="TIpo de materiales usados en viviendas y conteo de los mismos por estrato escogido")
st.plotly_chart(fig3, use_container_width=True)

st.write("---")

E = st.selectbox(
    label = "Estrato", options=[1,2,3,4,5,6])
dfE = datos[(datos['estrato'] == E)]
fig4 = px.histogram(dfE, x="servicio_internet",color_discrete_sequence=["#86C7BE"])
st.plotly_chart(fig4,use_container_width=True)
st.write("De la anterior grafica destacamos los siguiente: para entender mejor el valor 1 significa que la residencia cuenta con servicio de internet")
st.write("el valor 2 significa que NO tiene servicio de internet, y el valor  9 el comodin NO informa.")





#fig4 = px.bar(datos, x="estrato", y=datos['servicio_internet']==1.0, color="servicio_internet", title="Graficas de internet")
#st.plotly_chart(fig4)