import tkinter as tk

class Emitter:
    def __init__(self, position, power, frequency):
        self.position = position
        self.power = power
        self.frequency = frequency

    def draw(self, canvas, scale=50):
        emitter_x, emitter_y = self.position[0] * scale, self.position[1] * scale
        emitter_radius = 0.05 * scale  # Taille visuelle de l'émetteur
        canvas.create_oval(emitter_x - emitter_radius, emitter_y - emitter_radius,
                           emitter_x + emitter_radius, emitter_y + emitter_radius,
                           fill='blue', outline='black')
