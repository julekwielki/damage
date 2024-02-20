class Cell(object):
    def __init__(self):
        self.passage = 0
        self.age = 0
        self.status = 0  # -1 - martwa, 0 - empty, 1 - normal, 2 - zmutowana, zmutowana onkogen
        self.damage = 0
        self.onco_damage = 0
        self.perm_damage = 0
        self.onco_mut = 0
        self.par_a, self.par_b = -0.001, 1  # -0.000003, 1

    def die(self):
        self.status = -1
        self.age = 0
        self.damage = 0
        self.onco_damage = 0
        self.perm_damage = 0
        self.onco_mut = 0


