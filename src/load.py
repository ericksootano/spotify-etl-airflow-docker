import polars as pl
from .config import SILVER_DIR, GOLD_DIR


# -------------------------------------------------------
# GOLD TABLE 1: Canciones más consistentes
# -------------------------------------------------------
def gold_consistent_songs(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.group_by(["track_name", "artist"])
        .agg(
            [
                pl.count().alias("days_in_chart"),
                pl.col("position").mean().alias("avg_position"),
            ]
        )
        .sort("days_in_chart", descending=True)
    )


# -------------------------------------------------------
# GOLD TABLE 2: Streams totales por país y canción
# -------------------------------------------------------
def gold_streams_by_country(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.group_by(["region", "country", "track_name", "artist"])
        .agg(
            [
                pl.sum("streams").alias("total_streams"),
                pl.count().alias("days_in_chart"),
                (pl.sum("streams") / pl.count()).alias("avg_daily_streams"),
            ]
        )
        .sort("total_streams", descending=True)
    )

# -------------------------------------------------------
# GOLD TABLE 3: Tendencias temporales globales
# -------------------------------------------------------
def gold_daily_trends(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.group_by("date")
        .agg(pl.sum("streams").alias("total_streams_global"))
        .sort("date")
    )


# -------------------------------------------------------
# SAVE FUNCTION
# -------------------------------------------------------
def save_gold(df: pl.DataFrame, filename: str):
    GOLD_DIR.mkdir(parents=True, exist_ok=True)
    path = GOLD_DIR / filename
    print(f"[GOLD] Guardando archivo: {path}")
    df.write_parquet(path)
    print(f"[GOLD] Filas: {df.height}")
