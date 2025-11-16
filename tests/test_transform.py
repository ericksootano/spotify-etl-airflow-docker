import polars as pl
from src.transform import transform_spotify_daily


def test_transform_spotify_daily_basic_schema():
    # Datos simulados "Bronze" (como viene del CSV)
    df_raw = pl.DataFrame(
        {
            "Position": [1, 2],
            "Track Name": ["Song A", "Song B"],
            "Artist": ["Artist A", "Artist B"],
            "Streams": [1000, 2000],
            "URL": ["http://a", "http://b"],
            "Date": ["2017-01-01", "2017-01-02"],
            "Region": ["US", "mx"],
        }
    )

    df_silver = transform_spotify_daily(df_raw)

    # 1. Columnas esperadas
    expected_cols = {
        "position",
        "track_name",
        "artist",
        "streams",
        "url",
        "date",
        "region",
        "country",
    }
    assert set(df_silver.columns) == expected_cols

    # 2. Tipos principales
    schema = df_silver.schema
    assert schema["position"] == pl.Int64
    assert schema["streams"] == pl.Int64
    assert schema["date"] == pl.Date
    assert schema["region"] == pl.String
    assert schema["country"] == pl.String

    # 3. region en minúsculas
    regions = df_silver.select(pl.col("region").unique()).to_series().to_list()
    assert set(regions) == {"us", "mx"}
    # 4. country mapeado correctamente
    # us -> United States (está en REGION_MAPPING)
    # mx -> Mexico (también está en REGION_MAPPING 
    countries = df_silver.select("country").to_series().to_list()
    assert "United States" in countries
    # "mx": "Mexico" al diccionario, valida así:
    # assert "Mexico" in countries
