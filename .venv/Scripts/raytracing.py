import numpy as np
from physics import transmission_totale, calculer_coeff_reflexion
from position import Position
from material import Material
class RayTracing:

    def __init__(self, environment, frequency):
        self.environment = environment
        self.frequency = frequency
        self.beta = self.environment.materials['concrete'].beta(self.frequency)

    def compute_image_position(self, obstacle, source_position):
        if obstacle.is_vertical():
            return Position(2 * obstacle.start.x - source_position.x, source_position.y)
        else:
            return Position(source_position.x, 2 * obstacle.start.y - source_position.y)

    def calc_distance(self, p1, p2):
        return np.linalg.norm(np.array([p1.x, p1.y]) - np.array([p2.x, p2.y]))

    def compute_electrical_field_and_power(self, coefficient, distance):
        c= 299792458
        h_e = c/(self.frequency * np.pi)
        R_a=73
        Elec_field = (coefficient * np.sqrt(60 * 1.64e-3) * np.exp(1j * (-distance) * self.beta)) / distance
        Power = ((h_e * np.abs(Elec_field)) ** 2) / (8 * R_a)
        return Elec_field, Power

    def direct_propagation(self, emitter, receiver): #ok pour la propa direct
        Entot, Ptot = 0, 0
        transmission_coefficient, dm = transmission_totale(self.environment.obstacles, emitter.position, receiver.position)
        distance = self.calc_distance(emitter.position, receiver.position) + dm
        if distance == 0:  # Évite la division par zéro
            distance = 10**(-6)

        E, Power = self.compute_electrical_field_and_power(transmission_coefficient, distance)
        return Power

    def reflex_and_power(self, emitter, receiver): #ok pour les reflexions
        Power_tot = 0
        for obstacle in self.environment.obstacles:
            image_position = self.compute_image_position(obstacle, emitter.position)
            if obstacle.check_intersection(image_position, receiver.position):
                imp_p = obstacle.impact_point(image_position, receiver.position)
                transmission_coefficient1, dm_1 = transmission_totale(self.environment.obstacles, emitter.position, imp_p)
                transmission_coefficient2, dm_2 = transmission_totale(self.environment.obstacles, imp_p, receiver.position)
                reflection_coefficient = calculer_coeff_reflexion(obstacle, emitter.position, imp_p)
                coeff_tot = transmission_coefficient1 * transmission_coefficient2 * reflection_coefficient
                distance = self.calc_distance(imp_p, receiver.position) + dm_1 + dm_2
                E, Power = self.compute_electrical_field_and_power(coeff_tot, distance)
                Power_tot += Power
        return Power_tot

    def double_reflex_and_power(self, emitter, receiver): #ok pour les reflexion
        Power_tot = 0
        for obstacle1 in self.environment.obstacles:
            image_pos1 = self.compute_image_position(obstacle1, emitter.position)
            for obstacle2 in self.environment.obstacles:
                image_pos2 = self.compute_image_position(obstacle2, image_pos1)
                if obstacle1 == obstacle2:
                    continue
                elif obstacle2.check_intersection(image_pos2, receiver.position):
                    impact_point2 = obstacle2.impact_point(image_pos2, receiver.position)
                    if obstacle1.check_intersection(image_pos1, receiver.position):
                        impact_point1 = obstacle1.impact_point(image_pos1, receiver.position)
                        if impact_point1 is None or impact_point2 is None:
                            continue
                #trois coeff transmission poss car 3 rayons
                        transmission_coefficient1, dm_1 = transmission_totale(self.environment.obstacles, emitter.position, impact_point1)
                        transmission_coefficient2, dm_2 = transmission_totale(self.environment.obstacles, impact_point1, impact_point2)
                        transmission_coefficient3, dm_3 = transmission_totale(self.environment.obstacles, impact_point2, receiver.position)
                        reflection_coefficient1 = calculer_coeff_reflexion(obstacle1, emitter.position, impact_point1)
                        reflection_coefficient2 = calculer_coeff_reflexion(obstacle2, image_pos1, impact_point2)
                        coeff_tot = transmission_coefficient1 * transmission_coefficient2 * transmission_coefficient3 * reflection_coefficient1 * reflection_coefficient2
                        total_distance = self.calc_distance(emitter.position, impact_point1) + self.calc_distance(impact_point1, impact_point2) + self.calc_distance(impact_point2, receiver.position)
                        Elec, Power = self.compute_electrical_field_and_power(coeff_tot, total_distance)
                        Power_tot += Power
        return Power_tot

    def ray_tracer(self):
        for receiver in self.environment.receivers:
            max_power = -100  # Initialise à une puissance extrêmement basse
            for emitter in self.environment.emitters:
                direct_power = self.direct_propagation(emitter, receiver)
                reflex_power = self.reflex_and_power(emitter, receiver)
                double_reflex_power = self.double_reflex_and_power(emitter, receiver)
                total_power = direct_power + reflex_power + double_reflex_power
                received_power_dBm = 10 * np.log10(total_power / 1e-3)  # Conversion en dBm
                if received_power_dBm > max_power:
                    max_power = received_power_dBm
            receiver.received_power_dBm = max_power
    def visualize_ray_paths(self):
        plt.figure(figsize=(10, 6))
        for ray in self.environment.rays:
            plt.plot([ray.start_position.x, ray.end_position.x], [ray.start_position.y, ray.end_position.y], 'g-' if ray.interactions[0]['type'] == 'direct' else 'r--', label=ray.interactions[0]['type'].capitalize())
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.title('Ray Paths')
        plt.legend()
        plt.show()

