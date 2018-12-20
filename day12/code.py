import copy

class Node:
    def __init__(self, val, name, prev_node=None, next_node=None):
        self.next_node = next_node
        self.prev_node = prev_node
        self.val = val
        self.name = name

class LinkedList:
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length = 0
    
    def add_node(self, val, name, loc=None):
        if loc is None:
            loc = self.length
        node = Node(val, name)
        if self.length == 0:
            self.start_node = node
            self.end_node = node
        elif loc < 0:
            node.next_node = self.start_node
            self.start_node.prev_node = node
            self.start_node = node
        elif loc >= self.length:
            self.end_node.next_node = node
            node.prev_node = self.end_node
            self.end_node = node
        else:
            cur_node = self.start_node
            while loc != 0:
                loc -= 1
                cur_node = cur_node.next_node
            
            cur_node.next_node.prev_node = node
            cur_node.next_node = node
        self.length += 1
            
    def remove_node(self, loc):
        if loc < 0 or loc >= self.length:
            raise Exception('No sir! {}'.format(loc))

        cur_node = self.start_node
        while loc != 0:
            loc -= 1
            cur_node = cur_node.next_node
        cur_node.prev_node.next_node = cur_node.next_node
        cur_node.next_node.prev_node = cur_node.prev_node
        self.length -= 1

rules = {}
cur_state = LinkedList()
states = []

with open('input.txt', 'r') as f:
    lines = f.read().split('\n')
    initial_state = lines[0].split(':')[1].strip()
    for i in range(len(initial_state)):
        cur_state.add_node(initial_state[i] == '#', i, cur_state.length)
    
    for i in range(2, len(lines)):
        line = lines[i].split(' => ')
        rules[(
            line[0][0] == '#',
            line[0][1] == '#',
            line[0][2] == '#',
            line[0][3] == '#',
            line[0][4] == '#',
        )] = line[1][0] == '#'

# for testing
for r in range(32):
    key = (
        bool(r & 0x01),
        bool(r & 0x02),
        bool(r & 0x04),
        bool(r & 0x08),
        bool(r & 0x10)
    )

    if key not in rules:
        rules[key] = False


states.append(cur_state)
# just a way to save some special rules we know are important
prev_special_rules = []
prev_special_rules.append(rules[(False, False, False, True, False)])
prev_special_rules.append(rules[(False, False, False, False, True)])
prev_special_rules.append(rules[(False, False, False, True, True)])
after_special_rules = []
after_special_rules.append(rules[(True, False, False, False, False)])
after_special_rules.append(rules[(False, True, False, False, False)])
after_special_rules.append(rules[(True, True, False, False, False)])

def get_next_generation(cur_state):
    cur_node = cur_state.start_node
    next_state = LinkedList()
    while cur_node is not None:
        cur = cur_node.val
        prev = False
        prev2 = False
        after = False
        after2 = False

        if cur_node.prev_node is not None:
            prev = cur_node.prev_node.val
            if cur_node.prev_node.prev_node is not None:
                prev2 = cur_node.prev_node.prev_node.val
        if cur_node.next_node is not None:
            after = cur_node.next_node.val
            if cur_node.next_node.next_node is not None:
                after2 = cur_node.next_node.next_node.val
        
        # check some special cases before finishing processing
        # if we're at the first node, 
        if cur_node == cur_state.start_node:
            n = cur_node.val
            # assumption: must be at least spaces long
            n2 = cur_node.next_node.val
            added_first = False
            added_second = False

            if n and prev_special_rules[1]:
                next_state.add_node(True, cur_node.name - 2)
                added_first = True
                
            if n and n2 and prev_special_rules[2]:
                next_state.add_node(True, cur_node.name - 1)
                added_second = True
            elif n and (not n2) and prev_special_rules[0]:
                next_state.add_node(True, cur_node.name - 1)
                added_second = True
            elif (not n) and n2 and prev_special_rules[1]:
                next_state.add_node(True, cur_node.name - 1)
                added_second = True
            
            if added_first and not added_second:
                next_state.add_node(False, cur_node.name - 1)
                next_state.add_node(True, cur_node.name + 2)
        
        cur_rule = (prev2, prev, cur, after, after2)
        rule_out = False
        if cur_rule in rules:
            rule_out = rules[cur_rule]
        next_state.add_node(rule_out, cur_node.name, next_state.length)

        if cur_node == cur_state.end_node:
            n = cur_node.val
            # assumption: must be at least spaces long
            n2 = cur_node.prev_node.val
            added_first = False

            if n and n2 and after_special_rules[2]:
                next_state.add_node(True, cur_node.name + 1)
                added_first = True
            elif n and (not n2) and after_special_rules[1]:
                next_state.add_node(True, cur_node.name + 1)
                added_first = True
            elif (not n) and n2 and after_special_rules[0]:
                next_state.add_node(True, cur_node.name + 1)
                added_first = True

            if n and after_special_rules[0]:
                if not added_first:
                    next_state.add_node(False, cur_node.name + 1)
        
        cur_node = cur_node.next_node
    
    return next_state


# do 20 generations
for i in range(50000000000):
    print(i)
    cur_state = get_next_generation(cur_state)
    states.append(cur_state)

def get_gen_score(state):
    result = 0
    cur_node = state.start_node
    while cur_node is not None:
        if cur_node.val:
            result += cur_node.name
        cur_node = cur_node.next_node
    
    return result

def print_state(state):
    names = ''
    result = ''
    cur_node = state.start_node
    while cur_node is not None:
        names += ' ' + str(cur_node.name).rjust(2, '0')
        if cur_node.val:
            result += '  #'
        else:
            result += '  .'
        cur_node = cur_node.next_node
    
    print(names)
    print(result)

print_state(cur_state)
print('Result: {}'.format(get_gen_score(cur_state)))