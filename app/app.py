import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import base64
from pathlib import Path
import numpy as np

from sqlalchemy import create_engine

st.set_page_config(
    page_title="Análisis Climático – El Simbolar (Córdoba)",
    layout="wide"
)

def mostrar_gif(path: Path, width="100%"):
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    st.markdown(
        f"""
        <img src="data:image/gif;base64,{b64}" style="width:{width};"/>
        """,
        unsafe_allow_html=True
    )

BASE_DIR = Path(__file__).parent.parent

GIF_PATH_SIMPLE = BASE_DIR / "assets" / "deriva_viento.gif"
GIF_PATH_CORTINA = BASE_DIR / "assets" / "deriva_viento_cortina.gif"

st.title("🌦️ Analisis Meteorológico – El Simbolar, Córdoba")


@st.cache_data
def cargar_datos():

    df = pd.read_csv(
        "data/processed/resumen_mensual.csv"
    )

    return df
df = cargar_datos()
# fecha simulada de carga ETL
df["fecha_carga"] = pd.Timestamp.now()
st.success(
    f"Dataset cargado: {df.shape[0]} registros"
)


# def cargar_datos():
#     engine = create_engine(
#         "postgresql://airflow:airflow@localhost:5433/airflow"
#     )
#     query = """
#     SELECT *
#     FROM resumen_climatico
#     """
#     df = pd.read_sql(query, engine)
#     return df
# df = cargar_datos()
# st.success(
#     f"Dataset cargado desde PostgreSQL: {df.shape[0]} registros"
# )

seccion = st.radio(
    "📂 Navegación",
    [
        "📦 Monitoreo ETL",
        "🌤️ Clima general",
        "🌱 Análisis agroclimático",
        "🧪 Simulación de deriva",
        "ℹ️ Contexto y conclusiones"
    ],
    horizontal=True
)


if seccion == "📦 Monitoreo ETL":
    st.header("📦 Monitoreo del pipeline ETL")
    st.markdown("""
    Esta sección muestra métricas operacionales del pipeline
    construido con Apache Airflow + PostgreSQL.
    """)
    # convertir fecha
    df["fecha_carga"] = pd.to_datetime(df["fecha_carga"])  
    # métricas
    ultima_carga = df["fecha_carga"].max()
    total_registros = len(df)
    ejecuciones = df["fecha_carga"].dt.floor("s").nunique()
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "🕒 Última carga ETL",
        str(ultima_carga)
    )
    col2.metric(
        "📄 Registros almacenados",
        total_registros
    )
    col3.metric(
        "⚙️ Ejecuciones históricas",
        ejecuciones
    )
    st.divider()
    st.subheader("📈 Registros cargados por ejecución")
    etl_por_carga = (
        df.groupby(df["fecha_carga"].dt.floor("s"))
        .size()
    )
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(
        etl_por_carga.index,
        etl_por_carga.values,
        marker="o"
    )
    ax.set_xlabel("Fecha de carga")
    ax.set_ylabel("Cantidad de registros")
    ax.set_title("Histórico de ejecuciones ETL")
    st.pyplot(fig)


if seccion == "🌤️ Clima general":
    st.header("📊 Comportamiento climático anual")
    col1, col2 = st.columns(2)
    col1.metric(
        "🌡️ Temp. media (°C)",
        f"{df['temperatura_c'].mean():.1f}"
    )
    col2.metric(
        "💧 Humedad media (%)",
        f"{df['humedad_pct'].mean():.1f}"
    )
    st.divider()
    variable = st.selectbox(
        "Seleccioná la variable",
        ["temperatura_c", "humedad_pct"]
    )
    df_plot = df.groupby("mes")[variable].mean()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_plot.index, df_plot.values, marker="o")
    ax.set_xlabel("Mes")
    ax.set_ylabel(variable)
    ax.set_title(f"Evolución mensual de {variable}")
    st.pyplot(fig)


elif seccion == "🌱 Análisis agroclimático":
    st.header("🌱 Ventanas agroclimáticas")
    cultivo = st.selectbox(
        "Seleccioná cultivo",
        ["Soja", "Maíz", "Trigo"]
    )
    if cultivo == "Soja":
        meses = [10, 11, 12]
        t_min, t_max = 15, 30
    elif cultivo == "Maíz":
        meses = [9, 10, 11]
        t_min, t_max = 12, 30
    else:  # Trigo
        meses = [6, 7, 8]
        t_min, t_max = 5, 20
    df_cultivo = (
        df[df["mes"].isin(meses)]
        .groupby("mes")["temperatura_c"]
        .mean()
    )
    st.success(f"Ventana típica de siembra: meses {meses}")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_cultivo.index, df_cultivo.values, marker="o", label="Temp media")
    ax.axhline(t_min, linestyle="--", alpha=0.6, label="Temp mínima")
    ax.axhline(t_max, linestyle="--", alpha=0.6, label="Temp máxima")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Temperatura (°C)")
    ax.set_title(f"Temperatura durante ventana de {cultivo}")
    ax.legend()
    st.pyplot(fig)

elif seccion == "🧪 Simulación de deriva":
    st.header("🧪 Simulación ambiental de deriva de fitosanitarios")
    st.markdown("""
    Modelo conceptual para visualizar cómo **el viento** y la **altura de la cortina forestal**
    influyen en la deriva de fitosanitarios.
    """)
    st.subheader("🎛️ Parámetros de simulación")
    st.markdown("""
    👉 **Cómo usar la simulación**
    - Mové el **slider de viento** para aumentar o reducir la fuerza que empuja las partículas.
    - Ajustá la **altura de la cortina forestal** para ver su capacidad de contención.
    - Observá cómo cambia el **índice de cruce** y la animación:
    
    🟢 Con viento bajo y cortina alta → la deriva se contiene  
    🔴 Con viento alto y cortina baja → parte del fitosanitario atraviesa la cortina
    """)
    col1, col2 = st.columns(2)
    with col1:
        viento_sim = st.slider(
            "🌬️ Velocidad del viento (km/h)",
            min_value=0.0,
            max_value=25.0,
            value=8.0,
            step=0.5
        )
    with col2:
        altura_cortina = st.slider(
            "🌲 Altura relativa de la cortina (%)",
            min_value=10,
            max_value=100,
            value=60,
            step=5
        )
        
    viento_norm = viento_sim / 25
    altura_norm = altura_cortina / 100
    
    indice_cruce = viento_norm * (1 - altura_norm)
    porcentaje_cruce = int(indice_cruce * 100)
    st.metric("Índice conceptual de cruce", f"{indice_cruce:.2f}")

    st.caption(
    f"Viento relativo: {viento_norm:.2f} · "
    f"Eficiencia de la cortina: {altura_norm:.2f}"
    )

    st.divider()

    if indice_cruce < 0.3:
        st.success("🟢 Deriva mayormente contenida — Cortina efectiva")
        st.caption(
            "Una fracción muy pequeña del material fino puede atravesar la cortina."
        )

        st.metric(
            "Fitosanitario que atraviesa la cortina",
            f"{porcentaje_cruce} %"
        )
        st.progress(min(porcentaje_cruce / 100, 1.0))

        mostrar_gif(
            GIF_PATH_SIMPLE,
            width="100%"
        )

    else:
        st.error("🔴 Deriva significativa atravesando la cortina")
        st.caption(
            "Una proporción relevante del material logra superar la barrera vegetal."
        )

        st.metric(
            "Fitosanitario que atraviesa la cortina",
            f"{porcentaje_cruce} %"
        )
        st.progress(porcentaje_cruce / 100)

        mostrar_gif(
            GIF_PATH_CORTINA,
            width="100%"
        )

    st.markdown("""
        ⚠️ El viento supera la capacidad de contención  
        ⚠️ Parte del fitosanitario atraviesa la cortina  
        ❗ Riesgo para:
        - 🏠 Viviendas
        - 🐄 Animales
        - 🌊 Cuerpos de agua
        """)
    st.info("""
    📌 **Nota técnica**  
    Esta simulación es **conceptual y educativa**.  
    No reemplaza estudios de deriva certificados, pero permite
    **comprender visualmente** la importancia de las cortinas forestales.
    """)


    st.subheader("🌡️💧 Impacto ambiental en la eficiencia de aplicación")

    st.markdown("""
    Además de la deriva, la **temperatura** y la **humedad relativa**
    influyen directamente en la **eficiencia de la aplicación fitosanitaria**.

    Los siguientes gráficos muestran relaciones **conceptuales** ampliamente aceptadas
    en buenas prácticas agrícolas.
    """)

    temp = np.linspace(5, 40, 300)
    ef_temp = np.exp(-0.03 * (temp - 22)**2)
    fig, ax = plt.subplots()
    ax.plot(temp, ef_temp, linewidth=2, label="Eficiencia relativa")
# Zonas
    ax.axvspan(5, 12, alpha=0.18, color="red", label="Zona crítica")
    ax.axvspan(30, 40, alpha=0.18, color="red")
    ax.axvspan(12, 18, alpha=0.25, color="gold", label="Precaución")
    ax.axvspan(18, 25, alpha=0.30, color="green", label="Zona óptima")
    ax.axvline(22, linestyle="--", alpha=0.6)
    ax.set_xlabel("Temperatura (°C)")
    ax.set_ylabel("Eficiencia relativa")
    ax.set_title("Efecto de la temperatura en la eficiencia de aplicación")
    ax.set_ylim(0, 1)
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())
    st.pyplot(fig)

    hum = np.linspace(20, 100, 300)

# Aumento de eficiencia con la humedad
    ef_sube = 1 - np.exp(-0.06 * (hum - 35))

# Penalización por humedad excesiva (>80%)
    penalizacion = np.exp(-0.04 * np.maximum(hum - 80, 0))

# Eficiencia final
    ef_hum = ef_sube * penalizacion
    ef_hum = np.clip(ef_hum, 0, 1)

    fig, ax = plt.subplots()
    ax.plot(hum, ef_hum, linewidth=2, label="Eficiencia relativa")

# Zonas
    ax.axvspan(20, 40, alpha=0.18, color="red", label="Zona crítica (evaporación)")
    ax.axvspan(40, 60, alpha=0.25, color="gold", label="Precaución")
    ax.axvspan(60, 80, alpha=0.30, color="green", label="Zona óptima")
    ax.axvspan(80, 100, alpha=0.22, color="gold", label="Exceso de humedad")

    ax.set_xlabel("Humedad relativa (%)")
    ax.set_ylabel("Eficiencia relativa")
    ax.set_title("Efecto de la humedad en la eficiencia de aplicación")
    ax.set_ylim(0, 1)

# Leyenda sin duplicados
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())

    st.pyplot(fig)


    st.info("""
    📌 **Interpretación técnica**
    
    🟩 Zona óptima  
    Condiciones ideales para maximizar eficiencia y minimizar pérdidas.
    
    🟨 Precaución  
    Aplicación posible, pero con mayor riesgo de evaporación o menor absorción.
    
    🟥 Zona crítica  
    No se recomienda aplicar por alta pérdida o baja eficacia.
    """)


elif seccion == "ℹ️ Contexto y conclusiones":
    st.header("ℹ️ Contexto y conclusiones")

    st.markdown("""
    ## 📍 Contexto general
    - **Ubicación:** El Simbolar, Córdoba, Argentina  
    - **Clima:** Templado subhúmedo  
    - **Sistema productivo:** Agricultura extensiva  

    Este análisis integra **datos climáticos históricos** con
    **modelos conceptuales de simulación**, orientados a la **toma de decisiones agroambientales**.
    """)

    st.markdown("""
    ## 📌 Hallazgos clave
    - 🌡️ Las **temperaturas máximas** se concentran en los meses estivales, afectando el rendimiento de aplicaciones.
    - 💧 La **humedad relativa** presenta alta variabilidad en períodos críticos.
    - 🌬️ El **viento** es el principal factor de riesgo en la deriva de fitosanitarios.
    - 🌲 La **altura y densidad de la cortina forestal** influyen directamente en la contención de la deriva.
    """)

    st.markdown("""
    ## 🧪 Aportes de la simulación ambiental
    - Permite **visualizar el cruce o contención** de fitosanitarios según:
        - Velocidad del viento  
        - Altura relativa de la cortina  
    - Refuerza el concepto de **riesgo hacia zonas sensibles**:
        - 🏠 Viviendas  
        - 🐄 Animales  
        - 🌊 Cuerpos de agua  
    - Complementa el análisis numérico con una **lectura visual e intuitiva**.
    """)

    st.markdown("""
    ## 🌡️ Influencia de temperatura y humedad
    - **Temperaturas elevadas** incrementan la evaporación → menor eficiencia de aplicación.
    - **Baja humedad relativa** aumenta el riesgo de deriva.
    - Existen **zonas óptimas**, de **precaución** y **críticas**, claramente identificables en los gráficos.
    """)

    st.markdown("""
    ## ✅ Recomendaciones prácticas
    - Ajustar **fechas de siembra** según ventanas térmicas del cultivo.
    - Evitar aplicaciones con:
        - Viento > **15 km/h**
        - Temperaturas elevadas
        - Humedad relativa baja
    - Implementar y mantener **cortinas forestales** como barrera ambiental.
    """)

    st.info("""
    📌 **Conclusión final**

    La combinación de **datos climáticos**, **visualizaciones** y **simulaciones conceptuales**
    permite comprender de forma clara cómo las variables ambientales
    impactan en la eficiencia y seguridad de las aplicaciones agrícolas.

    Este enfoque no reemplaza estudios técnicos formales,
    pero constituye una **herramienta educativa y de apoyo a la toma de decisiones**.
    """)










