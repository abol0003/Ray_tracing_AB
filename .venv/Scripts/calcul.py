import numpy as np
from physics import *
def check_intersection(obstacles, start_point, end_point):
    """
    Vérifie si le segment de ligne entre start_point et end_point intersecte un obstacle.
    :param obstacles: Liste des obstacles dans l'environnement.
    :param start_point: Instance de Position représentant le point de départ du segment.
    :param end_point: Instance de Position représentant le point d'arrivée du segment.
    :return: Booléen indiquant si une intersection est trouvée.
    """
    for obstacle in obstacles:
        # Convertir les points de début et de fin de l'obstacle et du segment en coordonnées numpy pour faciliter les calculs
        p1 = np.array([obstacle.start.x, obstacle.start.y])
        p2 = np.array([obstacle.end.x, obstacle.end.y])
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

def calculer_puissance_recue(emetteur, recepteur, chemin_obstacles):
    """
    Calcule la puissance reçue par un récepteur en prenant en compte les réflexions et transmissions à travers les obstacles.

    :param emetteur: L'émetteur du signal.
    :param recepteur: Le récepteur du signal.
    :param chemin_obstacles: Liste des tuples d'obstacles et du type d'interaction ('reflexion' ou 'transmission') rencontrés par le signal.
    :return: La puissance reçue par le récepteur ajustée en fonction des interactions.
    """
    # Initialisation de la puissance reçue en espace libre
    freq = 60e9  # Fréquence en Hz (60 GHz pour IEEE 802.11ay)
    c = 3e8  # Vitesse de la lumière en m/s
    lambda_ = c / freq  # Longueur d'onde en mètres
    distance = np.sqrt((emetteur.position.x - recepteur.position.x) ** 2 +
                       (emetteur.position.y - recepteur.position.y) ** 2)
    puissance_libre_dB = 20 * np.log10(lambda_ / (4 * np.pi * distance))

    # Ajustement initial de la puissance reçue avec la puissance de l'émetteur et les gains des antennes en [dBW]
    puissance_ajustee_dB = emetteur.power + emetteur.gain + recepteur.gain + puissance_libre_dB

    # Application des pertes dues aux interactions
    for obstacle, interaction_type in chemin_obstacles:
        if interaction_type == 'reflexion':
            theta_i = calculer_angle_incidence(emetteur.position, recepteur.position)
            gamma_perp = calculer_gamma_perp(obstacle, theta_i)
            # Convertir le coefficient de réflexion en dB
            perte_dB = 20 * np.log10(abs(gamma_perp))
        elif interaction_type == 'transmission':
            # Pour simplifier, considérons une transmission idéale sans perte
            perte_dB = 0  # Dans un cas réel, il faudrait calculer la perte due à la transmission!!!

        puissance_ajustee_dB -= perte_dB  # Soustraire les pertes en dB

    return puissance_ajustee_dB



