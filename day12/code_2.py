import copy
import math

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


# just a way to save some special rules we know are important
prev_special_rules = []
prev_special_rules.append(rules[(False, False, False, True, False)])
prev_special_rules.append(rules[(False, False, False, False, True)])
prev_special_rules.append(rules[(False, False, False, True, True)])
after_special_rules = []
after_special_rules.append(rules[(True, False, False, False, False)])
after_special_rules.append(rules[(False, True, False, False, False)])
after_special_rules.append(rules[(True, True, False, False, False)])


def get_gen_score(state):
    result = 0
    cur_node = state.start_node
    while cur_node is not None:
        if cur_node.val:
            result += cur_node.name
        cur_node = cur_node.next_node
    
    return result


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
    

scores = [get_gen_score(cur_state)]
deltas = []

for i in range(1001):
    prev_score = scores[-1]
    cur_state = get_next_generation(cur_state)
    scores.append(get_gen_score(cur_state))
    deltas.append(scores[-1] - prev_score)

def find_cycles(data):
    seen = {}
    for idx, d in enumerate(data):
        if d not in seen:
            seen[d] = [idx]
            continue
        found = False
        for prev_idx in seen[d]:
            two_cycles = idx - prev_idx
            found = True
            for offset in range(two_cycles + 1):
                if d == 98:
                    print('data[{}]({}) vs data[{}]({})'.format(prev_idx + offset, data[prev_idx + offset], idx + offset, data[idx + offset]))
                if idx + offset >= len(data):
                    found = False
                    break
                if data[prev_idx + offset] != data[idx + offset]:
                    found = False
                    break
            if found:
                return (prev_idx, idx)
        seen[d].append(idx)
    return None

def calculate_large_value(scores, deltas, gen):
    cycle = find_cycles(deltas)
    print('Delta cycle: {}'.format(cycle))
    print('Delta vals: {}'.format(deltas[cycle[0]: cycle[1] + 1]))
    print('Cycle length: {}'.format(len(deltas[cycle[0]: cycle[1]])))
    print('Blah: {}'.format(scores[cycle[0] - 1: cycle[1] + 1]))

    cycle_len = cycle[1] - cycle[0]
    cycle_delta = sum(deltas[cycle[0]: cycle[1]])

    partial_cycle = (gen - cycle[0]) % cycle_len
    cycle_count = math.floor((gen - cycle[0]) / cycle_len)

    initial_score = scores[cycle[0]]
    initial_score += (cycle_count * cycle_delta)
    initial_score += sum(deltas[cycle[0]: cycle[0] + partial_cycle])

    print('initial_score: {}, total_cycle: {}, partial_cycle val: {}, partial_cycle: {}'.format(
        scores[cycle[0]],
        (cycle_count * cycle_delta),
        sum(deltas[cycle[0]: cycle[0] + partial_cycle]),
        deltas[cycle[0]: cycle[0] + partial_cycle]
    ))
    print('cycle_count: {}, partial_cycle: {}, cycle_delta: {}, cycle_len: {}'.format(cycle_count, partial_cycle, cycle_delta, cycle_len))
    print('Final result: {}'.format(initial_score))

calculate_large_value(scores, deltas, 50000000000)