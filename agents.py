import params
from utils import dijkstra_dist, pick_best_brittle_dest
from components.minHeap import MinHeap, HeapElement

human_id = 0


class Agent:
    def __init__(self, pos):
        self.pos = pos
        self.score = 0
        self.active = True
        self.name = ""
        self.score = 0

    def get_active_status(self):
        return self.active

    def agent_terminate(self):
        print("{} is terminating..".format(self.name))
        self.active = False

    def print_name(self):
        print("Agents name is: {}".format(self.name))

    def get_name(self):
        return self.name

    def update_env(self, curr_dest_vertex, dest_vertex_index):
        if curr_dest_vertex.get_id() == dest_vertex_index: # vertex we are traveling to has population
            curr_dest_vertex.reset_population()
        if curr_dest_vertex.check_is_brittle():
            curr_dest_vertex.break_ver()

    def update_score(self, add_score):
        self.score += add_score
        if params.debug:
            print

    def get_score(self):
        return self.score

    def calc_score(self, src_vertex, dest_vertex):
        if params.debug:
            print("score before update is: {}".format(self.score))
        time_taken = src_vertex.get_weight(dest_vertex.get_id())
        score = (dest_vertex.get_population() * 1000) - time_taken
        self.score += score
        if params.debug:
            print("this round score is: {}".format(score))
            print("score after update is: {}".format(self.score))
        return

class Human(Agent):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "human {}".format(params.human_id)
        params.human_id = params.human_id + 1

    def act(self):
        print("human acted\n")
        self.agent_terminate()


class Stupid(Agent):
    def __init__(self, pos):
        super().__init__(pos)

    def act(self):
        # TODO: ambiguity: should an agent make the changes in the environment by himself or return the changes that
        #  should be done and the simulator will perform them?

        print("stupid greedy agent start acting\n")
        # calculate all paths
        (dist, path) = dijkstra_dist(params.world_graph.get_vertex(self.pos))
        print(dist)
        print(path)
        if all(p == -1 for p in path):
            params.should_simulate = False
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
        # self.score += curr_action_score
        # change pos of agent to dest node
        self.pos = curr_dest_vertex_index
        print("{} finished acting\n".format(self.get_name()))


class Saboteur(Agent):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "saboteur {}".format(params.saboteur_id)
        params.saboteur_id += 1

    def act(self):
        print("saboteur agent start acting\n")
        if not self.get_active_status():
            return "no-op"
        # calculate all paths TODO: it is pretty bruteforce, not sure if we can/want calculate only paths to brittle
        #  nodes
        (dist, path) = dijkstra_dist(params.world_graph.get_vertex(self.pos))
        if True:
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
