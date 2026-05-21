import pandas as pd

def clean_data():

    df = pd.read_csv("data/raw/clima_simbolar_2023.csv")

    # eliminar duplicados
    df = df.drop_duplicates()

    # eliminar nulos
    df = df.dropna()

    # convertir fecha
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # crear columna mes
    df["mes"] = df["timestamp"].dt.month

    # guardar limpio
    output_path = "data/processed/clima_simbolar_clean.csv"

    df.to_csv(output_path, index=False)

    print(f"Dataset limpio guardado en: {output_path}")

    return df


if __name__ == "__main__":
    clean_data()