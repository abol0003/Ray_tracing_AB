class Obstacle:
    def __init__(self, start, end, material, thickness):
        self.start = start  # Doit être une instance de Position
        self.end = end      # Doit être une instance de Position
        self.material = material  # Doit être une instance de Material
        self.thickness = thickness

    def draw(self, canvas, scale=50):
        x0, y0 = self.start.get_x() * scale, self.start.get_y() * scale
        x1, y1 = self.end.get_x() * scale, self.end.get_y() * scale
        if self.material.name == 'metal':
            canvas.create_rectangle(x0, y0, x1, y1, fill=self.material.color, width=self.thickness * scale)
        else:
            canvas.create_line(x0, y0, x1, y1, fill=self.material.color, width=self.thickness * scale)

    def is_vertical(self):
        """Retourne True si l'obstacle est vertical, False sinon."""
        return self.start.x == self.end.x

    def impact_point(self, ray_start, ray_end):
        """Calcule et retourne le point d'impact d'un rayon avec l'obstacle."""
        if self.is_vertical():
            # Calcul pour un obstacle vertical.
            x_impact = self.start.x
            # Éviter la division par zéro en vérifiant si le rayon est vertical.
            if ray_start.x == ray_end.x:
                return None  # Aucun impact si le rayon est parallèle à l'obstacle.
            # Calcul de y en utilisant l'interpolation linéaire.
            y_impact = ray_start.y + (ray_end.y - ray_start.y) * (x_impact - ray_start.x) / (ray_end.x - ray_start.x)
            if min(self.start.y, self.end.y) <= y_impact <= max(self.start.y, self.end.y):
                return Position(x_impact, y_impact)
            else:
                return None
        else:
            # Calcul pour un obstacle horizontal.
            y_impact = self.start.y
            # Éviter la division par zéro en vérifiant si le rayon est horizontal.
            if ray_start.y == ray_end.y:
                return None  # Aucun impact si le rayon est parallèle à l'obstacle.
            # Calcul de x en utilisant l'interpolation linéaire.
            if ray_end.x - ray_start.x == 0:  # Évite la division par zéro
                return None
            x_impact = ray_start.x + (ray_end.x - ray_start.x) * (y_impact - ray_start.y) / (ray_end.y - ray_start.y)
            if min(self.start.x, self.end.x) <= x_impact <= max(self.start.x, self.end.x):
                return Position(x_impact, y_impact)
            else:
                return None
