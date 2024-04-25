import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from functools import partial
from concurrent.futures import ProcessPoolExecutor
from environment import Environment
from raytracing import RayTracing
from position import Position
from receiver import Receiver
from emitter import Emitter
import time

def draw_obstacles(ax, env):
    """
    Dessine les obstacles sur le graphique.
    """
    lines = []
    line_colors = []
    for obstacle in env.obstacles:
        x0, y0 = obstacle.start.x, obstacle.start.y
        x1, y1 = obstacle.end.x, obstacle.end.y
        line = [(x0, y0), (x1, y1)]
        lines.append(line)
        line_colors.append(obstacle.material.color)
    lc = LineCollection(lines, colors=line_colors, linewidths=[obstacle.thickness * 10 for _ in lines])
    ax.add_collection(lc)
    for emitter in env.emitters:
        ax.scatter(emitter.position.x, emitter.position.y, color='white', s=10, edgecolors='black',
                   label='Emitter' if 'Emitter' not in ax.get_legend_handles_labels()[1] else "")

def calculate_power_at_point(env, ray_tracer, x, y):
    """
    Calcule la puissance reçue en un point donné.
    """
    dummy_receiver = Receiver(Position(x, y), sensitivity=-90, gain=1.7)
    env.receivers = [dummy_receiver]
    ray_tracer.ray_tracer()
    return dummy_receiver.received_power_dBm if dummy_receiver.received_power_dBm >= -90 else -90

def create_heatmap(env, width, height, resolution):
    """
    Crée une carte thermique de la puissance reçue avec un pas de 0.5
    """
    x = np.arange(0, width, resolution)
    y = np.arange(0, height, resolution)
    X, Y = np.meshgrid(x, y)
    power_grid = np.full(X.shape, np.nan)
    ray_tracer = RayTracing(env, 60e9)
    func = partial(calculate_power_at_point, env, ray_tracer)
    with ProcessPoolExecutor() as executor:
        results = executor.map(func, X.ravel(), Y.ravel())
    power_grid = np.array(list(results)).reshape(X.shape)
    fig, ax = plt.subplots(figsize=(12, 10))
    heatmap = ax.pcolormesh(X, Y, power_grid, shading='auto', cmap='viridis', vmin=-90, vmax=-40)
    plt.colorbar(heatmap, label='Power Received (dBm)')
    draw_obstacles(ax, env)
    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    ax.set_title('Heatmap of Power Received in dBm with Obstacles')
    ax.set_xlim([0, width])
    ax.set_ylim([0, height])
    ax.set_aspect('equal')
    plt.gca().invert_yaxis()
    plt.show()

def calc_power_at_position(position, env, ray_tracer, width, height):
    """
        Calcule la puissance moyenne reçue à une position donnée en plaçant un émetteur.
        return: Tuple (position, puissance moyenne).
        """
    x, y = position
    env.emitters = [Emitter(Position(x, y), power=20, frequency=60e9, gain=1.7)]
    return (position, calculate_average_received_power(env, ray_tracer, width, height))

def calculate_average_received_power(env, ray_tracer, width, height):
    """
    Calcule la puissance moyenne reçue dans une zone en testant plusieurs positions de récepteurs.
    """
    dummy_positions = [(i, j) for i in np.arange(0, width, 0.5) for j in np.arange(0, height, 0.5)]
    total_power = 0
    count = 0
    for pos in dummy_positions:
        dummy_receiver = Receiver(Position(pos[0], pos[1]), sensitivity=-90, gain=1.7)
        env.receivers = [dummy_receiver]
        ray_tracer.ray_tracer()
        if dummy_receiver.received_power_dBm and dummy_receiver.received_power_dBm >= -90:
            total_power += dummy_receiver.received_power_dBm
            count += 1
    return total_power / count if count else -np.inf

def optimize_emitter_position_parallel(env, width, height, resolutio):
    """
    Optimise la position de l'émetteur pour maximiser la puissance moyenne reçue dans la zone.
    return: Meilleure position et puissance associée.
    """
    positions = [(x, y) for x in np.arange(0.5, width, resolution) for y in np.arange(0.5, height, resolution)]
    best_power = -np.inf
    best_position = None
    ray_tracer = RayTracing(env, 60e9)
    with ProcessPoolExecutor() as executor:
        func = partial(calc_power_at_position, env=env, ray_tracer=ray_tracer, width=width, height=height)
        results = executor.map(func, positions)
    for position, power in results:
        if power > best_power:
            best_power = power
            best_position = position
    return best_position, best_power

if __name__ == '__main__':
    env = Environment()
    start_time = time.time()
    create_heatmap(env, width=17, height=9, resolution=0.5)
    end_time = time.time()
    print(f"Heatmap Time: {end_time - start_time:.2f} seconds")
   #start_time2 = time.time()
   # best_position, best_power = optimize_emitter_position_parallel(env, 17, 9, 0.5)
    #end_time2 = time.time()
   # print(f"Optimal Emitter Position: {best_position} with power: {best_power} dBm")
   # print(f"best position Time: {end_time2 - start_time2:.2f} seconds")
