class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

class LinkedList:
    def __init__(self) -> None:
        self.head = None
    def to_array(self):
        arr = []
        if self.head is None:
            return arr
        node = self.head
        while node:
            arr.append(node.data)
            node = node.next_node
        return arr
    
    def print_ll(self):
        ll_string = ""
        node = self.head
        if node is None:
            print("Linked List is empty")
        else:
            while node:
                ll_string += f" {str(node.data)} ->"
                if node.next_node is None:
                    ll_string += " None"
                node = node.next_node 
            print(ll_string)
    def insert_at_beg(self, data):
        node = Node(data, self.head)
        self.head = node
        
    def insert_at_end(self, data):
        node = Node(data, None)
        if self.head is None:
            self.insert_at_beg(data)
            print("List is empty, hence inserting at the beginnig")
            return
        last_node = self.head
        while last_node.next_node is not None:
            last_node = last_node.next_node
        last_node.next_node = node
    
    def get_one(self, user_id):
        node = self.head
        while node:
            if node.data["id"] is int(user_id):
                return node.data
            node = node.next_node
        return None
# ll = LinkedList()

# node3 = Node("data3", None)
# node2 = Node("data2",node3)
# node1 = Node("data", node2)

# ll.head = node1

# ll.insert_at_beg("data4")
# ll.print_ll()
# ll.insert_at_end("data5")

# ll.print_ll()