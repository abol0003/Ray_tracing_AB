import numpy as np
from position import Position
from material import Material
from obstacle import Obstacle

frequency = 60e9
def calculer_angle_incidence(pos_emetteur, pos_incidence, obstacle): #ok
    """
    Calcule et renvoie l'angle d'incidence avec un émetteur et un point d'incidence donnés.
    """
    if obstacle.is_vertical():
        if pos_emetteur.x == pos_incidence.x:
            theta_i = np.pi / 2
        else:
            delta_x = pos_emetteur.x - pos_incidence.x
            delta_y = pos_emetteur.y - pos_incidence.y
            theta_i = abs(np.arctan(delta_y / delta_x))
    else:  # Si l'obstacle est horizontal
        if pos_emetteur.y == pos_incidence.y:
            theta_i = np.pi / 2
        else:
            delta_x = pos_emetteur.x - pos_incidence.x
            delta_y = pos_emetteur.y - pos_incidence.y
            theta_i = abs(np.arctan(delta_x / delta_y))

    return theta_i

def calcul_angle_trans(obstacle, theta_i):   #ok
    """
    Calcule et renvoie l'angle theta_t transmis via la loi de Snell-Descartes, en considérant
    la transition entre un matériau et l'air. Ici, on assume que la permittivité de l'air est
    approximativement équivalente à la permittivité du vide eps0 pour simplifier le calcul.
    """
    # Perméabilité relative de l'air par rapport au vide (en pratique, considérée comme ~1 pour l'air)
    eps_r_air = 1  # Approximation pour l'air
    # Perméabilité relative du matériau de l'obstacle
    eps_r_material = obstacle.material.permittivity

    theta_t = np.arcsin(np.sin(theta_i) / np.sqrt(eps_r_material))

    return theta_t



def calculer_gamma_perp(obstacle, theta_i):  #ok

    # Récupération des impédances Z_material et Z0 de l'objet obstacle
    Z_material, Z0 = obstacle.impedance(frequency)

    # Calcul de l'angle de transmission via la loi de Snell-Descartes
    theta_t = calcul_angle_trans(obstacle, theta_i)

    # Calcul du coefficient de réflexion perpendiculaire en utilisant les impédances
    # et l'angle de transmission theta_t
    gammaperp = (Z0 * np.cos(theta_i) - Z_material * np.cos(theta_t)) / (
                Z0 * np.cos(theta_i) + Z_material * np.cos(theta_t))

    return gammaperp


def calculer_gammam(obstacle, theta_i): #ok
    """
    Calcule la constante de propagation complexe.
    """
    omega=2*np.pi*frequency
    mu0 = 4 * np.pi * 1e-7
    #s = calculer_distance_parcourue(obstacle, theta_i)
    gammam= 1j*omega*np.sqrt(mu0*obstacle.material.permittivity)
    return gammam

def calculer_distance_parcourue(obstacle, theta_i): #ok
    """
    Calcule la distance parcourue par le rayon à travers l'obstacle.
    """
    theta_t = calcul_angle_trans(obstacle, theta_i)
    return np.abs(obstacle.thickness / np.cos(theta_t))


def calculer_phase_accumulee(obstacle, theta_i): #ok
    """
    Calcule la phase accumulée à travers l'obstacle, en utilisant la fréquence spécifiée
    pour calculer la valeur de beta du matériau de l'obstacle.
    """
    # Calcul de la distance parcourue par le rayon à travers l'obstacle
    s = calculer_distance_parcourue(obstacle, theta_i)

    # Calcul de l'angle de transmission theta_t
    theta_t = calcul_angle_trans(obstacle, theta_i)

    # Calcul de la valeur de beta pour le matériau de l'obstacle à la fréquence spécifiée
    beta_value = obstacle.material.beta(frequency)

    # Calcul de la phase accumulée en utilisant la valeur de beta
    phase_accumulee = 1j*2*beta_value * s * np.sin(theta_t) * np.sin(theta_i)

    return phase_accumulee


def calculer_coeff_reflexion(obstacle, position_emetteur, position_reflexion): #ok
    """
    Utilise les fonctions auxiliaires pour calculer le coefficient de réflexion.
    """
    theta_i = calculer_angle_incidence(position_emetteur, position_reflexion, obstacle)
    theta_t =calcul_angle_trans(obstacle, theta_i)
    gammap = calculer_gamma_perp(obstacle, theta_i)
    gamma_m = calculer_gammam(obstacle, theta_i)
    s = calculer_distance_parcourue(obstacle, theta_i)
    beta_s = calculer_phase_accumulee(obstacle, theta_i)

    numerateur = gammap * np.exp(-2 * gamma_m*s) * np.exp(beta_s *s)
    denominateur = 1 - ((gammap ** 2) * np.exp(-2 * gamma_m * s) * np.exp(s * beta_s))

    return gammap - ((1 - gammap ** 2)) * (numerateur / denominateur)

def calculer_coeff_transmission(obstacle, position_emetteur, position_recepteur): #ok
    """
    Utilise les fonctions auxiliaires pour calculer le coefficient de transmission.
    """
    theta_i = calculer_angle_incidence(position_emetteur, position_recepteur, obstacle)
    s = calculer_distance_parcourue(obstacle, theta_i)
    gamma_perp = calculer_gamma_perp(obstacle, theta_i)
    gamma_m = calculer_gammam(obstacle, theta_i)
    beta_s = calculer_phase_accumulee(obstacle, theta_i)

    numerateur = (1 - (gamma_perp ** 2)) * np.exp(-gamma_m * s )
    denominateur = 1 - ((gamma_perp ** 2) * np.exp(-2 * gamma_m *s) * np.exp(s* beta_s))

    return numerateur / denominateur


def transmission_totale(obstacles, position_depart, position_fin): #normalement ok
    """
    Calcule le coefficient de transmission total à travers tous les obstacles intersectés par le rayon.

    :param obstacles: Liste des obstacles dans l'environnement.
    :param position_emetteur: Position de l'émetteur.
    :param position_recepteur: Position du récepteur fictif.
    :return: Coefficient de transmission total et la distance totale parcourue à travers les obstacles.
    """
    coeff_total = 1.0
    distance_totale = 0
    for obstacle in obstacles:
        if obstacle.check_intersection(position_depart, position_fin):
            theta_i = calculer_angle_incidence(position_depart, position_fin, obstacle)
            coeff_transmission = calculer_coeff_transmission(obstacle, position_depart, position_fin)
            coeff_total *= coeff_transmission
            # Calcul de la distance parcourue dans l'obstacle
            distance_obstacle = calculer_distance_parcourue(obstacle, theta_i)
            distance_totale += distance_obstacle

    return coeff_total, distance_totale