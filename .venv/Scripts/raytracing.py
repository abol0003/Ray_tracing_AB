import numpy as np
from emitter import Emitter
from receiver import Receiver
from obstacle import Obstacle
from environment import Environment
from calcul_dBm import *
from physics import *
from position import Position
from material import Material
from ray import Ray

class RayTracing:
    def __init__(self, environment):
        self.environment = environment
        self.beta = self.material.beta(60e9) # Constante beta calculée à partir de la fréquence de 60 GHz

    def compute_image_position(self, obstacle, source_position):
        if obstacle.is_vertical():
            return Position(2 * obstacle.start.x - source_position.x, source_position.y)
        else:
            return Position(source_position.x, 2 * obstacle.start.y - source_position.y)

    def distance(self, position1, position2):

    def compute_electrical_field_and_power(self, transmission_coefficient, distance, obstacle=None, interaction_type='direct'):
        # Utilise la formule pour calculer le champ électrique et la puissance
        En = (transmission_coefficient * np.sqrt(60 * 1.64 * 10e-3) * np.exp(complex(0, -distance * self.beta))) / distance
        P = np.abs(En) ** 2
        return En, P

    def create_ray_and_compute_power_1(self, emitter, receiver, start_pos, end_pos, image):
        if obstacle.check_intersection(start_pos, end_pos):
            #calcule le point d'impact
            imp_p= obstacle.impact_point(start_pos, end_pos)
            # Calcul de la transmission totale et de la distance dans le matériel pour des chemins directs ou réfléchis
            transmission_coefficient1, dm_1 = transmission_totale(obstacles, start_position, imp_p)
            transmission_coefficient2, dm_2 = transmission_totale(obstacles, imp_p, end_position)
            reflexion_coefficient = calculer_coeff_reflexion(obstacle, start_pos, imp_p)
            coeff_tot=transmission_coefficient1*transmission_coefficient2*reflexion_coefficient
            distance_vector = +dm_1+dm_2
            distance = np.linalg.norm(distance_vector) + distance_in_material
            if distance == 0: distance = 10 ** (-6)  # Éviter la division par zéro

            # Calcul du champ électrique et de la puissance
            En, P = self.compute_electrical_field_and_power(coeff_tot, distance, obstacle=None, interaction_type=interaction_type)

            # Création du rayon avec les informations de puissance et d'interaction
            ray = Ray( imp_p, end_pos, P, emitter.frequency, interaction_type=interaction_type)
            for obstacle in obstacles:
                ray.add_interaction(interaction_type, obstacle)
            self.environment.rays.append(ray)
            return P
        return 0

    def ray_tracer(self):
        for emitter in self.environment.emitters:
            for receiver in self.environment.receivers:
                # Chemin direct
                self.create_ray_and_compute_power(emitter, receiver, emitter.position, receiver.position)

                # Réflexions simples et doubles     #il y a des erreur car il faut que le rayon soit créer à partir du point d'impact du rayon sur l'obstacle
                for obstacle in self.environment.obstacles:
                    image_position = self.compute_image_position(obstacle, emitter.position)
                    self.create_ray_and_compute_power(emitter, receiver, emitter.position, image_position, 'reflected', [obstacle])

                    for second_obstacle in self.environment.obstacles:
                        if second_obstacle == obstacle: continue
                        image_pos_second_reflection = self.compute_image_position(second_obstacle, image_position)
                        self.create_ray_and_compute_power(emitter, receiver, emitter.position, image_pos_second_reflection, 'double_reflected', [obstacle, second_obstacle])

                # Calcul de la puissance totale reçue et mise à jour du récepteur
                total_power_w = sum(ray.power for ray in self.environment.rays if ray.end_position == receiver.position)
                receiver.received_power_dBm = 10 * np.log10(total_power_w / 10 ** (-3))

    def visualize_ray_paths(self):
        plt.figure(figsize=(10, 6))
        for ray in self.environment.rays:
            plt.plot([ray.start_position.x, ray.end_position.x], [ray.start_position.y, ray.end_position.y], 'g-' if ray.interaction_type == 'direct' else 'r--', label=ray.interaction_type.capitalize())
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.title('Ray Paths')
        plt.legend()
        plt.show()
