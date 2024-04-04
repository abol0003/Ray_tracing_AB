# fichier ray.py
import numpy as np
from position import Position

class Ray:
    def __init__(self, start_position, end_position, power=0, frequency=0):
        self.start_position = start_position  # Position de départ
        self.end_position = end_position  # Position d'arrivée
        self.power = power  # Puissance du rayon
        self.frequency = frequency  # Fréquence du rayon
        self.interactions = []  # Historique des interactions

    def add_interaction(self, interaction_type, obstacle=None, interaction_point=None):
        self.interactions.append({
            'type': interaction_type,
            'obstacle': obstacle,
            'point': interaction_point
        })


