import numpy as np
from matplotlib import pyplot as plt
from emitter import Emitter
from receiver import Receiver
from obstacle import Obstacle
from environment import Environment
from calcul import *
from physics import *
class RayTracing:
    def __init__(self, environment):
        self.environment = environment

    def compute_image_position(self, obstacle, source_position):

        if obstacle.is_vertical():
            return Position(2 * obstacle.start.x - source_position.x, source_position.y)
        else:
            return Position(source_position.x, 2 * obstacle.start.y - source_position.y)

    def ray_tracer(self):
        for emitter in self.environment.emitters:
            for receiver in self.environment.receivers:
                # Liste temporaire pour stocker les informations sur les rayons de cet émetteur vers ce récepteur
                rays_info = []

                # Chemin direct
                if not check_intersection(self.environment.obstacles, emitter.position, receiver.position):
                    direct_power = calculer_puissance_recue(emitter, receiver, [])
                    rays_info.append({'type': 'direct', 'power': direct_power})

                    # Réflexion simple
                    for obstacle in self.environment.obstacles:
                        image_position = self.compute_image_position(obstacle, emitter.position)
                        if not check_intersection(self.environment.obstacles, image_position, receiver.position):
                            # Calculer l'angle d'incidence pour la réflexion
                            theta_i = calculer_angle_incidence(obstacle.position, emitter.position)
                            # Calculer le coefficient de réflexion
                            gamma_perp = calculer_gamma_perp(obstacle, theta_i)
                            # Assumer une perte de réflexion fictive pour simplifier, dans la réalité, utiliser gamma_perp pour calculer les pertes
                            reflected_power = calculer_puissance_recue(emitter, receiver, [(obstacle, 'reflection')])
                            rays_info.append({'type': 'reflected', 'obstacle': obstacle, 'power': reflected_power})

                    # Réflexion double
                    for second_obstacle in self.environment.obstacles:
                        if second_obstacle == obstacle:
                            continue  # Évite de considérer le même obstacle pour la deuxième réflexion

                        # Calcule la position de l'image de l'émetteur après la première réflexion
                        image_pos_first_reflection = self.compute_image_position(obstacle, emitter.position)

                        # Utilise cette position d'image comme "émetteur" pour calculer la deuxième réflexion
                        image_pos_second_reflection = self.compute_image_position(second_obstacle,
                                                                                  image_pos_first_reflection)

                        # Vérifie si le chemin est valide (pas d'intersection avec d'autres obstacles)
                        if not check_intersection(self.environment.obstacles, emitter.position,
                                                  image_pos_first_reflection) \
                                and not check_intersection(self.environment.obstacles, image_pos_first_reflection,
                                                           image_pos_second_reflection) \
                                and not check_intersection(self.environment.obstacles, image_pos_second_reflection,
                                                           receiver.position):
                            # Si valide, calcule la puissance reçue avec cette double réflexion
                            theta_i_first = calculer_angle_incidence(emitter.position, image_pos_first_reflection)
                            theta_i_second = calculer_angle_incidence(image_pos_first_reflection, receiver.position)
                            gamma_perp_first = calculer_gamma_perp(obstacle, theta_i_first)
                            gamma_perp_second = calculer_gamma_perp(second_obstacle, theta_i_second)
                            power_reflected_double = calculer_puissance_recue(emitter, receiver,
                                                                              [obstacle, second_obstacle]) * np.abs(
                                gamma_perp_first * gamma_perp_second) ** 2

                            # Stocke les informations de ce rayon pour la visualisation
                            rays_info.append({
                                'type': 'double_reflected',
                                'obstacle1': obstacle,
                                'obstacle2': second_obstacle,
                                'power': power_reflected_double
                            })
                # Traitement des informations sur les rayons pour déterminer la puissance reçue maximale
                max_power = max([ray['power'] for ray in rays_info], default=0)
                receiver.received_power = max_power  # Assumer une propriété pour stocker la puissance reçue

                # Après avoir traité tous les obstacles pour cet émetteur-récepteur, ajoute les rayons calculés à l'environnement
                self.environment.rays.extend(rays_info)

    def visualize_ray_paths(self):
        plt.figure(figsize=(10, 6))
        # Correction : Accès direct aux objets 'emitter' et 'receiver' supprimé
        for ray in self.environment.rays:
            if ray['type'] == 'direct':
                plt.plot([ray['start'].x, ray['end'].x], [ray['start'].y, ray['end'].y], 'g-', label='Direct')
            elif ray['type'] == 'reflected':
                plt.plot([ray['start'].x, ray['reflection_point'].x, ray['end'].x],
                         [ray['start'].y, ray['reflection_point'].y, ray['end'].y], 'r--', label='Reflected')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.title('Ray Paths')
        plt.legend()
        plt.show()

