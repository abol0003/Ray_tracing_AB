from position import Position

class Emitter:

    def __init__(self, position, power, frequency, gain):
        self.position = position
        self.power = power
        self.frequency = frequency
        self.gain = gain  # Ajout de l'attribut gain

    def draw(self, canvas, scale=50):
        emitter_x, emitter_y = self.position.get_x() * scale, self.position.get_y() * scale
        emitter_radius = 0.05 * scale  # Taille visuelle de l'émetteur
        canvas.create_oval(emitter_x - emitter_radius, emitter_y - emitter_radius,
                           emitter_x + emitter_radius, emitter_y + emitter_radius,
                           fill='blue', outline='black')



