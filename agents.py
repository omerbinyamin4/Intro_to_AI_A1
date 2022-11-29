import params
from utils import *
from minHeap import *


def calc_sum_of_people_saved(visited_vertex_id_list):
    sum_of_people_saved = 0
    for visited_vertex_id in visited_vertex_id_list:
        sum_of_people_saved += get_vertex_from_id(visited_vertex_id).get_population()
    return sum_of_people_saved


def generate_solution(node):
    solution_path = [node.id]
    while node.parent is not None:
        solution_path.insert(0, node.parent.id)
        node = node.parent
    people_saved = calc_sum_of_people_saved(solution_path)
    return (solution_path, people_saved)


class Agent:
    def __init__(self, pos, agent_type):
        self.pos = pos
        self.score = 0
        self.active = True
        self.name = ""
        self.score = 0
        self.full_path = str(pos)
        self.type = agent_type
        self.broken_list = []
        self.population_list = []
        for vertex_id in range(params.world_graph.get_num_of_vertices()):
            vertex = params.world_graph.get_vertex(vertex_id)
            if vertex.has_population():
                self.population_list.append(vertex_id)

    def get_active_status(self):
        return self.active

    def is_saviour(self):
        return (self.type == params.AGENT_TYPE_HUMAN or
                self.type == params.AGENT_TYPE_STUPID or
                self.type == params.AGENT_TYPE_GREEDY_SEARCH or
                self.type == params.AGENT_TYPE_A_STAR_SEARCH or
                self.type == params.AGENT_TYPE_REALTIME_A_STAR_SEARCH)

    def is_ai(self):
        return (self.type == params.AGENT_TYPE_GREEDY_SEARCH or
                self.type == params.AGENT_TYPE_A_STAR_SEARCH or
                self.type == params.AGENT_TYPE_REALTIME_A_STAR_SEARCH)

    def agent_terminate(self):
        print("{} is terminating..".format(self.name))
        self.active = False

    def print_name(self):
        print("Agents name is: {}".format(self.name))

    def get_name(self):
        return self.name

    def update_env(self, curr_dest_vertex):
        if self.is_saviour() and curr_dest_vertex.has_population():
            curr_dest_vertex.reset_population()
            self.add_to_population_list(curr_dest_vertex.get_id())
        if curr_dest_vertex.check_is_brittle():
            curr_dest_vertex.break_ver()
            self.add_to_broken_list(curr_dest_vertex.get_id())

    def update_score(self, add_score):
        self.score += add_score
        if params.debug:
            print

    def get_score(self):
        return self.score

    def calc_score_at_init(self, init_vertex):
        if params.debug:
            print("\n{} first location score".format(self.name))
            print("\tscore before update is: {}".format(self.score))
        score = 0

        if self.is_saviour():
            score = (init_vertex.get_population() * 1000)
        elif self.type == params.AGENT_TYPE_SABOTEUR:
            if init_vertex.brittle_not_broken():
                score += 1000
        else:
            params.agent_type_doesnt_exist(self.type)

        self.score += score
        if params.debug:
            print("\tthis round score is: {}".format(score))
            print("\tscore after update is: {}".format(self.score))
        return

    def calc_score(self, src_vertex, dest_vertex):
        if params.debug:
            print("score summary for {}:".format(self.name))
            print("\tscore before update is: {}".format(self.score))
        time_taken = src_vertex.get_weight(dest_vertex.get_id())
        score = 0

        if self.is_saviour():
            score = (dest_vertex.get_population() * 1000) - time_taken
        elif self.type == params.AGENT_TYPE_SABOTEUR:
            score -= time_taken
            if dest_vertex.brittle_not_broken():
                score += 1000
        else:
            params.agent_type_doesnt_exist(self.type)

        self.score += score
        if params.debug:
            print("\tthis round score is: {}".format(score))
            print("\tscore after update is: {}".format(self.score))
        return

    def print_agent(self):
        print(self.name + ":")
        print("\tAgent position is: " + str(self.pos))
        print("\tAgent score is: " + str(self.score))

    def update_full_path(self, next_vertex_idx):
        self.full_path += "->{}".format(str(next_vertex_idx))

    def add_to_broken_list(self, vertex_id, broken_list):
        vertex = params.world_graph.get_vertex(vertex_id)
        if vertex.check_is_brittle() and vertex_id not in broken_list:
            broken_list.append(vertex_id)

    def add_to_population_list(self, vertex_id, pop_list):
        if vertex_id not in pop_list:
            pop_list.append(vertex_id)
        else:
            print_error_and_exit("Tried to add to population list already existing vertex_id")

    def remove_from_population_list(self, vertex_id, pop_list):
        if vertex_id in pop_list:
            pop_list.remove(vertex_id)
        else:
            print_error_and_exit("Tried to remove from population list a non existing node")


class Human(Agent):
    def __init__(self, pos):
        super().__init__(pos, params.AGENT_TYPE_HUMAN)
        self.name = "human {}".format(params.human_id)
        params.human_id = params.human_id + 1

        init_vertex = params.world_graph.get_vertex(self.pos)
        self.calc_score_at_init(init_vertex)
        self.update_env(init_vertex)

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
            print("{} full path is: {}".format(self.name, self.full_path))

        self.pos = curr_dest_vertex_index
        print("{} finished acting\n".format(self.get_name()))


class Stupid(Agent):
    def __init__(self, pos):
        super().__init__(pos, params.AGENT_TYPE_STUPID)
        self.name = "stupid {}".format(params.stupid_id)
        params.stupid_id += 1

        init_vertex = params.world_graph.get_vertex(self.pos)
        self.calc_score_at_init(init_vertex)
        self.update_env(init_vertex)

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
            print("{} full path is: {}".format(self.name, self.full_path))

        self.pos = curr_dest_vertex_index
        print("{} finished acting\n".format(self.get_name()))


class Saboteur(Agent):
    def __init__(self, pos):
        super().__init__(pos, params.AGENT_TYPE_SABOTEUR)
        self.name = "saboteur {}".format(params.saboteur_id)
        params.saboteur_id += 1

        init_vertex = params.world_graph.get_vertex(self.pos)
        self.calc_score_at_init(init_vertex)
        self.update_env(init_vertex)

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
            print("{} full path is: {}".format(self.name, self.full_path))

        self.pos = curr_dest_vertex_index
        print("{} finished acting\n".format(self.get_name()))


# Search Agents (task #2)

class AI_Agent(Agent):
    def __init__(self, pos, h_func, agent_type):
        super().__init__(pos, agent_type)
        self.fringe = MinHeap()
        self.h_func = h_func
        self.num_of_expands = 0
        self.node_hash = 0

        # initialize fringe to start point
        g_init = 0
        first_node = self.create_node(pos, None, self.broken_list, self.population_list, g_init)
        first_heap_element = HeapElement(self.calc_f(first_node), first_node)
        self.fringe.insert_element(first_heap_element)

    def all_people_saved(self, node_population_list):
        return len(node_population_list) == 0

    def goal_test(self, node_population_list):
        if self.all_people_saved(node_population_list):
            return True
        return False

    def update_node_env(self, node_id, pop_list, broken_list):
        vertex = get_vertex_from_id(node_id)
        if vertex.has_population():
            self.remove_from_population_list(node_id, pop_list)
        if vertex.brittle_not_broken():
            self.add_to_broken_list(node_id, broken_list)

    def expand_and_insert_to_fringe(self, expanded_node):
        graph_vertex = get_vertex_from_id(expanded_node.id)
        if graph_vertex is not None:
            neigbors_h_list = []
            for neighbor_id in graph_vertex.adjacent.keys():
                parent = expanded_node
                neighbor_g = self.calc_new_g(expanded_node, neighbor_id)
                neighbor_node = self.create_node(neighbor_id, parent, expanded_node.broken_nodes,
                                                 expanded_node.nodes_with_population, neighbor_g)
                neighbor_node.print_search_tree_node()
                neighbor_f = self.calc_f(neighbor_node)
                self.fringe.insert_element(HeapElement(neighbor_f, neighbor_node))
                neigbors_h_list.append(neighbor_f - neighbor_g)
            self.num_of_expands += 1
            return neigbors_h_list
        else:
            print_error_and_exit("Given invalid vertex_id")

    def calc_new_g(self, curr_node, next_node_id):
        curr_vertex = get_vertex_from_id(curr_node.id)
        edge_weight = curr_vertex.get_weight(next_node_id)
        return curr_node.g + edge_weight

    def create_node(self, id, parent, broken_list, population_list, g):
        new_popluation_list = population_list.copy()
        if id in new_popluation_list:
            new_popluation_list.remove(id)
        h_func_calc = self.h_func(get_shortest_path_clique(id, new_popluation_list, broken_list))
        new_broken_list = broken_list.copy()
        curr_vertex = get_vertex_from_id(id)
        if curr_vertex.is_brittle and id not in new_broken_list:
            new_broken_list.append(id)
        new_node = Search_tree_node(id, parent, new_broken_list, new_popluation_list, g, h_func_calc, self.node_hash)
        self.node_hash += 1
        return new_node

    def calc_f(self, node):
        if self.type == params.AGENT_TYPE_GREEDY_SEARCH:
            return node.h
        if self.type == params.AGENT_TYPE_A_STAR_SEARCH:
            return node.g + node.h
        print_error_and_exit("agent type not supported: {}".format(self.type))


class Greedy_search(AI_Agent):
    def __init__(self, pos, h_func):
        super().__init__(pos, h_func, params.AGENT_TYPE_GREEDY_SEARCH)
        self.name = "greedy stupid"

    def act(self):
        while True:
            print("--------- started iteration ------------")
            # If fringe is empty, search agent failed and should return none
            if self.fringe.is_empty():
                return result(None, 0, 0, False, self.num_of_expands)

            # Pop top node in fringe
            curr_heap_element = self.fringe.extract_min()
            curr_node = curr_heap_element.value
            if params.debug:
                print("---- curr_expanded_node")
                curr_node.print_search_tree_node()
                print("----")

            (solution_path, people_saved) = generate_solution(curr_node)

            # If popped node has infi as heuristic function value, There is no solution
            if curr_node.h == params.infi:
                return result(solution_path, people_saved, curr_node.g, False, self.num_of_expands)

            # Check if goal_test is achieved - if yes finish simulation with solution
            if self.goal_test(curr_node.nodes_with_population):
                return result(solution_path, people_saved, curr_node.g, True, self.num_of_expands)

            self.expand_and_insert_to_fringe(curr_node)

            print("--------- finished iteration ------------")


class A_star_search(AI_Agent):
    def __init__(self, pos, h_func):
        super().__init__(pos, h_func, params.AGENT_TYPE_A_STAR_SEARCH)
        self.close = []
        self.name = "A_star search"

    def add_to_close(self, vertex_id, g, h):
        self.close.append({"id": vertex_id, "f": g + h})

    def should_insert_to_close(self, curr_node):
        for dict in self.close:
            if dict["id"] == curr_node.id:  # Found node with same id in close
                if self.calc_f(curr_node) < dict["f"]:
                    self.close.remove(dict)  # TODO: verify if indeed required
                    return True
                else:
                    return False
        return True  # node with same id doesn't exist in close

    def act(self):
        print("{} started acting\n".format(self.get_name()))

        while True:
            print("--------- started iteration ------------")
            # If fringe is empty, search agent failed and should return none
            if self.fringe.is_empty():
                return result(None, 0, 0, False, self.num_of_expands)

            # Pop top node in fringe
            curr_heap_element = self.fringe.extract_min()
            curr_node = curr_heap_element.value
            if params.debug:
                print("---- curr_expanded_node")
                curr_node.print_search_tree_node()
                print("----")

            (solution_path, people_saved) = generate_solution(curr_node)

            # If popped node has infi as heuristic function value, There is no solution
            if curr_node.h == params.infi:
                return result(solution_path, people_saved, curr_node.g, False, self.num_of_expands)

            # Check if goal_test is achieved - if yes finish simulation with solution
            if self.goal_test(curr_node.nodes_with_population):
                return result(solution_path, people_saved, curr_node.g, True, self.num_of_expands)

            if not self.should_insert_to_close(curr_node):
                continue

            self.add_to_close(curr_node.id, curr_node.g, curr_node.h)
            if params.debug:
                print(self.close)

            neigbors_h_list = self.expand_and_insert_to_fringe(curr_node)
            if all_infi(neigbors_h_list):
                dict_to_remove = {"id": curr_node.id, "f": self.calc_f(curr_node)}
                self.close.remove(dict_to_remove)
            print("--------- finished iteration ------------")


class realtime_A_star_search(AI_Agent):
    def __init__(self, pos, h_func):
        super().__init__(pos, h_func, params.AGENT_TYPE_REALTIME_A_STAR_SEARCH)
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
                self.pos = so_far_sol[1]  # move agent one step further
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


class solution:
    def __init__(self, solution_path, people_saved, sum_of_weights):
        self.solution_path = solution_path
        self.people_saved = people_saved
        self.sum_of_weights = sum_of_weights

    def print_solution(self):
        print("solution_path: {}".format(self.solution_path))
        print("people_saved: {}".format(self.people_saved))
        print("sum_of_weights: {}".format(self.sum_of_weights))


class result:
    def __init__(self, solution_path, people_saved, sum_of_weights, is_success, expands):
        self.solution_path = solution_path
        self.people_saved = people_saved
        self.sum_of_weights = sum_of_weights
        self.success = is_success
        self.num_of_expands = expands

    def print_result(self):
        print("result status: {}".format(self.success))
        if self.success:
            print("solution_path: {}".format(self.solution_path))
            print("people_saved: {}".format(self.people_saved))
            print("sum_of_weights: {}".format(self.sum_of_weights))
            print("num of expands taken: {}".format(self.num_of_expands))
            print("time taken for search: {}".format(self.num_of_expands * params.T))
