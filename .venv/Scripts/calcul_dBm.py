import numpy as np

def totalW(ray): #ok
    """
    Calcule la puissance totale reçue en W pour un rayon donné.
    Cela prend en compte les interactions (réflexions) enregistrées dans l'objet Ray.
    """
    # La puissance est déjà calculée et stockée dans l'objet Ray
    return ray.power

def totaldBm(ray): #ok
    """
    Convertit la puissance totale reçue par un rayon donné en dBm.
    """
    if ray.power > 10**(-250):  # Filtrer les puissances extrêmement faibles
        dBm = 10 * np.log10(ray.power / 10**(-3))  # Conversion en dBm
        return dBm
    return -np.inf  # Retourne une valeur infiniment petite si la puissance est sous le seuil

