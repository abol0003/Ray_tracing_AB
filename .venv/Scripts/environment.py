import tkinter as tk
from emitter import Emitter
from receiver import Receiver
from position import Position
from material import Material
from obstacle import Obstacle


class Environment:
    def __init__(self):
        self.obstacles = []
        self.emitters = []
        self.receivers = []
        self.materials = {}
        self.init_materials()
        self.init_obstacles()
        self.init_emitters()
        self.init_receivers()
        self.rays =[]
    def init_materials(self):
        # Initialisation des matériaux avec des instances de la classe Material
        self.materials['concrete'] = Material('concrete', 6.4954, 1.43, 'black')
        self.materials['cloison'] = Material('cloison', 2.7, 0.005346, 'red')
        self.materials['glass'] = Material('glass', 6.3919, 0.000107, 'lightblue')
        self.materials['metal'] = Material('metal', 1, 10**7, 'grey')

    def init_obstacles(self):
        # Murs en béton
        self.obstacles.append(Obstacle(Position(0, 0), Position(15, 0), self.materials['concrete'], 0.3))
        self.obstacles.append(Obstacle(Position(15, 0), Position(15, 4), self.materials['concrete'], 0.3))
        self.obstacles.append(Obstacle(Position(7, 0), Position(7, 4), self.materials['concrete'], 0.3))
        self.obstacles.append(Obstacle(Position(0, 0), Position(0, 8), self.materials['concrete'], 0.3))
        self.obstacles.append(Obstacle(Position(0, 8), Position(6, 8), self.materials['concrete'], 0.3))
        self.obstacles.append(Obstacle(Position(4, 8), Position(4, 6), self.materials['concrete'], 0.3))
        self.obstacles.append(Obstacle(Position(4, 6), Position(9, 6), self.materials['concrete'], 0.3))
        self.obstacles.append(Obstacle(Position(9, 6), Position(9, 8), self.materials['concrete'], 0.3))
        self.obstacles.append(Obstacle(Position(9, 8), Position(12, 8), self.materials['concrete'], 0.3))

        # Cloisons
        self.obstacles.append(Obstacle(Position(4, 0), Position(4, 4), self.materials['cloison'], 0.1))
        self.obstacles.append(Obstacle(Position(4, 4), Position(5, 4), self.materials['cloison'], 0.1))
        self.obstacles.append(Obstacle(Position(0, 5), Position(4, 5), self.materials['cloison'], 0.1))
        self.obstacles.append(Obstacle(Position(6, 4), Position(9, 4), self.materials['cloison'], 0.1))
        self.obstacles.append(Obstacle(Position(11, 0), Position(11, 4), self.materials['cloison'], 0.1))
        self.obstacles.append(Obstacle(Position(11, 4), Position(10, 4), self.materials['cloison'], 0.1))

        # Baie vitrée
        self.obstacles.append(Obstacle(Position(12, 8), Position(15, 4), self.materials['glass'], 0.05))

        # Ascenseur en métal
        self.obstacles.append(Obstacle(Position(4.25, 6.25), Position(5.755, 7.755), self.materials['metal'], 0.05))
        self.obstacles.append(Obstacle(Position(5.755, 6.15), Position(5.76, 7.855), self.materials['metal'], 0.05))

    def init_emitters(self):
        # ajout d'un émetteur
        self.emitters.append(Emitter(Position(9.4, 7), 10, 60, 1.7))

    def init_receivers(self):
        # Exemple d'ajout d'un récepteur
        receiver_position = Position(13, 3)  # Position du récepteur dans l'environnement (x, y)
        receiver_sensitivity = -90  # Sensibilité du récepteur en dBm
        receiver_gain = 2  # Gain de l'antenne du récepteur en dBi
        receiver_frequency = 60e9  # Fréquence de fonctionnement en Hz (60 GHz pour IEEE 802.11ay)
        receiver_bandwidth = 2e9  # Largeur de bande en Hz

        # Création de l'instance du récepteur et ajout à la liste des récepteurs
        self.receivers.append(Receiver(receiver_position, receiver_sensitivity, receiver_gain))

    def draw(self, canvas, scale=50):
        for obstacle in self.obstacles:
            obstacle.draw(canvas, scale)

        for emitter in self.emitters:
            emitter.draw(canvas, scale)

        for receiver in self.receivers:
            receiver.draw(canvas, scale)




# Création de la fenêtre Tkinter et du Canvas
def create_window_with_environment():
    root = tk.Tk()
    root.title("Simulation de l'Environnement")
    canvas = tk.Canvas(root, width=900, height=600, background='white')  # Ajusté pour la taille des obstacles
    canvas.pack(fill="both", expand=True)

    env = Environment()
    env.draw(canvas)

    root.mainloop()


create_window_with_environment()
