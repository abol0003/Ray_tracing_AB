import numpy as np
class Material:
    def __init__(self, name, permittivity, conductivity, color):
        self.name = name
        self.permittivity = permittivity
        self.conductivity = conductivity
        self.color = color

    def beta(self, frequency):
        """
        Calcule et retourne le beta du matériau à une fréquence donnée.
        beta = sqrt((conductivité * omega * mu0) / 2)
        où omega = 2 * pi * frequency et mu0 = 4 * pi * 1e-7.
        """
        #mu0 = 4 * np.pi * 1e-7  # Perméabilité du vide
        omega = 2 * np.pi * frequency  # Fréquence angulaire
        c= 299792458 #vitesse lumière
        #beta_value = np.sqrt((self.conductivity * omega * mu0) / 2)
        beta_value = omega/c
        return beta_value
