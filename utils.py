from graph import *
import params
import sys

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
    if params.debug:
        print("source vertex with id: {} now have adjacent list: {}".format(source.get_id(), source.get_connections()))
        print("dest vertex with id: {} now have adjacent list: {}\n".format(dest.get_id(), dest.get_connections()))


def print_world_state():
    # TODO: refactor to print actual desired state
    print("state")


# Dijkstra shortest path implementation

def dijkstra_dist(start_vertex):
    # Stores distance of each
    # vertex from source vertex
    g = params.world_graph
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
            print("Path not found!!");
            return;
        print_path(path, path[i], s);
        print(path[i] + " ");


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
