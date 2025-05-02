import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Mercado - Cuidado Capilar España",
    page_icon="💇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
    <style>
        .main {
            padding: 0rem 1rem;
        }
        .stApp {
            background-color: #f8f9fa;
        }
        .stMetric {
            background-color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .stSidebar {
            background-color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

def cargar_datos():
    """Carga los datos más recientes de competidores"""
    try:
        # Buscar el archivo más reciente en el directorio data
        archivos = [f for f in os.listdir('data') if f.startswith('competidores_espana_')]
        if not archivos:
            return None
            
        ultimo_archivo = max(archivos)
        df = pd.read_csv(os.path.join('data', ultimo_archivo))
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {str(e)}")
        return None

def mostrar_header():
    """Muestra el encabezado del dashboard"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🔍 Análisis de Mercado - Cuidado Capilar España")
        st.markdown("*Datos actualizados: {}*".format(
            datetime.now().strftime("%d/%m/%Y %H:%M")
        ))
    with col2:
        st.image("https://via.placeholder.com/150x80?text=Logo", width=150)

def mostrar_metricas(df):
    """Muestra las métricas principales"""
    st.subheader("📊 Métricas Principales")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Productos",
            f"{len(df):,}",
            "Analizados"
        )
    
    with col2:
        precio_medio = df['price'].mean()
        st.metric(
            "Precio Medio",
            f"{precio_medio:.2f}€",
            "Por producto"
        )
    
    with col3:
        n_marcas = df['brand'].nunique()
        st.metric(
            "Marcas Únicas",
            f"{n_marcas:,}",
            "En el mercado"
        )
    
    with col4:
        rating_medio = df['rating'].mean()
        st.metric(
            "Rating Medio",
            f"{rating_medio:.1f}★",
            "De 5 estrellas"
        )

def mostrar_distribucion_precios(df):
    """Muestra la distribución de precios"""
    st.subheader("💶 Distribución de Precios")
    
    fig = px.histogram(
        df,
        x='price',
        nbins=50,
        title='Distribución de Precios en el Mercado',
        labels={'price': 'Precio (€)', 'count': 'Número de Productos'},
        color_discrete_sequence=['#3498db']
    )
    
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def mostrar_top_marcas(df):
    """Muestra las marcas más populares"""
    st.subheader("🏆 Top Marcas")
    
    top_marcas = df['brand'].value_counts().head(10)
    
    fig = px.bar(
        x=top_marcas.values,
        y=top_marcas.index,
        orientation='h',
        title='Top 10 Marcas por Número de Productos',
        labels={'x': 'Número de Productos', 'y': 'Marca'},
        color_discrete_sequence=['#2ecc71']
    )
    
    fig.update_layout(
        plot_bgcolor='white',
        yaxis={'categoryorder': 'total ascending'}
    )
    
    st.plotly_chart(fig, use_container_width=True)

def mostrar_analisis_ratings(df):
    """Muestra el análisis de ratings"""
    st.subheader("⭐ Análisis de Valoraciones")
    
    col1, col2 = st.columns(2)
    
    with col1:
        rating_por_marca = df.groupby('brand')['rating'].mean().sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=rating_por_marca.values,
            y=rating_por_marca.index,
            orientation='h',
            title='Top 10 Marcas por Rating',
            labels={'x': 'Rating Promedio', 'y': 'Marca'},
            color_discrete_sequence=['#e74c3c']
        )
        
        fig.update_layout(
            plot_bgcolor='white',
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(
            df,
            x='brand',
            y='rating',
            title='Distribución de Ratings por Marca',
            labels={'rating': 'Rating', 'brand': 'Marca'},
            color_discrete_sequence=['#9b59b6']
        )
        
        fig.update_layout(
            plot_bgcolor='white',
            xaxis={'tickangle': 45}
        )
        
        st.plotly_chart(fig, use_container_width=True)

def mostrar_tendencias_precio(df):
    """Muestra las tendencias de precio"""
    st.subheader("📈 Tendencias de Precio")
    
    precio_por_marca = df.groupby('brand').agg({
        'price': ['mean', 'min', 'max']
    }).round(2)
    
    precio_por_marca.columns = ['Precio Medio', 'Precio Mínimo', 'Precio Máximo']
    precio_por_marca = precio_por_marca.sort_values('Precio Medio', ascending=False).head(10)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Precio Medio',
        x=precio_por_marca.index,
        y=precio_por_marca['Precio Medio'],
        marker_color='#3498db'
    ))
    
    fig.add_trace(go.Scatter(
        name='Rango de Precios',
        x=precio_por_marca.index,
        y=precio_por_marca['Precio Máximo'],
        mode='lines',
        line=dict(color='#e74c3c'),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        name='Rango de Precios',
        x=precio_por_marca.index,
        y=precio_por_marca['Precio Mínimo'],
        mode='lines',
        line=dict(color='#2ecc71'),
        fill='tonexty'
    ))
    
    fig.update_layout(
        title='Análisis de Precios por Marca',
        xaxis_title='Marca',
        yaxis_title='Precio (€)',
        plot_bgcolor='white',
        xaxis={'tickangle': 45}
    )
    
    st.plotly_chart(fig, use_container_width=True)

def mostrar_sidebar():
    """Configura y muestra la barra lateral"""
    st.sidebar.title("⚙️ Configuración")
    
    # Filtros
    st.sidebar.subheader("Filtros")
    
    # Rango de precios
    precio_min = st.sidebar.number_input(
        "Precio Mínimo (€)",
        min_value=0.0,
        value=0.0,
        step=1.0
    )
    
    precio_max = st.sidebar.number_input(
        "Precio Máximo (€)",
        min_value=0.0,
        value=1000.0,
        step=1.0
    )
    
    # Rating mínimo
    rating_min = st.sidebar.slider(
        "Rating Mínimo",
        min_value=0.0,
        max_value=5.0,
        value=0.0,
        step=0.5
    )
    
    # Selección de marcas
    marcas_seleccionadas = st.sidebar.multiselect(
        "Marcas",
        options=sorted(df['brand'].unique()),
        default=[]
    )
    
    return {
        'precio_min': precio_min,
        'precio_max': precio_max,
        'rating_min': rating_min,
        'marcas': marcas_seleccionadas
    }

def aplicar_filtros(df, filtros):
    """Aplica los filtros seleccionados al DataFrame"""
    df_filtrado = df.copy()
    
    # Filtrar por precio
    df_filtrado = df_filtrado[
        (df_filtrado['price'] >= filtros['precio_min']) &
        (df_filtrado['price'] <= filtros['precio_max'])
    ]
    
    # Filtrar por rating
    df_filtrado = df_filtrado[df_filtrado['rating'] >= filtros['rating_min']]
    
    # Filtrar por marcas
    if filtros['marcas']:
        df_filtrado = df_filtrado[df_filtrado['brand'].isin(filtros['marcas'])]
    
    return df_filtrado

# Cargar datos
df = cargar_datos()

if df is not None:
    # Mostrar interfaz
    mostrar_header()
    
    # Configurar sidebar y obtener filtros
    filtros = mostrar_sidebar()
    
    # Aplicar filtros
    df_filtrado = aplicar_filtros(df, filtros)
    
    # Mostrar secciones
    mostrar_metricas(df_filtrado)
    
    # Crear dos columnas para los gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        mostrar_distribucion_precios(df_filtrado)
        mostrar_top_marcas(df_filtrado)
    
    with col2:
        mostrar_analisis_ratings(df_filtrado)
        mostrar_tendencias_precio(df_filtrado)
    
    # Mostrar datos raw (opcional, solo para desarrollo)
    if st.sidebar.checkbox("Mostrar datos raw", False):
        st.dataframe(df_filtrado)
else:
    st.error("No se encontraron datos para mostrar. Por favor, ejecute primero el scraper de datos.") 