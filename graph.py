# import params


class Vertex:
    def __init__(self, node, population, is_brittle):
        self.id = node
        self.adjacent = {}
        self.population = population
        self.is_brittle = is_brittle
        self.is_broken = False
        self.solution_parent = None

    # def __str__(self):
    #     return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

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
        print("## Vertex properties: ##")
        print("id: " + str(self.id))
        print("adjacent:")
        print(self.adjacent)
        print("population: " + str(self.population))
        print("brittle: " + str(self.is_brittle))
        if self.is_brittle:
            print("broken: " + str(self.is_broken))
        print("## Finished vertex ##\n")


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

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
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices_keys(self):
        return self.vert_dict.keys()

    def get_vertices_values(self):
        return self.vert_dict.values()
