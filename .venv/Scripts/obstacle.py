import numpy as np
from matplotlib import pyplot as plt
from emitter import Emitter
from receiver import Receiver
from calcul_dBm import *
from physics import *
class Obstacle:
    
    
    def __init__(self, start, end, material, thickness):
        self.start = start  # Doit être une instance de Position
        self.end = end      # Doit être une instance de Position
        self.material = material  # Doit être une instance de Material
        self.thickness = thickness

    def draw(self, canvas, scale=50):
        x0, y0 = self.start.get_x() * scale, self.start.get_y() * scale
        x1, y1 = self.end.get_x() * scale, self.end.get_y() * scale
        if self.material.name == 'metal':
            canvas.create_rectangle(x0, y0, x1, y1, fill=self.material.color, width=self.thickness * scale)
        else:
            canvas.create_line(x0, y0, x1, y1, fill=self.material.color, width=self.thickness * scale)

    def is_vertical(self):
        """Retourne True si l'obstacle est vertical, False sinon."""
        return self.start.x == self.end.x

    def check_intersection(self, start_point, end_point):
        """
        Vérifie si le segment de ligne entre start_point et end_point intersecte cet obstacle.
        :param start_point: Instance de Position représentant le point de départ du segment.
        :param end_point: Instance de Position représentant le point d'arrivée du segment.
        :return: Booléen indiquant si une intersection est trouvée avec cet obstacle.
        """
        # Convertir les points de début et de fin de cet obstacle et du segment en coordonnées numpy
        p1 = np.array([self.start.x, self.start.y])
        p2 = np.array([self.end.x, self.end.y])
        q1 = np.array([start_point.x, start_point.y])
        q2 = np.array([end_point.x, end_point.y])

        # Utilisation de la formule pour vérifier l'intersection de deux segments de ligne
        r = p2 - p1
        s = q2 - q1
        rxs = np.cross(r, s)
        qpxr = np.cross((q1 - p1), r)

        if rxs == 0 and qpxr == 0:
            # Les lignes sont colinéaires
            return False

        if rxs == 0 and qpxr != 0:
            # Les lignes sont parallèles et non intersectées
            return False

        if rxs != 0:
            t = np.cross((q1 - p1), s) / rxs
            u = np.cross((q1 - p1), r) / rxs

            if 0 <= t <= 1 and 0 <= u <= 1:
                # Il y a intersection
                return True

        # Aucune intersection trouvée
        return False

    def is_on_obstacle(self, intersection_point):
        """Vérifie si le point d'intersection est sur l'obstacle."""
        if self.is_vertical():
            return min(self.start.y, self.end.y) <= intersection_point.y <= max(self.start.y, self.end.y)
        else:
            return min(self.start.x, self.end.x) <= intersection_point.x <= max(self.start.x, self.end.x)

    def impact_point(self, ray_start, ray_end):
        """Calcule et retourne le point d'impact d'un rayon avec l'obstacle."""
        if self.is_vertical():
            if ray_start.x == ray_end.x:  # Évite la division par zéro pour un segment vertical
                return None
            x_impact = self.start.x
            y_impact = ray_start.y + (ray_end.y - ray_start.y) * (x_impact - ray_start.x) / (ray_end.x - ray_start.x)
            intersection_point = Position(x_impact, y_impact)
        else:
            if ray_start.y == ray_end.y:  # Évite la division par zéro pour un segment horizontal
                return None
            y_impact = self.start.y
            x_impact = ray_start.x + (ray_end.x - ray_start.x) * (y_impact - ray_start.y) / (ray_end.y - ray_start.y)
            intersection_point = Position(x_impact, y_impact)

        if self.is_on_obstacle(intersection_point):
            return intersection_point
        else:
            return None

    def impedance(self, frequency):
        mu0 = 4 * np.pi * 1e-7  # Perméabilité du vide
        eps0 = 8.854187817e-12  # Permittivité du vide
        omega = 2 * np.pi * frequency  # Fréquence angulaire

        # Impédance intrinsèque du vide
        Z0 = np.sqrt(mu0 / eps0)

        # Calcul de l'impédance du matériau de l'obstacle
        eps_r= self.material.permittivity
        #sigma = self.material.conductivite
        #eps_r = eps_m - 1j * (sigma / omega)
        # Calcul de l'impédance complexe du matériau
        Z_material = np.sqrt(mu0 / eps_r)

        return Z_material, Z0
