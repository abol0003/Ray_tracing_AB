import numpy as np
from matplotlib import pyplot as plt
from physics import *
from position import Position
from emitter import Emitter
from receiver import Receiver
import tkinter as tk
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
        self.materials['concrete'] = Material('concrete',4.8 , 0.018, 'black') #test ex4.1

        #self.materials['concrete'] = Material('concrete', 6.4954, 1.43, 'black')
        self.materials['cloison'] = Material('cloison', 2.7, 0.005346, 'red')
        self.materials['glass'] = Material('glass', 6.3919, 0.000107, 'lightblue')
        self.materials['metal'] = Material('metal', 1, 10**7, 'grey')

    def init_obstacles(self):
        # Murs en béton
        self.obstacles.append(Obstacle(Position(0, 0), Position(0, 80), self.materials['concrete'], 0.15))
        self.obstacles.append(Obstacle(Position(0, 20), Position(200, 20), self.materials['concrete'], 0.15))
        self.obstacles.append(Obstacle(Position(0, 80), Position(200, 80), self.materials['concrete'], 0.15))



    def init_emitters(self):
        # ajout d'un émetteur
        self.emitters.append(Emitter(Position(32, 10), 3, ((868.3)*(10**6)), 1.7))

    def init_receivers(self):

        # Création de l'instance du récepteur et ajout à la liste des récepteurs
        self.receivers.append(Receiver(Position(47, 65), -90, 1.7))

    def draw(self, canvas, scale=5):
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

