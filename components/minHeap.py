from heapq import heappush, heappop, heapify


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

    # Method to remove minium element from min heap- return heap element with key and value
    def extract_min(self):
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
