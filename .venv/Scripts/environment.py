import tkinter as tk
from emitter import Emitter


class Environment:
    def __init__(self):
        self.obstacles = []
        self.emitters = []
        self.materials = {
            'concrete': {'permittivity': 6.4954, 'conductivity': 1.43, 'color': 'black'},
            'cloison': {'permittivity': 2.7, 'conductivity': 0.005346, 'color': 'red'},
            'glass': {'permittivity': 6.3919, 'conductivity': 0.000107, 'color': 'lightblue'},
            'metal': {'permittivity': 1, 'conductivity': 10**7, 'color': 'grey'},
        }
        self.init_obstacles()
        self.init_emitters()



    def init_obstacles(self):
        # Murs en béton
        self.obstacles.append({'start': (0, 0), 'end': (15, 0), 'material': 'concrete', 'thickness': 0.3})
        self.obstacles.append({'start': (15, 0), 'end': (15, 4), 'material': 'concrete', 'thickness': 0.3})
        self.obstacles.append({'start': (7, 0), 'end': (7, 4), 'material': 'concrete', 'thickness': 0.3})
        self.obstacles.append({'start': (0, 0), 'end': (0, 8), 'material': 'concrete', 'thickness': 0.3})
        self.obstacles.append({'start': (0, 8), 'end': (6, 8), 'material': 'concrete', 'thickness': 0.3})
        self.obstacles.append({'start': (4, 8), 'end': (4, 6), 'material': 'concrete', 'thickness': 0.3})
        self.obstacles.append({'start': (4, 6), 'end': (9, 6), 'material': 'concrete', 'thickness': 0.3})
        self.obstacles.append({'start': (9, 6), 'end': (9, 8), 'material': 'concrete', 'thickness': 0.3})
        self.obstacles.append({'start': (9, 8), 'end': (12, 8), 'material': 'concrete', 'thickness': 0.3})

        # Cloisons
        self.obstacles.append({'start': (4, 0), 'end': (4, 4), 'material': 'cloison', 'thickness': 0.1})
        self.obstacles.append({'start': (4, 4), 'end': (5, 4), 'material': 'cloison', 'thickness': 0.1})
        self.obstacles.append({'start': (0, 5), 'end': (4, 5), 'material': 'cloison', 'thickness': 0.1})
        self.obstacles.append({'start': (6, 4), 'end': (9, 4), 'material': 'cloison', 'thickness': 0.1})
        self.obstacles.append({'start': (11, 0), 'end': (11, 4), 'material': 'cloison', 'thickness': 0.1})
        self.obstacles.append({'start': (11, 4), 'end': (10, 4), 'material': 'cloison', 'thickness': 0.1})


        # Baie vitrée
        self.obstacles.append({'start': (12, 8), 'end': (15, 4), 'material': 'glass', 'thickness': 0.05})

        # Ascenseur en métal
        self.obstacles.append({'start': (4.25, 6.25), 'end': (5.755, 7.755 ), 'material': 'metal', 'thickness': 0.05}) #carré
        self.obstacles.append({'start': (5.755, 6.15), 'end': (5.76, 7.855 ), 'material': 'metal', 'thickness': 0.05}) #porte métallique

    def init_emitters(self):
        # d'ajout d'un émetteur
        self.emitters.append(Emitter(position=(9.4, 7), power=10, frequency=2.4))

    def draw(self, canvas, scale=50):
        for obstacle in self.obstacles:
            x0, y0 = obstacle['start'][0] * scale, obstacle['start'][1] * scale
            x1, y1 = obstacle['end'][0] * scale, obstacle['end'][1] * scale
            color = self.materials[obstacle['material']]['color']
            thickness = obstacle['thickness'] * scale

            if obstacle['material'] == 'metal':  # Pour l'ascenseur en métal,  un rectangle
                canvas.create_rectangle(x0, y0, x1, y1, width=thickness, fill=color)
            else:
                canvas.create_line(x0, y0, x1, y1, width=thickness, fill=color)
            # Dessiner les émetteurs
        for emitter in self.emitters:
            emitter.draw(canvas, scale)



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
