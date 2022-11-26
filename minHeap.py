from heapq import heappush, heappop, heapify
from graph import *
from params import *


# heappop - pop and return the smallest element from heap
# heappush - push the value item onto the heap, maintaining
#             heap invariant
# heapify - transform list into heap, in place, in linear time

# A class for Min Heap
class MinHeap:

    # Constructor to initialize a heap
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) / 2

    # Inserts a new element with key 'k' and value 'v'
    def insert_element(self, e):
        heappush(self.heap, (e.key, e.value))

        # Decrease value of key at index 'i' to new_val

    # It is assumed that new_val is smaller than heap[i]
    # def decrease_key(self, i, new_val):
    #     self.heap[i] = new_val
    #     while (i != 0 and self.heap[self.parent(i)] > self.heap[i]):
    #         # Swap heap[i] with heap[parent(i)]
    #         self.heap[i], self.heap[self.parent(i)] = (
    #             self.heap[self.parent(i)], self.heap[i])

    # Method to remove minimum element from min heap- return heap element with key and value
    def extract_min(self):
        if len(self.heap) == 0:
            return None
        (popped_key, popped_value) = heappop(self.heap)
        return HeapElement(popped_key, popped_value)

    # # This function deletes key at index i. It first reduces
    # # value to minus infinite and then calls extractMin()
    # def delete_key(self, i):
    #     self.decrease_key(i, float("-inf"))
    #     self.extractMin()

    # Get the minimum element from the heap
    def get_min(self):
        (min_key, min_value) = self.heap[0]
        return HeapElement(min_key, min_value)

    def contains(self, e):
        return e in self.heap

    def is_empty(self):
        return len(self.heap) == 0


class HeapElement:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class Search_tree_node:
    def __init__(self, id, parent, broken_list, population_list, g, h):
        self.id = id
        self.parent = parent #todo figure out how to add parent
        self.broken_nodes = broken_list
        self.nodes_with_population = population_list
        self.g = g # Cost so far to reach current node
        self.h = h # Estimated cost to goal from current node

    def print_search_tree_node(self):
        print("search_tree_node: " + str(self.id))
        print("\tparent: " + str(self.parent))
        print("\tbroken nodes: {}".format(self.broken_nodes))
        print("\tnodes_with_population: {}".format(self.nodes_with_population))
        print("\tg: " + str(self.g))
        print("\th: " + str(self.h))