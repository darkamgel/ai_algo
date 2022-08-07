class Queue:

    def __init__(self):
        self.stack = []
    
    def push_stack(self, node):
        self.stack.append(node)

    def pop_stack(self):
        if len(self.stack) ==0:
            self.stack.pop(0)
        else:
            print("Error")


# No of missionaries
M = 3

# No of cannibals
C = 3

# Position of canoe
P = 0

ini_state = [M,C,P]