from graph import *
import params


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
    source.add_neighbor(dest, int(line[3].split('W')[1]))


def print_world_state():
    # TODO: refactor to print actual desired state
    print("state")
