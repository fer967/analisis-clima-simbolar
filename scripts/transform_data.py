import pandas as pd

def transform_data():

    df = pd.read_csv("data/processed/clima_simbolar_clean.csv")

    resumen = (
        df.groupby("mes")
        .agg({
            "temperatura_c": "mean",
            "humedad_pct": "mean"
        })
        .reset_index()
    )

    output_path = "data/processed/resumen_mensual.csv"

    resumen.to_csv(output_path, index=False)

    print("Resumen mensual generado")

    return resumen


if __name__ == "__main__":
    transform_data()