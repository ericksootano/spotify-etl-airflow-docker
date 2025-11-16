import polars as pl
import pandas as pd
from datetime import date

from src.load import (
    gold_consistent_songs,
    gold_streams_by_country,
    gold_daily_trends,
)


def _build_sample_silver_df() -> pl.DataFrame:
    # DataFrame tipo Silver pequeño para probar agregaciones
    return pl.DataFrame(
        {
            "position": [1, 2, 1, 3],
            "track_name": ["Song A", "Song B", "Song A", "Song C"],
            "artist": ["Artist A", "Artist B", "Artist A", "Artist C"],
            "streams": [100, 200, 150, 50],
            "url": ["http://a", "http://b", "http://a", "http://c"],
            "date": [
                date(2017, 1, 1),
                date(2017, 1, 1),
                date(2017, 1, 2),
                date(2017, 1, 2),
            ],
            "region": ["us", "us", "mx", "mx"],
            "country": ["United States", "United States", "Mexico", "Mexico"],
        }
    )


def test_gold_consistent_songs_structure_and_values():
    df_silver = _build_sample_silver_df()
    df_gold = gold_consistent_songs(df_silver)

    # columnas esperadas
    assert set(df_gold.columns) == {
        "track_name",
        "artist",
        "days_in_chart",
        "avg_position",
    }

    # Song A aparece 2 días, Song B y C solo 1
    row_song_a = df_gold.filter(pl.col("track_name") == "Song A").row(0, named=True)
    assert row_song_a["days_in_chart"] == 2
    # promedio de posición = (1 + 1) / 2 = 1.0
    assert row_song_a["avg_position"] == 1.0


def test_gold_streams_by_country_structure_and_values():
    df_silver = _build_sample_silver_df()
    df_gold = gold_streams_by_country(df_silver)

    # columnas esperadas (incluye region y country)
    assert set(df_gold.columns) == {
        "region",
        "country",
        "track_name",
        "artist",
        "total_streams",
        "days_in_chart",
        "avg_daily_streams",
    }

    # streams totales de Song A en us = 100
    row_us_song_a = df_gold.filter(
        (pl.col("region") == "us") & (pl.col("track_name") == "Song A")
    ).row(0, named=True)
    assert row_us_song_a["total_streams"] == 100

    # streams totales de Song A en mx = 150
    row_mx_song_a = df_gold.filter(
        (pl.col("region") == "mx") & (pl.col("track_name") == "Song A")
    ).row(0, named=True)
    assert row_mx_song_a["total_streams"] == 150


def test_gold_daily_trends_structure_and_values():
    df_silver = _build_sample_silver_df()
    df_gold = gold_daily_trends(df_silver)

    # columnas esperadas
    assert set(df_gold.columns) == {"date", "total_streams_global"}

    # Convertimos a pandas para hacer aserciones de forma estable
    pdf = df_gold.to_pandas()

    # para 2017-01-01: streams = 100 + 200 = 300
    day1_value = pdf.loc[
        pdf["date"] == pd.Timestamp(2017, 1, 1), "total_streams_global"
    ].iloc[0]

    # para 2017-01-02: streams = 150 + 50 = 200
    day2_value = pdf.loc[
        pdf["date"] == pd.Timestamp(2017, 1, 2), "total_streams_global"
    ].iloc[0]

    assert day1_value == 300
    assert day2_value == 200
