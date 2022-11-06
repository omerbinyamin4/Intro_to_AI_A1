import params

class Agent:
    def __init__(self, pos):
        self.pos = pos
        self.score = 0


class Human(Agent):
    def __init__(self, pos):
        super().__init__(pos)

    def act(self):
        print("human acted\n")


class Stupid(Agent):
    def __init__(self, pos):
        super().__init__(pos)

    def act(self):
        print("stupid acted\n")


class Saboteur(Agent):
    def __init__(self, pos):
        super().__init__(pos)

    def act(self):
        print("saboteur acted\n")
        params.should_simulate = False


