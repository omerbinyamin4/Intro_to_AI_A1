import params
from utils import dijkstra_dist, pick_best_brittle_dest, path_exists

class Agent:
    def __init__(self, pos):
        self.pos = pos
        self.score = 0
        self.active = True
        self.name = ""

    def get_active_status(self):
        return self.active

    def agent_terminate(self):
        print("{} is terminating..".format(self.name))
        self.active = False

    def print_name(self):
        print("Agents name is: {}".format(self.name))

class Human(Agent):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "human {}".format(params.human_id)
        params.human_id += 1

    def act(self):
        print("human acted\n")
        self.agent_terminate()

class Stupid(Agent):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "stupid {}".format(params.stupid_id)
        params.stupid_id += 1

    def act(self):
        # TODO: ambiguity: should an agent make the changes in the environment by himself or return the changes that
        #  should be done and the simulator will perform them?

        print("stupid greedy agent start acting\n")
        # calculate all paths
        (dist, path) = dijkstra_dist(params.world_graph.get_vertex(self.pos))
        print(dist)
        print(path)
        if not path_exists(path):
            self.agent_terminate
            return
        # pick vertex which has the shortest path to from agent pos
        # dest = pick_best_dest(dist) TODO: should prefer lower population or only lower index?
        dest_vertex = min(dist)
        # update environment
        params.world_graph.get_vertex(dest_vertex).reset_population()
        for v in params.world_graph.vert_dict:
            for stop in path:
                if stop > -1 and params.world_graph.get_vertex(stop).is_brittle:
                    was_removed = params.world_graph.get_vertex(v).adjacent.pop(stop, False)
        # change state
        curr_action_score = calc_score(params.world_graph.get_vertex(dest_vertex).get_population(), path, self.pos, dest_vertex)
        self.score += curr_action_score
        # change pos of agent to dest node
        self.pos = dest_vertex


class Saboteur(Agent):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "saboteur {}".format(params.saboteur_id)
        params.saboteur_id += 1

    def act(self):
        print("saboteur agent start acting\n")
        # calculate all paths TODO: it is pretty bruteforce, not sure if we can/want calculate only paths to brittle
        #  nodes
        (dist, path) = dijkstra_dist(params.world_graph.get_vertex(self.pos))
        if not path_exists(path):
            self.agent_terminate
            return
        # pick vertex which has the shortest path to from agent pos
        # dest = pick_best_dest(dist) TODO: should prefer lower population or only lower index?
        dest = pick_best_brittle_dest(dist)
        if dest == -1:
            return
        # update environment
        for v in params.world_graph.vert_dict:
            v.adjacent.pop(dest)

        # change state
        curr_action_score = calc_score(0, path, self.pos, dest)
        self.score += curr_action_score
        # change pos of agent to dest node
        self.pos = dest


def calc_score(rescued_population, path, source, dest):
    curr = dest
    time_taken = 0
    while dest != source:
        time_taken += params.world_graph.get_vertex(path[curr]).get_weight(curr)
        curr = path[curr]
    print("time taken: {}".format(time_taken))
    return (rescued_population * 1000) - time_taken
