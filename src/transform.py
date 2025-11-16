import polars as pl
from .config import SILVER_DIR

REGION_MAPPING = {
    "global": "Global",
    "us": "United States",
    "gb": "United Kingdom",
    "br": "Brazil",
    "mx": "Mexico",
    "de": "Germany",
    "es": "Spain",
    "nl": "Netherlands",
    "au": "Australia",
    "se": "Sweden",
    "do": "Dominican Republic",
    "ec": "Ecuador",
    "ar": "Argentina",
    "cl": "Chile",
    "co": "Colombia",
    "pe": "Peru",
    "pt": "Portugal",
    "fr": "France",
    "it": "Italy",
}


def transform_spotify_daily(df_raw: pl.DataFrame) -> pl.DataFrame:
    """
    Limpieza Silver:
    - Renombrar columnas
    - Convertir tipos
    - Normalizar 'region'
    - Añadir columna 'country'
    """

    df = df_raw.rename(
        {
            "Position": "position",
            "Track Name": "track_name",
            "Artist": "artist",
            "Streams": "streams",
            "URL": "url",
            "Date": "date",
            "Region": "region",
        }
    )

    df = df.with_columns(
        [
            pl.col("date").str.strptime(pl.Date, "%Y-%m-%d"),
            pl.col("region").str.to_lowercase(),
            pl.col("streams").cast(pl.Int64),
            pl.col("position").cast(pl.Int64),
        ]
    )

    # NUEVO: Normalizar país
    df = df.with_columns(
        pl.col("region")
        .map_elements(lambda code: REGION_MAPPING.get(code, code))
        .alias("country")
    )

    return df


def save_silver(df: pl.DataFrame, filename: str = "spotify_daily_silver.parquet"):
    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    path = SILVER_DIR / filename
    print(f"[SILVER] Guardando: {path}")
    df.write_parquet(path)
    print(f"[SILVER] Filas: {df.height}")
