import pandas as pd
import os
from datetime import datetime
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def cargar_datos_competidores():
    """Carga los datos de competidores desde el archivo más reciente"""
    try:
        # Buscar el archivo más reciente en la carpeta data
        archivos = [f for f in os.listdir('data') if f.startswith('competidores_espana_')]
        if not archivos:
            logging.warning("No se encontraron archivos de datos de competidores")
            return None
            
        archivo_mas_reciente = max(archivos, key=lambda x: os.path.getctime(os.path.join('data', x)))
        ruta_archivo = os.path.join('data', archivo_mas_reciente)
        
        # Cargar datos
        df = pd.read_csv(ruta_archivo)
        logging.info(f"Datos cargados correctamente desde {ruta_archivo}")
        return df
        
    except Exception as e:
        logging.error(f"Error al cargar datos de competidores: {str(e)}")
        return None

def obtener_metricas_principales(df):
    """Calcula las métricas principales de los competidores"""
    if df is None or df.empty:
        return None
        
    try:
        metricas = {
            'total_competidores': len(df),
            'marcas_unicas': df['marca'].nunique(),
            'precio_promedio': df['precio'].mean(),
            'precio_minimo': df['precio'].min(),
            'precio_maximo': df['precio'].max(),
            'rating_promedio': df['rating'].mean(),
            'top_marcas': df['marca'].value_counts().head(5).to_dict(),
            'top_vendedores': df['vendedor'].value_counts().head(5).to_dict()
        }
        return metricas
    except Exception as e:
        logging.error(f"Error al calcular métricas: {str(e)}")
        return None

def obtener_distribucion_precios(df):
    """Calcula la distribución de precios"""
    if df is None or df.empty:
        return None
        
    try:
        # Crear rangos de precios
        bins = [0, 10, 20, 30, 40, 50, float('inf')]
        labels = ['0-10€', '10-20€', '20-30€', '30-40€', '40-50€', '50€+']
        
        df['rango_precio'] = pd.cut(df['precio'], bins=bins, labels=labels)
        distribucion = df['rango_precio'].value_counts().sort_index().to_dict()
        
        return distribucion
    except Exception as e:
        logging.error(f"Error al calcular distribución de precios: {str(e)}")
        return None

def obtener_top_productos(df, n=10):
    """Obtiene los productos más populares"""
    if df is None or df.empty:
        return None
        
    try:
        # Agrupar por producto y calcular métricas
        top_productos = df.groupby('producto').agg({
            'precio': 'mean',
            'rating': 'mean',
            'reviews': 'sum'
        }).sort_values('reviews', ascending=False).head(n)
        
        return top_productos
    except Exception as e:
        logging.error(f"Error al obtener top productos: {str(e)}")
        return None 