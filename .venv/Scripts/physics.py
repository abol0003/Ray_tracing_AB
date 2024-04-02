import numpy as np

def calculer_angle_incidence(position_emetteur, position_recepteur):
    """
    Calcule l'angle d'incidence d'un rayon entre l'émetteur et le récepteur.
    """
    delta_x = position_emetteur.x - position_recepteur.x
    delta_y = position_emetteur.y - position_recepteur.y
    return np.arctan2(delta_y, delta_x)

def calculer_gamma_perp(obstacle, theta_i, frequency):
    # Constants
    mu0 = 4 * np.pi * 1e-7  # Perméabilité du vide
    eps0 = 8.854187817e-12  # Permittivité du vide

    # Impédance intrinsèque du vide
    Z0 = np.sqrt(mu0 / eps0)

    # Calcul de l'impédance du matériau de l'obstacle
    # Noter que wall.material.permittivite est la permittivité relative du matériau
    # et wall.material.conductivite est sa conductivité
    eps_r = obstacle.material.permittivite
    sigma = obstacle.material.conductivite
    omega = 2 * np.pi * frequency  # Fréquence angulaire de l'onde

    # Calcul de l'impédance du matériau de l'obstacle
    Z2 = np.sqrt((mu0 * omega) / (sigma + 1j * omega * eps0 * eps_r))

    # Calcul de l'angle de transmission via la loi de Snell-Descartes
    # Note: La loi de Snell nécessite la permittivité relative (eps_r)
    theta_t = np.arcsin(np.sin(theta_i) / np.sqrt(eps_r))

    # Calcul du coefficient de réflexion perpendiculaire
    gammaperp = (Z0 * np.cos(theta_i) - Z2 * np.cos(theta_t)) / (Z0 * np.cos(theta_i) + Z2 * np.cos(theta_t))

    return gammaperp

def calculer_attenuation_conductivite(obstacle, theta_i):
    """
    Calcule l'atténuation due à la conductivité de l'obstacle.
    """
    s = calculer_distance_parcourue(obstacle, theta_i)
    return obstacle.material.conductivite * s

def calculer_distance_parcourue(obstacle, theta_i):
    """
    Calcule la distance parcourue par le rayon à travers l'obstacle.
    """
    theta_t = np.arcsin(np.sqrt(obstacle.material.permittivite / np.sin(theta_i) ** 2))
    return np.abs(obstacle.epaisseur / np.cos(theta_t))

def calculer_phase_accumulee(obstacle, theta_i):
    """
    Calcule la phase accumulée à travers l'obstacle.
    """
    s = calculer_distance_parcourue(obstacle, theta_i)
    theta_t = np.arcsin(np.sqrt(obstacle.material.permittivite / np.sin(theta_i) ** 2))
    return obstacle.beta * s * np.sin(theta_t) * np.sin(theta_i)

def calculer_coeff_reflexion(obstacle, position_emetteur, position_recepteur):
    """
    Utilise les fonctions auxiliaires pour calculer le coefficient de réflexion.
    """
    theta_i = calculer_angle_incidence(position_emetteur, position_recepteur)
    gamma_perp = calculer_gamma_perp(obstacle, theta_i)
    gamma_m = calculer_attenuation_conductivite(obstacle, theta_i)
    beta_s = calculer_phase_accumulee(obstacle, theta_i)

    numerateur = gamma_perp * np.exp(-2 * gamma_m) * np.exp(1j * 2 * beta_s)
    denominateur = 1 - (gamma_perp ** 2 * np.exp(-2 * gamma_m) * np.exp(1j * 2 * beta_s))

    return gamma_perp + ((1 - gamma_perp ** 2) * numerateur / denominateur)

def calculer_coeff_transmission(obstacle, position_emetteur, position_recepteur):
    """
    Utilise les fonctions auxiliaires pour calculer le coefficient de transmission.
    """
    theta_i = calculer_angle_incidence(position_emetteur, position_recepteur)
    gamma_perp = calculer_gamma_perp(obstacle, theta_i)
    gamma_m = calculer_attenuation_conductivite(obstacle, theta_i)
    beta_s = calculer_phase_accumulee(obstacle, theta_i)

    numerateur = (1 - gamma_perp ** 2) * np.exp(-gamma_m)
    denominateur = 1 - (gamma_perp ** 2 * np.exp(-2 * gamma_m) * np.exp(1j * 2 * beta_s))

    return numerateur / denominateur
