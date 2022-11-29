from agents import *
from utils import *
import params
from argparse import ArgumentParser, RawTextHelpFormatter

input_graphs = "./input_graphs"


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
            params.agents_list.append(Greedy_search(int(pos), get_mst_sum))
        elif agent_type == params.AGENT_TYPE_A_STAR_SEARCH:
            params.agents_list.append(A_star_search(int(pos), get_mst_sum))
        elif agent_type == params.AGENT_TYPE_REALTIME_A_STAR_SEARCH:
            params.agents_list.append(realtime_A_star_search(int(pos), get_mst_sum))
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
        single_or_multi = input("choose mode:\n"
                                "(1) single agent\n"
                                "(2) multi agent\n")
        if int(single_or_multi) == 1:
            single_agent_type = input("choose agent type:\n"
                                      "(1) Greedy Search Agent\n"
                                      "(2) A* Search Agent\n"
                                      "(3) Real Time Search Agent\n").split(',')
            pos = input("enter start position for the agent:\n").split(',')
            if single_agent_type[0] == '3':
                prompt_user_l()
            init_agents(pos, int(single_agent_type[0]) + 2)

        elif int(single_or_multi) == 2:
            greedy_search_pos = input("enter start position for single greedy search agent\n"
                                      "possible positions are 0-{}\n"
                                      "enter -1 for no greedy search agents\n"
                                      .format(params.world_graph.num_vertices - 1)).split(',')
            a_star_search_pos = input("enter start position for single a_star search agent\n"
                                      "possible positions are 0-{}\n"
                                      "enter -1 for no a_star search agents\n"
                                      .format(params.world_graph.num_vertices - 1)).split(',')
            realtime_a_star_search_pos = input("enter start position for single realtime a_star search agent\n"
                                               "possible positions are 0-{}\n"
                                               "enter -1 for no realtime a_star search agents\n"
                                               .format(params.world_graph.num_vertices - 1)).split(',')
            if realtime_a_star_search_pos[0] != '-1':
                prompt_user_l()
            init_agents(greedy_search_pos, params.AGENT_TYPE_GREEDY_SEARCH)
            init_agents(a_star_search_pos, params.AGENT_TYPE_A_STAR_SEARCH)
            init_agents(realtime_a_star_search_pos, params.AGENT_TYPE_REALTIME_A_STAR_SEARCH)

        prompt_user_t()

        simulate_2()
    else:
        print("Error: inserted non existing task number: {}".format(int(task)))


def simulate():
    print("------------------ Simulation Started ------------------\n")
    if params.debug:
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
    if params.debug:
        print_world_state()
    results = []

    # run all agents at turns
    for agent in params.agents_list:
        results.append(agent.act())

    # print all results
    for res in results:
        if res.success:
            print("## Solution found by Agent '{}': ##\n---------------------------\n".format(res.agent_name))
            res.print_result()
            print("\n---------------------------\n## end of solution ##\n")
        else:
            print("No Solution was Found :(\n")
    print("------------------ Simulation Ended ------------------\n")


def prompt_user_l():
    should_use_def_l = input("Do you want to define new limit of expansions for the realtime A* agent?\n"
                             "(1) - Yes\n"
                             "(0) - No\n")
    if int(should_use_def_l) == 1:
        user_l = input("insert limit of expansion for the realtime A* agent\n")
        params.user_L = int(user_l[0])


def prompt_user_t():
    should_use_def_l = input("Do you want to define new T value for performance measurement?\n"
                             "(1) - Yes\n"
                             "(0) - No\n")
    if int(should_use_def_l) == 1:
        user_t = input("insert T value for performance measurement\n")
        params.T = int(user_t[0])


if __name__ == '__main__':
    arg_parser = ArgumentParser(
        prog="startup.py",
        formatter_class=RawTextHelpFormatter,
        description="Simulates agents for the hurricane evacuation problem",
    )
    arg_parser.add_argument('-i', "--input_env", default="simple_env2.txt", help='Enter input environment')
    arg_parser.add_argument('-d', "--debug", action='store_true', help='Add this flag if you wish to be in debug mode')

    command_line_args = arg_parser.parse_args()

    startup(input_graphs + "/" + command_line_args.input_env, command_line_args.debug)
