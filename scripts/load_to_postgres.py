import pandas as pd
from sqlalchemy import create_engine

def load_to_postgres():

    # conexión PostgreSQL Docker
    engine = create_engine(
        "postgresql+psycopg2://airflow:airflow@postgres:5432/airflow"
    )

    # leer CSV transformado
    df = pd.read_csv(
        "/opt/airflow/data/processed/resumen_mensual.csv"
    )

    # timestamp ETL
    df["fecha_carga"] = pd.Timestamp.now()

    # cargar tabla
    df.to_sql(
        "resumen_climatico",
        engine,
        if_exists="append",
        index=False
    )

    print("Datos cargados en PostgreSQL")


if __name__ == "__main__":
    load_to_postgres()