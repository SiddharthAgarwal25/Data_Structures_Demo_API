class Node:
    def __init__(self, data, next_node):
        self.data = data
        self.next_node = next_node

class Queue:
    def __init__(self):
        self.head = None # first node
        self.tail = None # last node

    def first_in(self, data):
        if self.head == None and self.tail==None:
            self.head = self.tail = Node(data, None)
            return
        new_node = Node(data, None)
        self.tail.next_node = new_node
        self.tail = self.tail.next_node
        return 
    
    def first_out(self):
        if self.head is None:
            print("Queue is empty")
        
        removed = self.head
        self.head = self.head.next_node
        if self.head is None:
            self.tail = None
        return removed
    

