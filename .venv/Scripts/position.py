
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist_to_wall(self, wall):
        if wall.is_vertical():
            res = wall.get_end().get_x() - self.x
        else:
            res = abs(wall.get_end().get_y() - self.y)
        return res

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_position(self):
        return self

    def __str__(self):
        return f"({self.x}, {self.y})"

    def plot(self):
        plt.scatter(self.x, self.y)
        plt.show()