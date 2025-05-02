import requests
import base64
import json
import pandas as pd
from datetime import datetime
import os
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataForSEOClient:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = 'https://api.dataforseo.com/v3'
        self.headers = {
            'Authorization': f'Basic {base64.b64encode(f"{username}:{password}".encode()).decode()}',
            'Content-Type': 'application/json'
        }

    def buscar_competidores(self, keyword, location_code=2724, language_code='es', limit=100):
        """Busca competidores para una palabra clave específica"""
        endpoint = f"{self.base_url}/serp/google/organic/live/advanced"
        
        data = [{
            "keyword": keyword,
            "location_code": location_code,  # 2724 = España
            "language_code": language_code,
            "depth": limit,
            "device": "desktop",
            "os": "windows"
        }]
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            if result['status_code'] == 20000:
                return self._procesar_resultados(result['tasks'][0]['result'][0]['items'])
            else:
                logging.error(f"Error en la API: {result['status_message']}")
                return None
                
        except Exception as e:
            logging.error(f"Error al buscar competidores: {str(e)}")
            return None

    def _procesar_resultados(self, items):
        """Procesa los resultados de la API en un formato adecuado"""
        competidores = []
        
        for item in items:
            if item.get('type') == 'organic':
                competidor = {
                    'dominio': item.get('domain', ''),
                    'titulo': item.get('title', ''),
                    'url': item.get('url', ''),
                    'posicion': item.get('rank_absolute', 0),
                    'descripcion': item.get('description', ''),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                competidores.append(competidor)
        
        return pd.DataFrame(competidores)

def obtener_datos_competidores():
    """Función principal para obtener datos de competidores"""
    print("\n=== Obteniendo datos de competidores desde DataForSEO ===")
    
    # Verificar credenciales
    if not os.path.exists('config_credentials.json'):
        print("❌ No se encontró el archivo de credenciales")
        print("Por favor, crea el archivo config_credentials.json con tus credenciales de DataForSEO")
        return None
    
    try:
        with open('config_credentials.json', 'r') as f:
            credenciales = json.load(f)
            
        if 'dataforseo' not in credenciales:
            print("❌ No se encontraron credenciales de DataForSEO")
            return None
            
        username = credenciales['dataforseo']['username']
        password = credenciales['dataforseo']['password']
        
        # Crear cliente
        client = DataForSEOClient(username, password)
        
        # Palabras clave para buscar
        keywords = [
            "champú anticaída",
            "mascarilla hidratante cabello",
            "tratamiento capilar profesional",
            "aceite capilar",
            "serum reparador cabello"
        ]
        
        # Obtener datos para cada keyword
        todos_competidores = []
        
        for keyword in keywords:
            print(f"\nBuscando competidores para: {keyword}")
            df = client.buscar_competidores(keyword)
            
            if df is not None:
                df['keyword'] = keyword
                todos_competidores.append(df)
                print(f"✓ Encontrados {len(df)} competidores")
            else:
                print("❌ No se pudieron obtener datos")
        
        if todos_competidores:
            # Combinar todos los resultados
            df_final = pd.concat(todos_competidores, ignore_index=True)
            
            # Guardar datos
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            archivo = f'data/competidores_espana_{timestamp}.csv'
            
            if not os.path.exists('data'):
                os.makedirs('data')
                
            df_final.to_csv(archivo, index=False)
            print(f"\n✓ Datos guardados en: {archivo}")
            print(f"✓ Total de competidores encontrados: {len(df_final)}")
            
            return archivo
        else:
            print("\n❌ No se pudieron obtener datos de competidores")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    obtener_datos_competidores() 