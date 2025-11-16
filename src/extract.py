import polars as pl
from .config import BRONZE_DIR

def extract_spotify_daily(filename: str = "spotify_daily.csv") -> pl.DataFrame:
    """
    Lee el CSV crudo desde la capa Bronze.
    No limpia ni transforma nada.
    """
    file_path = BRONZE_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"El archivo {file_path} no existe.")

    print(f"[EXTRACT] Cargando archivo: {file_path}")

    df = pl.read_csv(file_path)

    print(f"[EXTRACT] Filas cargadas: {df.height}")
    print(f"[EXTRACT] Columnas: {df.columns}")

    return df
