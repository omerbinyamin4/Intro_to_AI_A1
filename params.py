from graph import Graph

world_graph = Graph()
world_clique = Graph()
agents_list = []
should_simulate = True
debug = False
total_victims = 0

human_id = 0
stupid_id = 0
saboteur_id = 0

expansions_limit = 10000
# TODO: write prompt to get this variable from user when applying real time a* search agent
user_L = 10

AGENT_TYPE_HUMAN = 0
AGENT_TYPE_STUPID = 1
AGENT_TYPE_SABOTEUR = 2
AGENT_TYPE_GREEDY_SEARCH = 3
