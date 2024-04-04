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

def totalW(ray):
    """
    Calcule la puissance totale reçue en W pour un rayon donné.
    Cela prend en compte les interactions (réflexions) enregistrées dans l'objet Ray.
    """
    # La puissance est déjà calculée et stockée dans l'objet Ray
    return ray.power

def totaldBm(ray):
    """
    Convertit la puissance totale reçue par un rayon donné en dBm.
    """
    if ray.power > 10**(-250):  # Filtrer les puissances extrêmement faibles
        dBm = 10 * np.log10(ray.power / 10**(-3))  # Conversion en dBm
        return dBm
    return -np.inf  # Retourne une valeur infiniment petite si la puissance est sous le seuil
