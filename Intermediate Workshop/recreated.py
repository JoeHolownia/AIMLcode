"""
THIS IS WHAT WE RECREATED DURING THE 2HR INTERMEDIATE SESSION.
"""
import networkx as nx
from numpy import random

"""
Represents a node on the network.
"""
class Node(object):

    """
    Constructor.
    """
    def __init__(self, node_id, neighbour_ids):

        self.node_id = node_id

        self.edges = {} # Mapping {neighbour_id: probabilities}
        self.neighbours = {} # Mapping {neighbour_id: Actual Neighbour Object}

        self.initialise_edges(neighbour_ids)

    def initialise_edges(self, neighbour_ids):

        # check
        if len(neighbour_ids) == 0:
            return

        initial_probability = 1 / len(neighbour_ids)

        # Update edges dictionary
        for id in neighbour_ids:
            self.edges[id] = initial_probability

    def get_edges(self):

        edge_list = []

        for neighbour_id in self.edges:
            # remember: {key:value}
            item = (self.node_id, neighbour_id)
            edge_list.append(item)

        return edge_list

    def initialise_neighbours(self, node_dict):

        for node_id, node in node_dict.items():

            for neighbour_id in self.edges: # {neighbour_id: probability}

                if node_id == neighbour_id:
                    self.neighbours[node_id] = node

        # print("Node id {} with neighbours {} ".format(self.node_id, self.neighbours))

    def create_choice_dict(self):

        choice_dict = {}
        choice_cutoff = 0

        for id, transition_probability in self.edges.items():
            # From our original probabilities: {1: 0.3, 2: 0.3, 3: 0.3}
            # define range for this choice (i.e. 0.0 <-> 0.5) as (0, 0.5)
            range = (choice_cutoff, choice_cutoff + transition_probability)

            choice_dict[id] = range
            choice_cutoff += transition_probability

        return choice_dict

    def make_choice(self):

        # generate a random number
        random_num = random.rand() # float between 0-1
        print(random_num)

        choice_dict = self.create_choice_dict()
        print(choice_dict)

        # decide which node to go to
        for node_id, range in choice_dict.items():
            # (0, 0.5), (0.5, 1)
            lower_bound = range[0]
            upper_bound = range[1]

            if lower_bound < random_num <= upper_bound:
                return node_id # choice of neighbour to go to

        # if an error occurs
        return None

    def transition_to_neighbour(self, limit, goal_node_id):

        path = []

        # Base cases
        if limit < 1:
            return path
        elif self.node_id == goal_node_id:
            return path
        elif len(self.neighbours) == 0:
            return path

        # make choice
        next_node_id = self.make_choice()
        path.append((self.node_id, next_node_id))

        next_node = self.neighbours[next_node_id] # actual node object
        print("Next node: {}".format(next_node_id))

        # recursive step
        path.extend(next_node.transition_to_neighbour(limit - 1, goal_node_id))

        return path

    def __str__(self):
        return "Node with id {} and edges {}".format(self.node_id, self.edges)

"""
Represent the entire network, containing all nodes.
"""
class Network(object):

    """
    Constructor.
    """
    def __init__(self, graph, training_tests, path_length, reinforcement):

        self.nodes = {} # {Map all node_ids:Node objects}
        self.goal_node_id = 0 # default 0

        self.graph = graph
        self.training_tests = training_tests
        self.path_length = path_length
        self.reinforcement = reinforcement

    def add_node_to_network(self, node_id, neighbour_ids):

        node = Node(node_id, neighbour_ids)
        self.nodes[node_id] = node # Mapping node_id: node_object

        # Networkx stuff:
        self.graph.add_node(node_id)
        self.graph.add_edges_from(node.get_edges()) # Because networkx [(node_id, neighbour_id), ...]


    def initialise_all_node_neighbours(self):

        for node in self.nodes.values(): # returning the values of the dictionary, values = objects
            node.initialise_neighbours(self.nodes)

    def construct_graph_example_1(self, goal_node):

        self.goal_node_id = goal_node

        self.add_node_to_network(0, [1, 3])
        self.add_node_to_network(1, [2])
        self.add_node_to_network(2, [3, 4])
        self.add_node_to_network(3, [2, 5])
        self.add_node_to_network(4, [0])
        self.add_node_to_network(5, [])

if __name__ == "__main__":

    # Program starts here: initialise network object
    network = Network(graph=nx.MultiDiGraph(),
                      training_tests=10,
                      path_length=5,
                      reinforcement=0.1
                      )

    # construct example graph
    network.construct_graph_example_1(goal_node=5)

    # initialise all node objects
    network.initialise_all_node_neighbours()

    # test path traversal
    # start transition
    starting_node = network.nodes[0]
    path = starting_node.transition_to_neighbour(limit=network.path_length, goal_node_id=network.goal_node_id)
    print("Path: {}".format(path))

