class Player:
    def __init__(self):
        self.alive = True
        self.arrows = 5
        self.position = None

    def shoot_arrow(self):
        if self.arrows != 0:
            self.arrows = self.arrows - 1