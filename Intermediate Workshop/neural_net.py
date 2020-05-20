import networkx as nx
from numpy import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

"""
Object representing a node on the network.
"""
class Node(object):

    def __init__(self, id, neighbour_ids):

        self.id = id
        self.edges = {}
        self.neighbours = {} # Mapping from ID to Actual Object

        # function to create edge dictionary of Neighbour_ID: Probability
        self.initialise_edges(neighbour_ids)


    """
    Setup edges dictionary as mapping of {neighbour_id: probability}.
    All probabilities will start equal.
    """
    def initialise_edges(self, neighbour_ids):

        # avoid division by 0
        if len(neighbour_ids) == 0:
            return

        initial_probability = 1.0 / len(neighbour_ids)
        for id in neighbour_ids:
            self.edges[id] = initial_probability

    """
    Create dictionary of {neighbour_id: neighbour object}, for graph traversal.
    """
    def initialise_neighbours(self, node_dict):

        for node_id, node in node_dict.items():

            for neighbour_id in self.edges:

                if node_id == neighbour_id:
                    self.neighbours[neighbour_id] = node

        # print(self.neighbours)

    """
    Creates a convenient dictionary with probability ranges for each edge, so that
    a generated random number can be checked in each range.
    """
    def create_choice_dict(self):
        choice_dict = {}
        choice_cutoff = 0
        for id in self.edges:
            # define range for this choice (i.e. 0.0 <-> 0.5) as (0, 0.5)
            transition_probability = self.edges[id]
            range = choice_cutoff, choice_cutoff + transition_probability
            choice_dict[id] = range
            choice_cutoff += transition_probability

        return choice_dict

    """
    Generates a random float between 0 and 1, and uses the choice dictionary created
    to decide which edge to go to.
    """
    def make_choice(self):
        random_num = random.rand()
        print(random_num)
        choice_dict = self.create_choice_dict()
        print(choice_dict)
        # decide which node to go to
        for id in choice_dict:
            # range is e.g. (0, 0.5)
            range = choice_dict[id]
            lower_bound = range[0]
            upper_bound = range[1]

            if lower_bound < random_num <= upper_bound:
                return id

        # if an error occurs
        return None

    """
    Recursive function that travels between nodes and tracks the path
    taken. Path ends if you reach the goal node or a node with no neighbours,
    or if you run out of moves from the limited path length.
    """
    def transition_to_neighbour(self, limit, goal_node_id):

        # going to be a list of (current_node, next_node)
        path = []

        # Base case
        if limit < 1:
            # end if no more transitions left
            return path
        elif len(self.neighbours) == 0:
            # end if there is nowhere to go to
            return path
        elif self.id == goal_node_id:
            # end if we reach goal
            return path

        # make choice and add to path
        next_node_id = self.make_choice()
        path.append((self.id, next_node_id))
        next_node = self.neighbours[next_node_id]
        print("Next node: {}".format(next_node_id))

        # recursive step, add the transitions of all subsequent neighbours
        path.extend(next_node.transition_to_neighbour(limit - 1, goal_node_id))

        return path

    """
    Returns the connected neighbours from the neighbour dictionary, in a format
    that works with networkx (node: neighbour).
    """
    def get_edges(self):
        edge_list = []
        for neighbour in self.edges.keys():
            edge_list.append((self.id, neighbour))
        return edge_list

    def get_id(self):
        return self.id

    """
    Positively or negatively reinforces the chosen edge on the path,
    as to help the model learn.
    """
    def update_probabilities(self, node_id, change):

        # node_id is the node that we travelled to on the path

        # if no more than 1 edge, do nothing
        if len(self.edges) < 2:
            return

        # change for each other node
        proportional_change = change / (len(self.edges) - 1)

        print("Node {} Before probability change: {}".format(self.id, self.edges))
        for key in self.edges:
            # update probability
            if key == node_id:
                # increase/decrease probability for given edge
                self.edges[key] += change
            else:
                # complementary proportional change for each other node
                self.edges[key] -= proportional_change

            # Ensure probabilities remain between desired values.
            if self.edges[key] < 0:
                self.edges[key] = 0
            elif self.edges[key] > 1:
                self.edges[key] = 1

        print("Node {} After probability change: {}".format(self.id, self.edges))

    def __str__(self):
        return "Node ID: {}, Connections: {}".format(self.id, self.edges)

"""
Class representing the entire Network, with many nodes within.
"""
class Network(object):

    def __init__(self, graph, training_tests, path_length, reinforcement):
        self.graph = graph  # networkx graph object
        self.nodes = {}  # mapping of all Node Ids: Node Objects
        self.goal_node_id = 0  # the node we want to reach

        # Parameters for training tests:
        self.training_tests = training_tests
        self.path_length = path_length
        self.reinforcement = reinforcement

        # figure and axis for animation ONLY
        self.figure, self.axis = plt.subplots(figsize=(6, 4))

    """
    Creates new node object from input and adds it to the network.
    Handles addition of node to networkx display graph as well.
    """
    def add_node_to_network(self, node_id, neighbour_ids: list):

        node = Node(node_id, neighbour_ids)
        self.nodes[node_id] = node

        # add nodes and edges to graph (Networkx stuff)
        self.graph.add_node(node_id)
        self.graph.add_edges_from(node.get_edges())

    """
    Ensures all nodes have initialised their neighbour node objects, so they can
    talk to eachother.
    """
    def initialise_all_node_neighbours(self):

        for node in self.nodes.values():
            node.initialise_neighbours(self.nodes)

    """
    Given a path taken through the network, will either reduce or increase all
    edge probabilities on that path, depending on whether it reached the goal.
    """
    def update_node_probabilities(self, path):

        reinforcement = self.reinforcement

        # Check if goal reached (for positive reinforcement)
        if self.goal_node_id in self.get_visited_nodes(path):
            print("Positive reinforcement!")
        else:
            print("Negative reinforcement!")
            reinforcement = -reinforcement

        # Transition is (node_id, neighbour_id)
        for transition in path:

            node_id = transition[0]
            neighbour_id = transition[1]
            node = self.nodes[node_id]

            node.update_probabilities(neighbour_id, reinforcement)

    """
    Returns the node ids of all nodes on the given path.
    """
    def get_visited_nodes(self, path):

        visited_node_ids = []
        # get node ids from path [()()()]
        for edge in path:
            for id in edge:
                visited_node_ids.append(id)

        # just eliminated repeating entries with a quick trick!
        visited_node_ids = list(dict.fromkeys(visited_node_ids))

        return visited_node_ids

    """
    Draws networkx graph display. Don't worry too much about this...
    But feel free to copy the code if you want to display your model.
    """
    def draw_graph(self, path):

        # Layout
        pos = nx.spring_layout(self.graph)

        # Draw nodes
        nx.draw_networkx_nodes(self.graph,
                               pos,
                               nodelist=list(self.nodes.keys()),
                               node_color='b')

        # Draw goal node in green
        nx.draw_networkx_nodes(self.graph,
                               pos,
                               nodelist=[self.goal_node_id],
                               node_color='g')

        # Nodes on path are red if goal not reached, green if it is reached.
        path_colour = 'r'
        if self.goal_node_id in self.get_visited_nodes(path):
            path_colour = 'g'

        nx.draw_networkx_nodes(self.graph,
                               pos,
                               nodelist=self.get_visited_nodes(path),
                               node_color=path_colour)


        # Draw edges
        nx.draw_networkx_edges(self.graph, pos, width=1.0, alpha=0.5)

        # Edges of path are red if goal not reached, green if it is reached.
        nx.draw_networkx_edges(self.graph, pos,
                               edgelist=path,
                               width=8, alpha=0.5, edge_color=path_colour)

        nx.draw_networkx_labels(self.graph, pos)
        plt.show()

    """
    Simpler way to run training tests. Works in PyCharm, but not in Spyder...
    """
    def run_all_training_tests_with_plots(self):

        i = 0
        while i < self.training_tests:

            # start transition
            starting_node = self.nodes[0]
            path = starting_node.transition_to_neighbour(limit=self.path_length,
                                                         goal_node_id=self.goal_node_id)
            print("Path: {}".format(path))

            self.draw_graph(path)

            self.update_node_probabilities(path)

            i += 1

    """
    Function for animated version of the plot (need to run in Spyder).
    """
    def run_training_test_frame(self, frame):
        self.axis.clear()
        # start transition
        starting_node = network.nodes[0]
        path = starting_node.transition_to_neighbour(limit=self.path_length,
                                                     goal_node_id=network.goal_node_id)
        print("Path: {}".format(path))

        network.draw_graph(path)

        network.update_node_probabilities(path)

        self.axis.set_title("Training test: {}".format(frame + 1))
        self.axis.set_xticks([])
        self.axis.set_yticks([])

    """
    Run animation for all training tests. (Only runs well in Spyder).
    """
    def run_animation(self, speed):

        animated_graph = animation.FuncAnimation(self.figure,
                                                 self.run_training_test_frame,
                                                 frames=self.training_tests,
                                                 interval=speed,
                                                 repeat=False
                                                 )
        plt.show()

    def construct_graph_example_1(self, goal_node):

        self.goal_node_id = goal_node
        self.add_node_to_network(0, [1, 3])
        self.add_node_to_network(1, [2])
        self.add_node_to_network(2, [3, 4])
        self.add_node_to_network(3, [2, 5])
        self.add_node_to_network(4, [0])
        self.add_node_to_network(5, [])

    def construct_graph_example_2(self, num_nodes, goal_node):

        self.goal_node_id = goal_node

        i = 0
        skip = False
        while i < num_nodes:
            neighbours = [i + 1, i + 2]

            for n_id in neighbours:
                if n_id > num_nodes - 1:
                    skip = True

            if skip:
                self.add_node_to_network(i, [])
            else:
                self.add_node_to_network(i, neighbours)

            i += 1


if __name__ == "__main__":

    # create network object
    network = Network(graph=nx.MultiDiGraph(),
                      training_tests=100,
                      path_length=7,
                      reinforcement=0.1
                      )

    # Example graph constructors:
    # recommended settings: 10, 5, 0.1
    #network.construct_graph_example_1(goal_node=4)
    
    # recommended settings: 100, 10, 0.1
    network.construct_graph_example_2(num_nodes=20, goal_node=12)

    # initialise Neighbour_ID: Neighbour Object dictionary for all nodes
    network.initialise_all_node_neighbours()

    # Learning Loop - Many Plots Version (For Pycharm)
    # network.run_all_training_tests_with_plots()

    # Animation of Learning Loop - (Use in Spyder only)
    network.run_animation(speed=300)


