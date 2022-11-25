from graph import *
import params
import sys
from components.minHeap import MinHeap, HeapElement

infi = sys.maxsize


def line_to_vertex(line):
    v_id = -1
    v_population = 0
    v_is_brittle = False

    for prop in line:
        if 'V' in prop:
            v_id = int(prop.split('V')[1])
        if 'P' in prop:
            v_population = int(prop.split('P')[1])
        if 'B' in prop:
            v_is_brittle = True
    if v_id == -1:
        return None
    return Vertex(v_id, v_population, v_is_brittle)


def line_to_edge(line):
    # assuming line is struct as: #E{number} source_vertex_id des_veretex_id W{edege_weight}
    source = params.world_graph.get_vertex(int(line[1]))
    dest = params.world_graph.get_vertex(int(line[2]))
    source.add_neighbor(dest.id, int(line[3].split('W')[1]))
    dest.add_neighbor(source.id, int(line[3].split('W')[1]))


def print_world_state():
    print("###### WORLD STATE ######\n")
    for vertex in params.world_graph.vert_dict:
        params.world_graph.get_vertex(vertex).print_vertex()
    for agent in params.agents_list:
        agent.print_agent()
    print("###### FINISHED WORLD STATE ######\n")


# Dijkstra shortest path implementation

def dijkstra_dist(start_vertex, g):
    # Stores distance of each
    # vertex from source vertex
    dist = [infi for i in range(g.num_vertices)]

    # bool array that shows
    # whether the vertex 'i'
    # is visited or not
    visited = [False for i in range(g.num_vertices)]

    # for i in range(g.num_vertices):
    #     path[i] = -1
    path = [-1 for i in range(g.num_vertices)]
    dist[start_vertex.id] = 0
    current_vertex = start_vertex

    # Set of vertices that has
    # a parent (one or more)
    # marked as visited
    sett = set()
    while True:
        # Mark current_vertex as visited
        visited[current_vertex.id] = True
        for neighbor in current_vertex.adjacent.keys():
            if visited[neighbor]:
                continue

            # Inserting into the
            # visited vertex
            sett.add(neighbor)
            alt_dist = dist[current_vertex.id] + current_vertex.adjacent[neighbor]

            # Condition to check the distance
            # is correct and update it
            # if it is minimum from the previous
            # computed distance
            if alt_dist < dist[neighbor]:
                dist[neighbor] = alt_dist
                path[neighbor] = current_vertex.id

        if current_vertex.id in sett:
            sett.remove(current_vertex.id)
        if len(sett) == 0:
            break

        # The new current_vertex
        min_dist = infi
        next_id = 0

        # Loop to update the distance
        # of the vertices of the graph
        for vertex_id in sett:
            if dist[vertex_id] < min_dist:
                min_dist = dist[vertex_id]
                next_id = vertex_id
        current_vertex = g.get_vertex(next_id)

    return dist, path


def print_path(path, i, s):
    if i != s:

        # Condition to check if
        # there is no path between
        # the vertices
        if path[i] == -1:
            print("Path not found!!")
            return
        print_path(path, path[i], s)
        print(path[i] + " ")


# pick the shortest path dest vertex
# if two or more vertices have the same path length, pick the one with lowest population
def pick_best_dest(dist):
    min_dist = 1000000000
    min_population = 1000000000
    for i in range(len(dist)):
        if dist[i] <= min_dist and params.world_graph.get_vertex(i).population <= min_population:
            return i


def pick_best_brittle_dest(dist):
    min_dist = 1000000000
    best_v_id = -1
    for i in range(len(dist)):
        if dist[i] < min_dist and params.world_graph.get_vertex(i).is_brittle:
            best_v_id = i
    return best_v_id


def all_infi(dist):
    for idx in dist:
        if idx != infi:
            return False
    return True


# Returns index of vertex to choose to go to next, or -1 if doesn't exist
def min_dist_with_cond(dist, agent_type):
    # 0 is always the distance to current index, which we don't want to select.
    dist[dist.index(0)] = infi
    while (not all_infi(dist)):
        curr_vertex_dist = min(dist)
        if curr_vertex_dist == infi:  # vertex is unreachable or self
            return -1
        curr_vertex = params.world_graph.get_vertex(dist.index(curr_vertex_dist))
        if (agent_type == params.AGENT_TYPE_STUPID) and (
                curr_vertex.has_population()):  # Found good vertex for stupid greedy
            return dist.index(curr_vertex_dist)
        elif (agent_type == params.AGENT_TYPE_SABOTEUR) and (
                curr_vertex.brittle_not_broken()):  # Found good vertex for saboteur
            return dist.index(curr_vertex_dist)

        dist[dist.index(curr_vertex_dist)] = infi
    return -1


# Extracts next vertex in path by traveling from dest to src
def extract_next_vertex_in_path(path, src_vertex_index, dest_vertex_index):
    # Start trip from dest_index
    prev_vertex_index = dest_vertex_index
    next_vertex_index = path[prev_vertex_index]
    # Run until find of src, and return the previous vertex in that path
    while next_vertex_index != src_vertex_index:
        prev_vertex_index = next_vertex_index
        next_vertex_index = path[prev_vertex_index]
    return prev_vertex_index


# deprecated
# def convert_world_to_shortest_paths_clique(g):
#     clique = params.world_clique
#
#     # copy all vertices to new clique graph
#     for vertex in g.get_vertices_values():
#         clique.add_vertex(Vertex(vertex.id, vertex.population, False))
#
#     # add edges representing shortest path between all vertices in g
#     for vertex in g.get_vertices_values():
#         (dist, path) = dijkstra_dist(vertex, params.world_graph)
#         for shortest_path in dist:
#             if dist.index(shortest_path) != vertex.id and shortest_path != infi:
#                 g_dest_vertex = g.get_vertex(dist.index(shortest_path))
#                 clique.add_edge(Vertex(vertex.id, vertex.population, False),
#                                 Vertex(g_dest_vertex.id, g_dest_vertex.population, False), shortest_path)


def get_shortest_path_clique(src, populated_vertices_id_list, broken_vertices_id_list):
    world_graph_copy = Graph()
    world_graph_copy.copy_graph(params.world_graph, broken_vertices_id_list)
    clique = Graph()
    # add all vertices to the new clique
    clique.add_vertex(
        Vertex(src, params.world_graph.get_vertex(src).get_population, params.world_graph.get_vertex(src).is_brittle))
    for v_id in populated_vertices_id_list:
        clique.add_vertex(Vertex(v_id, params.world_graph.get_vertex(v_id).get_population,
                                 params.world_graph.get_vertex(v_id).is_brittle))
    # add all edges to the new clique
    for vertex in clique.get_vertices_values():
        (dist, path) = dijkstra_dist(world_graph_copy.get_vertex(vertex.id), world_graph_copy)
        for shortest_path in dist:
            dest_vertex_id = dist.index(shortest_path)
            if dest_vertex_id != vertex.id and shortest_path != infi and dest_vertex_id in clique.get_vertices_keys():
                dest_vertex = clique.get_vertex(dest_vertex_id)
                clique.add_edge(vertex, dest_vertex, shortest_path)

    return clique


def min_key_for_prim(g, key, mst_set):
    min = infi
    for vertex_id in g.get_vertices_keys():
        if key[vertex_id] < min and mst_set[vertex_id] == False:
            min = key[vertex_id]
            min_id = vertex_id

    return min_id


def get_mst_sum(g):
    key = {}
    mst_set = {}

    for vertex_id in g.get_vertices_keys():
        key[vertex_id] = infi
        mst_set[vertex_id] = False

    key[list(key.keys())[0]] = 0

    for _ in g.get_vertices_keys():
        u_id = min_key_for_prim(g, key, mst_set)
        mst_set[u_id] = True

        for neighbor_id in g.get_vertex(u_id).adjacent.keys():
            weight = g.get_vertex(u_id).get_weight(neighbor_id)
            if mst_set[neighbor_id] == False and key[neighbor_id] > weight:
                key[neighbor_id] = weight

    weights_sum = 0
    for weight in key.values():
        weights_sum += weight

    return weights_sum
