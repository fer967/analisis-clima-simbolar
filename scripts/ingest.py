import pandas as pd

def ingest_data():
    df = pd.read_csv("data/raw/clima_simbolar_2023.csv")

    print("Dataset cargado correctamente")
    print(df.head())

    return df


if __name__ == "__main__":
    ingest_data()