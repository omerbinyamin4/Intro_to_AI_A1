
from components import *
from graph import *
from agents import *
import params
from argparse import ArgumentParser, RawTextHelpFormatter

input_graphs = "./input_graphs"

def print_agent_list():
    print("## Agents list: ##")
    for agent in params.agents_list:
        print(agent.get_name())
    print("## Finished agent list ##")

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
            if params.debug:
                new_v.print_vertex()
            if new_v is not None:
                params.world_graph.add_vertex(new_v)
        if '#E' in line[0] and len(line) == 4:
            line_to_edge(line)
    if params.debug:
        print("vert_dict.keys after init: {}\n".format(params.world_graph.get_vertices_keys()))
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
        if agent_type == "human":
            params.agents_list.append(Human(int(pos)))
        elif agent_type == "stupid_greedy":
            params.agents_list.append(Stupid(int(pos)))
        elif agent_type == "saboteur":
            params.agents_list.append(Saboteur(int(pos)))
        else:
            print("error: agent type {} not supported".format(agent_type))

def startup(input_env, debug_mode):
    params.debug = debug_mode
    init_graph_from_file(input_env)
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

    #TODO : can an agent start in a brittle vertex?
    init_agents(human_pos, "human")
    init_agents(stupid_greedy_pos, "stupid_greedy")
    init_agents(saboteur_pos, "saboteur")

    simulate()

def simulate():
    print("------------------ Simulation Started ------------------\n")
    if params.debug:
        print_agent_list()

    while params.should_simulate:
        for agent in params.agents_list:
            agent.act()
            print_world_state()
        # Check if simulation should cont
        params.should_simulate = False
        for agent in params.agents_list:
            # If there is an agent still active - simulation should cont
            if agent.get_active_status():
                params.should_simulate = True
                break
        # TODO: improve cond to check if there are anymore people to be saved.
        # TODO: Active property is imporant to check if a agent should keep running, but maybe not good for termination because of sabteur
        # TODO: Add 'blocked' property to Vertex and support property in code
        # TODO: calculation of score is incorrect at the moment - should be fixed.
        # TODO: adjust each move to work according to time units (as opposed to 1 time unit)
        # TODO: change agent to return a response (new class?) instead of changing the world by itself
        # TODO: state should be - where is each agent, which vertices has people, which vertices are brittle, which vertices are blocked
        # I think we should start by letting each agent run alone, and advance from there according to answers on ambiguities..
        # Ambiguities:
        # When a time step occurs? after all agents steped or after each agent stepped? 
        # Check if sabteur makes brittle non brittle or non blocked?
        # Should stupid greedy consider the fact a saboteur can break/broke a brittle vertix in its path?
        # if there are 2 greedy agents - should they check where the other agent is headed and go to a different place?

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
