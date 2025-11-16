# 🎧 Spotify Daily Charts – Proyecto ETL con Arquitectura Medallion

Este proyecto implementa un pipeline **ETL** sobre el dataset de los **rankings diarios de Spotify a nivel mundial**, siguiendo la arquitectura **Medallion (Bronze → Silver → Gold)** y preparado para ser orquestado con **Airflow + Docker**.

> Objetivo: pasar de datos crudos de Spotify (top 200 canciones diarias por país) a tablas analíticas listas para responder preguntas de negocio sobre **consistencia en el ranking**, **streams por país** y **tendencias en el tiempo**.

---

## 📂 Arquitectura del Proyecto

Estructura principal del proyecto:

```text
spotify_etl_project/
├─ src/
│  ├─ config.py              # Rutas y configuración general
│  ├─ extract.py             # Lógica Bronze: lectura de CSV crudo
│  ├─ transform.py           # Lógica Silver: limpieza + tipificación
│  └─ load.py                # Lógica Gold: agregaciones y métricas
├─ data/
│  ├─ bronze/                # Datos crudos (Kaggle)
│  ├─ silver/                # Datos limpios y tipados
│  └─ gold/                  # Tablas analíticas finales
├─ notebooks/
│  └─ exploracion_inicial.ipynb
├─ dags/                     # (Próximo paso) DAGs de Airflow
├─ docker/                   # (Próximo paso) Configuración Docker/Airflow
├─ requirements.txt
└─ README.md
