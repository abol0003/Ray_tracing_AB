from position import Position
import tkinter as tk

class Receiver:
    def __init__(self, position, sensitivity, gain, frequency, bandwidth):
        """
        Initialise un nouveau récepteur.

        :param position: Objet Position représentant la position du récepteur.
        :param sensitivity: Sensibilité du récepteur en dBm.
        :param antenna_gain: Gain de l'antenne du récepteur en dBi.
        :param frequency: Fréquence de fonctionnement du récepteur en Hz.
        :param bandwidth: Largeur de bande du récepteur en Hz.
        """
        self.position = position  # position est maintenant un objet de la classe Position
        self.sensitivity = sensitivity
        self.gain = gain
        self.frequency = frequency
        self.bandwidth = bandwidth
        self.received_power = None  # Ajout d'un attribut pour stocker la puissance reçue


    def draw(self, canvas, scale=50):
        """
        Dessine le récepteur sur un canvas Tkinter.

        :param canvas: Canvas Tkinter sur lequel dessiner le récepteur.
        :param scale: Échelle pour la conversion des unités spatiales en pixels.
        """
        x, y = self.position.get_x(), self.position.get_y()
        receiver_radius = 0.05 * scale  # Taille visuelle du récepteur
        canvas.create_oval(x * scale - receiver_radius, y * scale - receiver_radius,
                           x * scale + receiver_radius, y * scale + receiver_radius,
                           fill='green', outline='black')
