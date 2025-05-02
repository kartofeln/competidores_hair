# Shopping Hair & Skin - Análisis de Competidores

Aplicación web para el análisis de competidores en el mercado de cuidado capilar y de la piel en España.

## Características

- Dashboard interactivo con Streamlit
- Extracción de datos de competidores desde múltiples fuentes
- Análisis de precios, productos y tendencias del mercado
- Visualización de datos con gráficos interactivos
- Filtros dinámicos para análisis específico

## Instalación Local

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/shopping-hair-skin.git
cd shopping-hair-skin
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar credenciales:
- Copiar `.env.example` a `.env`
- Rellenar las credenciales necesarias en `.env`

5. Ejecutar la aplicación:
```bash
streamlit run dashboard_competidores.py
```

## Despliegue en Render

1. Crear una cuenta en [Render](https://render.com)
2. Conectar tu repositorio de GitHub
3. Crear un nuevo servicio Web Service
4. Configurar el servicio con los siguientes parámetros:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run dashboard_competidores.py --server.port $PORT`
   - Environment Variables: Configurar las variables de entorno necesarias

## Estructura del Proyecto

```
shopping-hair-skin/
├── data/                  # Datos de competidores
├── src/                   # Código fuente
│   ├── dashboard_competidores.py
│   ├── obtener_datos_dataforseo.py
│   └── generar_datos_demo.py
├── requirements.txt       # Dependencias
├── render.yaml           # Configuración de Render
├── .env.example          # Ejemplo de variables de entorno
└── README.md             # Documentación
```

## Seguridad

- Las credenciales se manejan a través de variables de entorno
- Los archivos sensibles están excluidos del control de versiones
- Se recomienda usar HTTPS para el despliegue en producción

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 