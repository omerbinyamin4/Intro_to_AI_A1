import utils
from components import *
from graph import *
from agents import *
from utils import *
import params
from argparse import ArgumentParser, RawTextHelpFormatter

input_graphs = "./input_graphs"


def print_agent_list():
    print("## Agents list ##")
    for agent in params.agents_list:
        print(agent.get_name())
    print("## Finished agent list ##\n")


def init_graph_from_file(input_env):
    input_file = open(input_env, 'r')
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
                params.total_victims += new_v.population
        if '#E' in line[0] and len(line) == 4:
            line_to_edge(line)
    input_file.close()


def check_pos_in_range(pos):
    if ((pos < 0) or (pos > params.world_graph.num_vertices - 1)):
        print("### pos {} is not valid ###\n"
              "possible positions are 0-{} or -1 for no agents\n"
              "Existing...\n".format(pos, params.world_graph.num_vertices - 1))
        exit(0)


def init_agents(agents_list, agent_type):
    if int(agents_list[0]) == -1:
        return
    for pos in agents_list:
        check_pos_in_range(int(pos))
        if agent_type == params.AGENT_TYPE_HUMAN:
            params.agents_list.append(Human(int(pos)))
        elif agent_type == params.AGENT_TYPE_STUPID:
            params.agents_list.append(Stupid(int(pos)))
        elif agent_type == params.AGENT_TYPE_SABOTEUR:
            params.agents_list.append(Saboteur(int(pos)))
        elif agent_type == params.AGENT_TYPE_GREEDY_SEARCH:
            params.agents_list.append(Greedy_search(int(pos)))
        else:
            params.agent_type_doesnt_exist(agent_type)


def startup(input_env, debug_mode):
    params.debug = debug_mode
    init_graph_from_file(input_env)
    task = input("Insert task number to run:\n")
    if int(task) == 1:
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
        # TODO : can an agent start in a brittle vertex?
        init_agents(human_pos, params.AGENT_TYPE_HUMAN)
        init_agents(stupid_greedy_pos, params.AGENT_TYPE_STUPID)
        init_agents(saboteur_pos, params.AGENT_TYPE_SABOTEUR)
        simulate()
    elif int(task) == 2:
        # greedy_search_pos = input("enter start position for single greedy search agent\n"
        #                           "possible positions are 0-{}\n"
        #                           "enter -1 for no saboteur agents\n"
        #                           .format(params.world_graph.num_vertices - 1)).split(',')
        #
        # init_agents(greedy_search_pos, params.AGENT_TYPE_GREEDY_SEARCH)
        #
        # simulate_2()
        clique = get_shortest_path_clique(0, [1, 3], [2])
        clique.print_graph_vertices()
        print(get_mst_sum(clique))
    else:
        print("Error: inserted non existing task number: {}".format(int(task)))


def simulate():
    print("------------------ Simulation Started ------------------\n")
    if params.debug:
        print_agent_list()
        print_world_state()

    while params.should_simulate:
        for agent in params.agents_list:
            agent.act()
            print_world_state()
        # Check if simulation should cont
        params.should_simulate = False
        for agent in params.agents_list:
            # If there is an agent still active - simulation should cont
            if agent.get_active_status():
                if params.debug:
                    agent.print_name()
                params.should_simulate = True
                break

    print("------------------ Simulation Ended ------------------\n")


def simulate_2():
    print("------------------ Simulation Started ------------------\n")
    agent = params.agents_list.pop(0)
    while params.should_simulate:
        sol = agent.act()
        if (sol is not None) and (not params.should_simulate):
            print("Solution Found :", sol)
            print("\n")
        elif not params.should_simulate:
            print("No Solution was Found :(\n")
    print("------------------ Simulation Ended ------------------\n")


if __name__ == '__main__':
    arg_parser = ArgumentParser(
        prog="startup.py",
        formatter_class=RawTextHelpFormatter,
        description="Simulates agents for the hurricane evacuation problem",
    )
    arg_parser.add_argument('-i', "--input_env", default="input.txt", help='Enter input environment')
    arg_parser.add_argument('-d', "--debug", action='store_true', help='Add this flag if you wish to be in debug mode')

    command_line_args = arg_parser.parse_args()

    startup(input_graphs + "/" + command_line_args.input_env, command_line_args.debug)
