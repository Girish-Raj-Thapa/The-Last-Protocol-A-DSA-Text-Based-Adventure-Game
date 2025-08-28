class Node:
    def __init__(self, value):
        self.value = value 
        self.next = None

class LinkedList:
    def __init__(self, head=None):
        self.head = head 
        self.next = None
    
    def append(self, value):
        new_node = Node(value)

        if not self.head: # for empty list
            self.head = new_node
            return 
        
        current = self.head
        while current.next: # for finding the end of the list
            current = current.next 

        current.next = new_node # adding the new_node to the end of the list

    
    def display(self):
        """ 
        Display all nodes of the list from start to fininsh 
        """
        
        current = self.head 
        count = 1
        while current:
            print(f"{count}. {current.value}")
            current = current.next 
            count += 1

class Stack:
    """
    Stack is used for undo functionality.
    """        

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def is_empty(self):
        return len(self.items) == 0
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None 
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None 
    
class Queue:
    """
    For managing NPC Actions.
    A Deque (double-ended queue) is used to avoid the performance cost of inserting at the start of a list.
    """
    
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.insert(0, item)

    def is_empty(self):
        return len(self.items) == 0

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop()
        return None 
    
class PriorityQueue:
    """
    A priority queue for urgent drone threats. Lower number = higher priority.
    This implementation uses a simple list and manual searching.
    """

    def __init__(self):
        self._items = []
        self.max_size = 5  # Added limit to prevent flooding

    def enqueue(self, value, priority):
        """
        Adds an item with priority to the queue, if not exceeding max size.
        """
        if len(self._items) >= self.max_size:
            print("Drone queue is full; cannot add more threats.")
            return
        self._items.append((priority, value))

    def is_empty(self):
        return len(self._items) == 0

    def dequeue(self):
        """
        Removes and returns the highest priority item.
        """
        if self.is_empty():
            return None
        
        highest_priority_index = 0

        for i in range(1, len(self._items)):
            if self._items[i][0] < self._items[highest_priority_index][0]:
                highest_priority_index = i

        return self._items.pop(highest_priority_index)[1]
    
    def peek(self):
        """
        Returns the highest priority item without removing it
        """
        if self.is_empty():
            return None 
        
        highest_priority_index = 0
        for i in range(1, len(self._items)):
            if self._items[i][0] < self._items[highest_priority_index][0]:
                highest_priority_index = i
        
        return self._items[highest_priority_index][1]