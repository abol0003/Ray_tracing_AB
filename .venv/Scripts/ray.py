import numpy as np
from position import Position
class Ray:
    def __init__(self, start_position, end_position, power=0, frequency=0):
        self.start_position = start_position  # Position de départ
        self.end_position = end_position  # Position d'arrivée
        self.power = power  # Puissance du rayon
        self.frequency = frequency  # Fréquence du rayon
        self.interactions = []  # Historique des interactions

    def draw_ray(self, canvas, scale=50):
        # Dessine le rayon sur le canvas avec une couleur spécifique au type d'interaction
        start_x = self.start_position.get_x() * scale
        start_y = self.start_position.get_y() * scale
        end_x = self.end_position.get_x() * scale
        end_y = self.end_position.get_y() * scale
        color = 'green' if self.interactions[0]['type'] == 'direct' else 'red'
        canvas.create_line(start_x, start_y, end_x, end_y, fill=color, dash=(4, 2) if color == 'red' else None)

    def add_interaction(self, interaction_type, obstacle=None, interaction_point=None):
        self.interactions.append({
            'type': interaction_type,
            'obstacle': obstacle,
            'point': interaction_point
        })

