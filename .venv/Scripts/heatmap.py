import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from environment import Environment
from raytracing import RayTracing
from position import Position
from receiver import Receiver


def draw_obstacles(ax, env):
    """
    Dessine les obstacles sur l'axe matplotlib.

    :param ax: Axe matplotlib sur lequel dessiner les obstacles.
    :param env: Environnement contenant les obstacles.
    """
    lines = []
    line_colors = []
    for obstacle in env.obstacles:
        # Obtenir les points de départ et de fin de chaque obstacle
        x0, y0 = obstacle.start.x, obstacle.start.y
        x1, y1 = obstacle.end.x, obstacle.end.y
        line = [(x0, y0), (x1, y1)]
        lines.append(line)
        line_colors.append(obstacle.material.color)

        # Créer une collection de lignes
        lc = LineCollection(lines, colors=line_colors, linewidths=[obstacle.thickness * 10 for _ in lines])
        ax.add_collection(lc)
        for emitter in env.emitters:
            ax.scatter(emitter.position.x, emitter.position.y, color='white', s=10, edgecolors='black',
                       label='Emitter' if 'Emitter' not in ax.get_legend_handles_labels()[1] else "")


def create_heatmap(env, width=20, height=15, resolution=0.5):
    """
    Crée une carte thermique de la puissance reçue en dBm.

    :param env: Environnement contenant les obstacles et émetteurs.
    :param width: Largeur de la carte (en mètres).
    :param height: Hauteur de la carte (en mètres).
    :param resolution: Résolution de la grille (en mètres).
    """
    x = np.arange(0, width, resolution)
    y = np.arange(0, height, resolution)
    X, Y = np.meshgrid(x, y)
    power_grid = np.full(X.shape, np.nan)  # Utilise NaN pour les données initiales

    ray_tracer = RayTracing(env, 60e9)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            dummy_receiver = Receiver(Position(X[i, j], Y[i, j]), sensitivity=-90, gain=1.7)
            env.receivers = [dummy_receiver]
            ray_tracer.ray_tracer()
            if dummy_receiver.received_power_dBm >= -90:
                power_grid[i, j] = dummy_receiver.received_power_dBm
            else:
                power_grid[i, j]= -90

    fig, ax = plt.subplots(figsize=(12, 10))
    heatmap = ax.pcolormesh(X, Y, power_grid, shading='auto', cmap='viridis', vmin=-90, vmax=-40)
    plt.colorbar(heatmap, label='Power Received (dBm)')

    draw_obstacles(ax, env)  # Dessiner les obstacles sur la carte thermique

    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    ax.set_title('Heatmap of Power Received in dBm with Obstacles')
    ax.set_xlim([0, width])
    ax.set_ylim([0, height])
    plt.gca().invert_yaxis()  # Inverser l'axe Y pour avoir l'origine en haut à gauche
    plt.show()


# Exemple d'utilisation
env = Environment()
create_heatmap(env, width=17, height=9, resolution=0.5)
