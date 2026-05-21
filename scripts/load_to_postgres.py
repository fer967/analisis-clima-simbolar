import pandas as pd
from sqlalchemy import create_engine

def load_to_postgres():

    # conexión
    engine = create_engine(
        "postgresql+psycopg2://airflow:airflow@postgres:5432/airflow"
    )

    # leer csv transformado
    df = pd.read_csv("data/processed/resumen_mensual.csv")

    # guardar tabla
    df.to_sql(
        "resumen_climatico",
        engine,
        if_exists="replace",
        index=False
    )

    print("Datos cargados en PostgreSQL")

if __name__ == "__main__":
    load_to_postgres()