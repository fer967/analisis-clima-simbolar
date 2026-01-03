import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# -----------------------
# Configuración general
# -----------------------
n = 200
viento = 0.15
cortina_x = 5
frames = 40

# Crear carpeta assets si no existe
os.makedirs("assets", exist_ok=True)

# -----------------------
# Inicialización partículas
# -----------------------
x = np.zeros(n)
y = np.random.uniform(0, 10, n)

fig, ax = plt.subplots(figsize=(6, 4))
scat = ax.scatter(x, y, s=10)
ax.axvline(cortina_x, color="green", linewidth=3)

ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_title("Deriva de fitosanitarios — efecto cortina forestal")
ax.set_xlabel("Distancia")
ax.set_ylabel("Altura")

# -----------------------
# Animación
# -----------------------
def update(frame):
    global x
    x = x + viento
    x = np.where(x > cortina_x, cortina_x, x)  # la cortina frena
    scat.set_offsets(np.c_[x, y])
    return scat,

ani = FuncAnimation(fig, update, frames=frames)

# -----------------------
# Guardar GIF
# -----------------------
output_path = "assets/deriva_viento.gif"
ani.save(output_path, writer="pillow")

plt.close()

print(f"GIF generado correctamente: {output_path}")
