
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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