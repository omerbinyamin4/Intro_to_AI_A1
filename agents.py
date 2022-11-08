import params
from utils import dijkstra_dist


class Agent:
    def __init__(self, pos):
        self.pos = pos
        self.score = 0


class Human(Agent):
    def __init__(self, pos):
        # not sure what type C is, make sure this fix works
        # previous line: super().__init__(self, pos)
        super(Agent, self).__init__(self, pos)

    def act(self):
        print("human acted\n")


class Stupid(Agent):
    def __init__(self, pos):
        super(Agent, self).__init__(pos)

    def act(self):
        # TODO: ambiguity: should an agent make the changes in the environment by himself or return the changes that
        #  should be done and the simulator will perform them?

        print("stupid greedy agent start acting\n")
        # calculate all paths
        (dist, path) = dijkstra_dist(params.world_graph.get_vetex(self.pos))
        if all(p == -1 for p in path):
            params.should_simulate = False
            return
        # pick vertex which has the shortest path to from agent pos
        # dest = pick_best_dest(dist) TODO: should prefer lower population or only lower index?
        dest = min(dist)
        # update environment
        params.world_graph.get_vertex(dest).rest_population()
        for v in params.world_graph.vert_dict:
            for stop in path:
                if params.world_graph.get_vertex(stop).is_brittle:
                    v.adjacent.pop(stop)
        # change state
        curr_action_score = calc_score(params.world_graph.get_vertex(dest).get_population(), path, self.pos, dest)
        self.score += curr_action_score
        # change pos of agent to dest node
        self.pos = dest


class Saboteur(Agent):
    def __init__(self, pos):
        super(Agent, self).__init__(pos)

    def act(self):
        print("saboteur acted\n")
        params.should_simulate = False


def calc_score(rescued_population, path, source, dest):
    curr = dest
    time_taken = 0
    while dest != source:
        time_taken += params.world_graph.get_vertex(path[curr]).get_weight(curr)
        curr = path[curr]
    return (rescued_population * 1000) - time_taken
