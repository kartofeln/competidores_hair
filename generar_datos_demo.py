import pandas as pd
import numpy as np
from datetime import datetime
import os

def generar_datos_demo():
    """Genera datos de ejemplo para el dashboard"""
    print("Generando datos de demostración...")
    
    # Crear directorio de datos si no existe
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Marcas populares en el mercado español
    marcas = [
        'Loreal', 'Garnier', 'Pantene', 'Head & Shoulders', 'Schwarzkopf',
        'Wella', 'Tresemme', 'Syoss', 'Nivea', 'Elvive', 'Herbal Essences',
        'Dove', 'Nioxin', 'Kerastase', 'Redken'
    ]
    
    # Tipos de productos
    tipos = [
        'Champú', 'Acondicionador', 'Mascarilla', 'Aceite', 'Tratamiento',
        'Serum', 'Spray', 'Gel', 'Crema', 'Tónico'
    ]
    
    # Generar datos aleatorios
    n_productos = 500
    datos = {
        'product_id': range(1, n_productos + 1),
        'title': [f"{np.random.choice(tipos)} {np.random.choice(marcas)}" for _ in range(n_productos)],
        'brand': [np.random.choice(marcas) for _ in range(n_productos)],
        'price': np.random.uniform(2, 50, n_productos).round(2),
        'rating': np.random.uniform(3, 5, n_productos).round(1),
        'reviews': np.random.randint(10, 1000, n_productos),
        'source': np.random.choice(['Google Shopping', 'Amazon'], n_productos),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Crear DataFrame
    df = pd.DataFrame(datos)
    
    # Guardar datos
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archivo = f'data/competidores_espana_{timestamp}.csv'
    df.to_csv(archivo, index=False)
    
    print(f"✓ Datos de demostración generados y guardados en: {archivo}")
    print(f"✓ Total de productos: {n_productos}")
    print(f"✓ Marcas incluidas: {len(marcas)}")
    print(f"✓ Tipos de productos: {len(tipos)}")
    
    return archivo

if __name__ == "__main__":
    generar_datos_demo() 