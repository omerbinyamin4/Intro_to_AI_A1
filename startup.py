
from utils import *
from graph import *
from agents import *
import params


def init_graph_from_file(param):
    input_file = open('input.txt', 'r')
    lines = input_file.readlines()
    # TODO: deal with empty files or files with no vertices
    for line in lines:
        line = line.split()
        if len(line) == 0:
            continue
        if '#V' in line[0]:
            new_v = line_to_vertex(line)
            if new_v is not None:
                params.world_graph.add_vertex(new_v)
        if '#E' in line[0] and len(line) == 4:
            line_to_edge(line)
    input_file.close()

def check_pos_in_range(pos):
    if ((pos < -1) or (pos > params.world_graph.num_vertices - 1)):
        print("### pos {} is not valid ###\n"
        "possible positions are 0-{} or -1 for no agents\n"
        "Existing...\n".format(pos, params.world_graph.num_vertices - 1))
        exit(0)


def startup():
    init_graph_from_file('./input.txt')
    human_pos = input("enter start position for each human agent (i.e: 1,1,0)\n"
                          "possible positions are 0-{}\n"
                          "enter -1 for no human agents\n"
                          .format(params.world_graph.num_vertices - 1)).split(',')

    stupid_greedy_pos = input("enter start position for each stupid greedy agent (i.e: 1,1,0)\n"
                              "possible position are 0-{}\n"
                              "enter -1 for no stupid greedy agents\n"
                              .format(params.world_graph.num_vertices - 1)).split(',')

    saboteur_pos = input("enter start position for each saboteur agent (i.e: 1,1,0)\n"
        "possible positions are 0-{}\n"
        "enter -1 for no saboteur agents\n"
        .format(params.world_graph.num_vertices - 1)).split(',')

    for pos in human_pos:
        check_pos_in_range(int(pos))
        params.agents_list.append(Human(pos))

    for pos in stupid_greedy_pos:
        check_pos_in_range(int(pos))
        params.agents_list.append(Stupid(pos))

    for pos in saboteur_pos:
        check_pos_in_range(int(pos))
        params.agents_list.append(Saboteur(pos))

    simulate()
    print("simulation ended.\n")


def simulate():
    print("## simulation started... ##\n")

    while params.should_simulate:
        for agent in params.agents_list:
            if params.should_simulate:
                agent.act()
                print_world_state()


if __name__ == '__main__':
    startup()
