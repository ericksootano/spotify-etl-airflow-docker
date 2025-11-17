import os

# Configuración usando variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/airflow")
SPOTIFY_API_KEY = os.getenv("SPOTIFY_API_KEY", "your_api_key_here")

# Rutas de datos
DATA_PATH = os.getenv("DATA_PATH", "data/")
