import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# =============================
# Parámetros
# =============================
n = 250
x = np.zeros(n)
y = np.random.uniform(0, 10, n)

viento = 0.25            # velocidad del viento
altura_cortina = 6.0    # slider luego (0–10)
cortina_x = 5

# probabilidad de cruce
prob_cruce = max(0, viento*4 - altura_cortina/10)

# =============================
# Figura
# =============================
fig, ax = plt.subplots(figsize=(7, 4))

colors = np.array(["green"] * n)
scat = ax.scatter(x, y, s=12, c=colors)

# cortina forestal
ax.axvline(cortina_x, color="darkgreen", linewidth=4)
ax.text(cortina_x - 0.4, 9.5, "🌳", fontsize=18)

# zona sensible
ax.text(8.2, 7, "🏠", fontsize=20)
ax.text(8.2, 5, "🐄", fontsize=20)
ax.text(8.2, 3, "🌊", fontsize=20)

ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_title("Deriva de fitosanitarios — viento vs cortina forestal")
ax.set_xticks([])
ax.set_yticks([])


def update(frame):
    global x, colors

    x = x + viento

    for i in range(n):
        if x[i] >= cortina_x:
            if np.random.rand() < prob_cruce:
                colors[i] = "red"   # cruza la cortina
            else:
                x[i] = cortina_x
                colors[i] = "green" # queda frenada

    scat.set_offsets(np.c_[x, y])
    scat.set_color(colors)
    return scat,

ani = FuncAnimation(fig, update, frames=40, interval=120)

ani.save(
    "assets/deriva_viento_cortina.gif",
    writer="pillow"
)

plt.close()
