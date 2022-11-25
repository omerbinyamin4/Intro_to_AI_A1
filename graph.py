# import params


class Vertex:
    def __init__(self, node, population, is_brittle):
        self.id = node
        self.adjacent = {}
        self.population = population
        self.is_brittle = is_brittle
        self.is_broken = False
        self.solution_parent = None

    def copy_vertex(self, vertex, optional_exclude_id_list):
        self.id = vertex.get_id()
        self.population = vertex.get_population()
        self.is_brittle = vertex.check_is_brittle()
        self.is_broken = vertex.is_broken
        for key in vertex.adjacent.keys():
            if key not in optional_exclude_id_list:
                self.adjacent[key] = vertex.adjacent[key]

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor_id):
        if neighbor_id in self.adjacent.keys():
            return self.adjacent[neighbor_id]
        return None

    def get_population(self):
        return self.population

    def has_population(self):
        return self.population > 0

    def reset_population(self):
        # params.total_victims = params.total_victims - self.population
        self.population = 0

    def check_is_brittle(self):
        return self.is_brittle

    def break_ver(self):
        self.is_broken = True

    def check_if_broken(self):
        return self.is_broken

    def brittle_not_broken(self):
        return (self.is_brittle) and (not self.is_broken)

    def print_vertex(self):
        print("Vertex {}:".format(str(self.id)))
        print("\tadjacent: {}".format(self.adjacent))
        print("\tpopulation: " + str(self.population))
        print("\tbrittle: " + str(self.is_brittle))
        if self.is_brittle:
            print("\tbroken: " + str(self.is_broken))


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def copy_graph(self, g, optional_exclude_id_list):
        self.num_vertices = g.num_vertices
        for key in g.get_vertices_keys():
            new_vertex = Vertex(0, 0, False)  # garbage values that will be overridden in copy_vertex
            new_vertex.copy_vertex(g.get_vertex(key), optional_exclude_id_list)
            self.vert_dict[key] = new_vertex

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, new_vertex):
        self.num_vertices = self.num_vertices + 1
        self.vert_dict[new_vertex.id] = new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=0):
        if frm.id not in self.vert_dict.keys():
            self.add_vertex(frm)
        if to.id not in self.vert_dict.keys():
            self.add_vertex(to)

        self.get_vertex(frm.id).add_neighbor(to.id, cost)
        self.get_vertex(to.id).add_neighbor(frm.id, cost)

    def get_vertices_keys(self):
        return self.vert_dict.keys()

    def get_vertices_values(self):
        return self.vert_dict.values()

    def print_graph_vertices(self):
        print("## Graph vertices: ##\n---------------------------\n")
        for vertex in self.get_vertices_values():
            vertex.print_vertex()
        print("---------------------------\n## end of graph vertices ##")
