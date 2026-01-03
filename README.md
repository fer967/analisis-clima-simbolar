# 🌦️ Análisis Climático de El Simbolar (Córdoba, Argentina)

Proyecto de **Ciencia de Datos aplicada al agro (AgTech)** que analiza datos meteorológicos simulados con base realista para la localidad de **El Simbolar, Córdoba**, con el objetivo de apoyar **decisiones agrícolas** y **buenas prácticas en la aplicación de fitosanitarios**.

---

## 🎯 Objetivo del Proyecto

* Simular y analizar datos climáticos locales (temperatura, humedad, viento, presión).
* Aplicar el ciclo completo de Ciencia de Datos: **Dataset → EDA → ETL → Análisis → Visualización**.
* Evaluar **impacto del clima en decisiones agronómicas**, como:

  * Ventanas de siembra.
  * Riesgo de deriva en aplicaciones fitosanitarias.
  * Beneficios de cortinas forestales como externalidad positiva.

---

## 🧠 Enfoque Metodológico

El proyecto fue desarrollado siguiendo buenas prácticas profesionales:

1. **Creación de un dataset ficticio con ruido controlado**

   * Valores nulos, duplicados, outliers.
   * Errores de formato y variabilidad realista.

2. **Carga y exploración inicial (EDA)**

   * Análisis de estructura, tipos de datos y estadísticos.
   * Detección visual de inconsistencias.

3. **Limpieza y ETL**

   * Normalización de formatos temporales.
   * Corrección de modelo estacional para el hemisferio sur.
   * Eliminación y tratamiento de ruido no informativo.

4. **Análisis con Pandas**

   * `query()`, `eval()`, `groupby()`, `resample()`.
   * Agregaciones mensuales y detección de eventos extremos.

5. **Visualización y storytelling**

   * Series temporales.
   * Distribuciones y relaciones entre variables.
   * Gráficos de ventanas de siembra.
   * Simulaciones animadas (.gif) de deriva de fitosanitarios.

---

## 📊 Principales Visualizaciones

* 📈 Temperatura y humedad a lo largo del tiempo.
* 📉 Promedios mensuales (estacionalidad climática).
* 🌱 Ventanas de siembra por cultivo (zona centro de Córdoba).
* 🌬️ GIFs de simulación de deriva de fitosanitarios:

  * Efecto del viento.
  * Influencia de temperatura y humedad.
  * Rol protector de cortinas forestales.

---

## 🌲 Externalidades Positivas Analizadas

A partir de las simulaciones se observa que las **cortinas forestales**:

* Reducen significativamente la deriva de fitosanitarios.
* Protegen espejos de agua y lotes vecinos.
* Mejoran la eficiencia de la aplicación.
* Aportan un servicio ecosistémico clave para la producción sostenible.

---

## 🧾 Conclusiones

* El clima local presenta **alta estacionalidad térmica**, coherente con la región.
* El viento, la temperatura y la humedad son **variables críticas** para aplicaciones agrícolas.
* El análisis de datos permite **reemplazar decisiones intuitivas por evidencia**.
* La integración de datos climáticos locales mejora la planificación y reduce impactos ambientales.

---

## ✅ Recomendaciones para el Productor

* Realizar aplicaciones fitosanitarias:

  * Con viento < 10 km/h.
  * Humedad relativa > 60%.
  * Preferentemente temprano por la mañana.

* Incorporar cortinas forestales como práctica preventiva.

* Ajustar fechas de siembra según condiciones térmicas reales y no solo calendario.

---

## 🛠️ Tecnologías Utilizadas

* **Python**
* **Pandas** — manipulación y análisis de datos
* **NumPy** — simulación y cálculos
* **Matplotlib / Seaborn** — visualización
* **Pillow** — generación de GIFs
* **Jupyter Notebook** — análisis interactivo
* **VS Code + venv** — entorno de desarrollo

---

## 📁 Estructura del Proyecto

```
analisis_clima_simbolar/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_creacion_dataset.ipynb
│   ├── 02_eda_etl.ipynb
│   ├── 03_analisis_visualizaciones.ipynb
│
├── outputs/
│   ├── gifs/
│   └── figures/
│
├── requirements.txt
└── README.md
```

---

## 🎥 Storytelling — Video para CV (Guión sugerido)

**Duración:** 2–3 minutos

### 1️⃣ Introducción (20s)

> “Hola, soy desarrollador orientado a Ciencia de Datos. En este proyecto analizo datos climáticos locales de El Simbolar, Córdoba, aplicando técnicas reales de análisis y visualización para el agro.”

### 2️⃣ Problema (30s)

> “En la práctica agrícola muchas decisiones se toman por calendario o experiencia, sin integrar datos climáticos locales, lo que puede generar ineficiencias y riesgos ambientales.”

### 3️⃣ Solución (60s)

> “Desarrollé un dataset climático realista, apliqué limpieza, análisis exploratorio, modelado estacional y visualizaciones. Incluso simulé en GIFs cómo el viento y la temperatura afectan la deriva de fitosanitarios, y cómo una cortina forestal reduce ese impacto.”

### 4️⃣ Valor agregado (30s)

> “Este enfoque permite tomar decisiones basadas en evidencia, mejorar la eficiencia productiva y reducir impactos ambientales.”

### 5️⃣ Cierre (20s)

> “Este proyecto muestra cómo la ciencia de datos puede aplicarse a problemas reales del agro. Gracias por su tiempo.”

---

## 📌 Autor

**Gabriel Fernando Correa**
Proyecto demostrativo para portfolio profesional en Ciencia de Datos / Desarrollo Full-Stack aplicado al agro.
