import polars as pl
from .config import SILVER_DIR


def transform_spotify_daily(df_raw: pl.DataFrame) -> pl.DataFrame:
    """
    Aplica las transformaciones de Bronze -> Silver:
    - Renombra columnas a snake_case
    - Convierte tipos (date, int)
    - Normaliza region
    """

    # 1) Renombrar columnas a snake_case
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

    # 2) Convertir tipos y normalizar
    df = df.with_columns(
        [
            # Date a tipo fecha (ya viene 'YYYY-MM-DD')
            pl.col("date").str.strptime(pl.Date, format="%Y-%m-%d"),

            # Por si alguna región viene rara, aseguramos minúsculas
            pl.col("region").str.to_lowercase(),

            # Streams y position como int64 explícito (por claridad)
            pl.col("streams").cast(pl.Int64),
            pl.col("position").cast(pl.Int64),
        ]
    )

    return df


def save_silver(df: pl.DataFrame, filename: str = "spotify_daily_silver.parquet") -> None:
    """
    Guarda el dataframe Silver en la carpeta data/silver como Parquet.
    """
    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    output_path = SILVER_DIR / filename
    print(f"[SILVER] Guardando Silver en: {output_path}")
    df.write_parquet(output_path)
    print(f"[SILVER] Filas guardadas: {df.height}")
