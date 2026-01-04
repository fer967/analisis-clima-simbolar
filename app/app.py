import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import base64
from pathlib import Path

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
    return pd.read_csv("data/processed/clima_simbolar_2023_clean.csv")
df = cargar_datos()
st.success(f"Dataset cargado: {df.shape[0]} registros")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Clima general",
    "🌱 Análisis agroclimático",
    "🧪 Simulación ambiental",
    "ℹ️ Contexto & conclusiones"
])


with tab1:
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


with tab2:
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

    st.subheader("🎛️ Parámetros ambientales")

    viento = st.slider(
    "Velocidad del viento (km/h)",
    min_value=0.0,
    max_value=25.0,
    value=8.0,
    step=0.5
    )

    temperatura = st.slider(
    "Temperatura ambiente (°C)",
    min_value=5.0,
    max_value=40.0,
    value=25.0,
    step=0.5
    )

    humedad = st.slider(
    "Humedad relativa (%)",
    min_value=20,
    max_value=100,
    value=60,
    step=5
    )

    factor_viento = viento / 20
    factor_temp = max(0, (temperatura - 20) / 20)
    factor_humedad = max(0, (60 - humedad) / 60)

    riesgo_deriva = factor_viento + factor_temp + factor_humedad
    riesgo_deriva = min(riesgo_deriva, 1.0)

    st.subheader("📊 Riesgo estimado de deriva")

    st.metric("Índice de riesgo de deriva", f"{riesgo_deriva:.2f}")

    if riesgo_deriva < 0.3:
        st.success("🟢 Riesgo BAJO — Condiciones adecuadas")
    elif riesgo_deriva < 0.6:
        st.warning("🟡 Riesgo MODERADO — Aplicar con precaución")
    else:
        st.error("🔴 Riesgo ALTO — No se recomienda aplicar")

    st.info("""
    **Interpretación técnica**

    El riesgo de deriva aumenta con:
    - Mayor velocidad del viento
    - Temperaturas elevadas (mayor evaporación)
    - Baja humedad relativa

    Las **cortinas forestales** actúan como barrera física,
    reduciendo la deriva y protegiendo:
    - Espejos de agua
    - Lotes vecinos
    - Zonas pobladas
    """)


with tab3:
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

# -----------------------------
# Modelo conceptual corregido
# -----------------------------
    viento_norm = viento_sim / 25
    altura_norm = altura_cortina / 100

    indice_cruce = viento_norm * (1 - altura_norm)

    st.metric("Índice conceptual de cruce", f"{indice_cruce:.2f}")

    st.caption(
    f"Viento relativo: {viento_norm:.2f} · "
    f"Eficiencia de la cortina: {altura_norm:.2f}"
    )

    st.divider()

    if indice_cruce < 0.3:
        st.success("🟢 Deriva contenida — Cortina efectiva")

        mostrar_gif(
            GIF_PATH_SIMPLE,
            width="100%"
        )

    else:
        st.error("🔴 Deriva cruzando la cortina")

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


with tab4:
    st.header("ℹ️ Contexto y conclusiones")

    st.markdown("""
    ### 📍 Contexto
    - Ubicación: El Simbolar, Córdoba, Argentina  
    - Clima templado subhúmedo  
    - Producción agrícola extensiva  

    ### 📌 Hallazgos clave
    - Temperaturas máximas concentradas en verano
    - Humedad variable durante períodos críticos
    - El viento puede impactar aplicaciones fitosanitarias

    ### ✅ Recomendaciones
    - Ajustar fechas de siembra según ventana térmica
    - Evitar aplicaciones con viento > 15 km/h
    - Implementar **cortinas forestales** para reducir deriva
    """)



# Para ejecutar la aplicación:    streamlit run app/app.py





