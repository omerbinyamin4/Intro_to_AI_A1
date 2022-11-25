import params
import utils
from utils import *
from components.minHeap import MinHeap, HeapElement

human_id = 0


def generate_solution(last_vertex_id):
    solution = []
    curr_sol_vertex = params.world_graph.get_vertex(last_vertex_id)
    while curr_sol_vertex.path_parent is not None:
        solution.append(curr_sol_vertex.path_parent)
        curr_sol_vertex = params.world_graph.get_vertex(curr_sol_vertex.path_parent)
    return solution


class Agent:
    def __init__(self, pos):
        self.pos = pos
        self.score = 0
        self.active = True
        self.name = ""
        self.score = 0
        self.full_path = str(pos)
        self.type = -1

    def get_active_status(self):
        return self.active

    def agent_terminate(self):
        print("{} is terminating..".format(self.name))
        self.active = False

    def print_name(self):
        print("Agents name is: {}".format(self.name))

    def get_name(self):
        return self.name

    def update_env(self, curr_dest_vertex):
        if (self.type == params.AGENT_TYPE_HUMAN) or (self.type == params.AGENT_TYPE_STUPID):
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
        score = 0

        if (self.type == params.AGENT_TYPE_STUPID) or (self.type == params.AGENT_TYPE_HUMAN):
            score = (dest_vertex.get_population() * 1000) - time_taken
        elif self.type == params.AGENT_TYPE_SABOTEUR:
            score -= time_taken
            if dest_vertex.brittle_not_broken():
                score += 1000
        else:
            params.agent_type_doesnt_exist(self.type)

        self.score += score
        if params.debug:
            print("this round score is: {}".format(score))
            print("score after update is: {}".format(self.score))
        return

    def print_agent(self):
        print(self.name + ":")
        print("\tAgent position is: " + str(self.pos))
        print("\tAgent score is: " + str(self.score) + "\n")

    def update_full_path(self, next_vertex_idx):
        self.full_path += "->{}".format(str(next_vertex_idx))

class Human(Agent):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "human {}".format(params.human_id)
        params.human_id = params.human_id + 1
        self.type = params.AGENT_TYPE_HUMAN

    def act(self):
        print("{} started acting\n".format(self.get_name()))
        src_vertex = params.world_graph.get_vertex(self.pos)
        curr_dest_vertex_index = int(input("enter next vertex to move to, or -1 to terminate\n"))
        if curr_dest_vertex_index == -1:
            self.agent_terminate()
            return
        
        curr_dest_vertex = params.world_graph.get_vertex(curr_dest_vertex_index)
        self.calc_score(src_vertex, curr_dest_vertex)
        self.update_env(curr_dest_vertex)
        self.update_full_path(curr_dest_vertex_index)

        if params.debug:
            print("{} full path is: {}".format(self.name ,self.full_path))

        self.pos = curr_dest_vertex_index
        print("{} finished acting\n".format(self.get_name()))

class Stupid(Agent):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "stupid {}".format(params.stupid_id)
        params.stupid_id += 1
        self.type = params.AGENT_TYPE_STUPID

    def act(self):
        print("{} started acting\n".format(self.get_name()))
        src_vertex = params.world_graph.get_vertex(self.pos)
        if not self.get_active_status():
            return "no-op"
        # calculate all paths
        (dist, path) = dijkstra_dist(src_vertex, params.world_graph)

        # pick vertex which has the shortest path from agent pos which has population
        dest_vertex_index = min_dist_with_cond(dist, params.AGENT_TYPE_STUPID)

        if dest_vertex_index == -1:
            self.agent_terminate()
            return
        curr_dest_vertex_index = extract_next_vertex_in_path(path, self.pos, dest_vertex_index)
        curr_dest_vertex = params.world_graph.get_vertex(curr_dest_vertex_index)
        if params.debug:
            print("chosen dest_vertex by {} is {} and first vertex in path is {}".format(self.get_name(),
                                                                                         dest_vertex_index,
                                                                                         curr_dest_vertex_index))

        self.calc_score(src_vertex, curr_dest_vertex)
        self.update_env(curr_dest_vertex)
        self.update_full_path(curr_dest_vertex_index)
        if params.debug:
            print("{} full path is: {}".format(self.name ,self.full_path))

        self.pos = curr_dest_vertex_index
        print("{} finished acting\n".format(self.get_name()))


class Saboteur(Agent):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "saboteur {}".format(params.saboteur_id)
        params.saboteur_id += 1
        self.type = params.AGENT_TYPE_SABOTEUR

    def act(self):
        print("{} started acting\n".format(self.get_name()))
        src_vertex = params.world_graph.get_vertex(self.pos)
        if not self.get_active_status():
            return "no-op"

        (dist, path) = dijkstra_dist(params.world_graph.get_vertex(self.pos), params.world_graph)

        # pick vertex which has the shortest path from agent pos which is brittle and not broken
        dest_vertex_index = min_dist_with_cond(dist, params.AGENT_TYPE_SABOTEUR)

        if dest_vertex_index == -1:
            self.agent_terminate()
            return
        
        curr_dest_vertex_index = extract_next_vertex_in_path(path, self.pos, dest_vertex_index)
        curr_dest_vertex = params.world_graph.get_vertex(curr_dest_vertex_index)
        if params.debug:
            print("chosen dest_vertex by {} is {} and first vertex in path is {}".format(self.get_name(),
                                                                                         dest_vertex_index,
                                                                                         curr_dest_vertex_index))

        self.calc_score(src_vertex, curr_dest_vertex)
        self.update_env(curr_dest_vertex)
        self.update_full_path(curr_dest_vertex_index)
        if params.debug:
            print("{} full path is: {}".format(self.name ,self.full_path))

        self.pos = curr_dest_vertex_index
        print("{} finished acting\n".format(self.get_name()))


# Search Agents (task #2)

def goal_test():
    return params.total_victims == 0


def h_func(src_id, dest_id):
    if src_id == dest_id:
        return 0
    return params.world_clique.get_vertex(src_id).get_weight(dest_id)


class Greedy_search(Agent):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "greedy stupid"
        self.fringe = MinHeap()
        # initialize fringe to start point
        self.fringe.insert_element(HeapElement(h_func(pos, pos), pos))
        self.type == params.AGENT_TYPE_GREEDY_SEARCH

    def act(self):
        print("{} started acting\n".format(self.get_name()))
        if self.fringe.is_empty():
            params.should_simulate = False
            # TODO: should return none and simulator terminate? or should also change agent state to terminate?
            return None

        curr_vertex_id = self.fringe.extract_min().value

        # ignore brittle broken (already visited vertices)
        while params.world_graph.get_vertex(curr_vertex_id).check_if_broken():
            if self.fringe.is_empty():
                params.should_simulate = False
                # TODO: should return none and simulator terminate? or should also change agent state to terminate?
                return None
            curr_vertex_id = self.fringe.extract_min().value

        curr_vertex = params.world_graph.get_vertex(curr_vertex_id)
        # rescue people and update env
        curr_vertex.reset_population()  # also reduces its population from total_victims
        if curr_vertex.check_is_brittle():
            curr_vertex.break_ver()
        if goal_test():
            params.should_simulate = False
            return generate_solution(curr_vertex_id)

        self.expand_and_insert_to_fringe(curr_vertex_id)

    def expand_and_insert_to_fringe(self, vertex_id):
        graph_vertex = params.world_graph.get_vertex(vertex_id)
        if graph_vertex is not None:
            for neighbor in graph_vertex.adjacent.keys():
                params.world_graph.get_vertex(neighbor).solution_parent = graph_vertex.id
                self.fringe.insert_element(HeapElement(h_func(neighbor, vertex_id), neighbor))


class A_star_search(Agent):
    def __init__(self, pos, h_func):
        super().__init__(pos)
        self.open = MinHeap()
        self.closed = MinHeap()
        self.h_func = h_func
        self.num_of_expands = 0
        # initialize fringe to start point
        self.open.insert_element(HeapElement(h_func(pos), pos))

    def act(self):
        if self.open.is_empty():
            self.active = False
            # TODO: should return none and simulator terminate? or should also change agent state to terminate?
            # return None

        curr_vertex_id = self.fringe.extract_min().value

        # ignore brittle broken (already visited vertices)
        while params.world_graph.get_vertex(curr_vertex_id).check_if_broken():
            curr_vertex_id = self.fringe.extract_min().value

        curr_vertex = params.world_graph.get_vertex(curr_vertex_id)
        # rescue people and update env
        curr_vertex.reset_population()  # also reduces its population from total_victims
        if curr_vertex.check_is_brittle():
            curr_vertex.break_ver()
        if goal_test():
            return generate_solution(curr_vertex_id)

        if not self.closed.contains(HeapElement(self.h(curr_vertex_id), curr_vertex_id)):
            self.closed.insert_element(HeapElement(self.h(curr_vertex_id), curr_vertex_id))
            # TODO: what if an element with same value but diff key (h(value)) exists in closed?
            if self.num_of_expands < params.expansions_limit:
                self.expand_and_insert_to_open(curr_vertex_id)
                self.num_of_expands += 1
            else:
                self.active = False
                # TODO: should return none and simulator terminate? or should also change agent state to terminate?
                # return None

    def expand_and_insert_to_open(self, vertex_id):
        graph_vertex = params.world_graph.get_vertex(vertex_id)
        if graph_vertex is not None:
            for neighbor in graph_vertex.adjacent.keys():
                neighbor.solution_parent = graph_vertex.id
                self.open.insert_element(HeapElement(self.h_func(neighbor), neighbor))

class realtime_A_star_search(Agent):
    def __init__(self, pos, h_func):
        super().__init__(pos)
        self.open = MinHeap()
        self.closed = MinHeap()
        self.h_func = h_func
        self.num_of_expands = 0
        # initialize fringe to start point
        self.open.insert_element(HeapElement(h_func(pos), pos))

    def act(self):
        if self.open.is_empty():
            self.active = False
            # TODO: should return none and simulator terminate? or should also change agent state to terminate?
            # return None

        curr_vertex_id = self.fringe.extract_min().value

        # ignore brittle broken (already visited vertices)
        while params.world_graph.get_vertex(curr_vertex_id).check_if_broken():
            curr_vertex_id = self.fringe.extract_min().value

        curr_vertex = params.world_graph.get_vertex(curr_vertex_id)
        # rescue people and update env
        curr_vertex.reset_population()  # also reduces its population from total_victims
        if curr_vertex.check_is_brittle():
            curr_vertex.break_ver()
        if goal_test():
            return generate_solution(curr_vertex_id)

        if not self.closed.contains(HeapElement(self.h(curr_vertex_id), curr_vertex_id)):
            self.closed.insert_element(HeapElement(self.h(curr_vertex_id), curr_vertex_id))
            # TODO: what if an element with same value but diff key (h(value)) exists in closed?
            if self.num_of_expands < params.user_L:
                self.expand_and_insert_to_open(curr_vertex_id)
                self.num_of_expands += 1
            else:
                so_far_sol = generate_solution(curr_vertex_id)
                self.pos = so_far_sol[1] # move agent one step further
                # TODO: update env according to the step (reset population, break vertex if brittle
                self.num_of_expands = 0
                self.active = False
                # TODO: should return none and simulator terminate? or should also change agent state to terminate?
                # return None

    def expand_and_insert_to_open(self, vertex_id):
        graph_vertex = params.world_graph.get_vertex(vertex_id)
        if graph_vertex is not None:
            for neighbor in graph_vertex.adjacent.keys():
                neighbor.solution_parent = graph_vertex.id
                self.open.insert_element(HeapElement(self.h_func(neighbor), neighbor))

