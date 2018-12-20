import copy

board = []
goblins = []
elves = []
unit_id = 0

output = open('output.txt', 'w')

import builtins
def print(s):
    global output
    if output is not None:
        output.write(s + '\n')
    builtins.print(s)


class Unit:
    def __init__(self, x, y, is_elf):
        global unit_id
        self.unit_id = unit_id
        unit_id += 1
        self.x = x
        self.y = y
        self.attack = 3
        self.hp = 200
        self.is_elf = is_elf
    
    def print(self):
        print('Elf: {}, ({}, {})'.format(self.is_elf, self.x, self.y))
    
    def pos(self):
        return (self.x, self.y)

with open('input.txt', 'r') as f:
    data = f.read().split('\n')

    height = len(data)
    width = max([len(x) for x in data])

    for x in range(width):
        board.append([True for _ in range(height)])
    
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == '#':
                board[x][y] = False
            elif char == 'E':
                elves.append(Unit(x, y, True))
                board[x][y] = False
            elif char == 'G':
                goblins.append(Unit(x, y, False))
                board[x][y] = False

def adjacent_locs(board, loc):
    offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    result = []

    for o in offsets:
        if board[loc[0] + o[0]][loc[1] + o[1]]:
            result.append((loc[0] + o[0], loc[1] + o[1]))
    
    return result

def get_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# A* implementation, with priority linked list
class Node:
    def __init__(self, val, sort_val, prev_node=None, next_node=None):
        self.next_node = next_node
        self.prev_node = prev_node
        self.val = val
        self.sort_val = sort_val

class OrderedLinkedList:
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length = 0
    
    def print(self):
        node_list = []
        cur_node = self.start_node
        while cur_node is not None:
            node_list.append('({}, {}, {}, {})'.format(cur_node.val, cur_node.sort_val, cur_node.prev_node, cur_node.next_node))
            cur_node = cur_node.next_node
        print(','.join(node_list))
    
    def add_node(self, val, sort_val):
        node = Node(val, sort_val)
        if self.length == 0:
            self.start_node = node
            self.end_node = node
        else:
            cur_node = self.start_node
            while cur_node is not None:
                if sort_val < cur_node.sort_val:
                    break
                cur_node = cur_node.next_node
            
            if cur_node == self.start_node:
                node.next_node = self.start_node
                self.start_node.prev_node = node
                self.start_node = node
            elif cur_node is None:
                self.end_node.next_node = node
                node.prev_node = self.end_node
                self.end_node = node
            else:
                node.prev_node = cur_node.prev_node
                node.next_node = cur_node
                cur_node.prev_node.next_node = node
                cur_node.prev_node = node
        self.length += 1
    
    def update_node(self, val, new_sort_val):
        node = self.start_node
        node_loc = 0
        while node is not None:
            if node.val == val:
                break
            node = node.next_node
            node_loc += 1
            
        if node is None:
            return False
        
        # this is slow, but easier to implement
        # so unless i find that this becomes a bottleneck, i'm doing it this way
        test_node = self.remove_node(node_loc)
        if test_node.val != node.val:
            raise Exception('You really messed up man')
        
        self.add_node(node.val, new_sort_val)
        return True
            
    def remove_node(self, loc):
        if loc < 0 or loc >= self.length:
            return None

        cur_node = self.start_node
        while loc != 0:
            loc -= 1
            cur_node = cur_node.next_node
        if cur_node == self.start_node:
            self.start_node = cur_node.next_node
        if cur_node == self.end_node:
            self.end_node = cur_node.prev_node
        if cur_node.prev_node is not None:
            cur_node.prev_node.next_node = cur_node.next_node
        if cur_node.next_node is not None:
            cur_node.next_node.prev_node = cur_node.prev_node
        self.length -= 1
        return cur_node

def search(board, start, end):
    if start == end:
        return 0
    visited = {}
    cur_best_score = {start: 0}
    estimated_dist = {start: get_dist(start, end)}
    fringe = OrderedLinkedList()
    fringe.add_node(start, estimated_dist[start])

    while fringe.length != 0:
        cur_node = fringe.remove_node(0)
        cur_pos = cur_node.val
        cur_cost = cur_best_score[cur_pos]
        visited[cur_pos] = True
        if cur_pos == end:
            return cur_cost
        for adj in adjacent_locs(board, cur_pos):
            if adj in visited:
                continue
            if adj not in cur_best_score:
                cur_best_score[adj] = cur_cost + 1
                estimated_dist[adj] = get_dist(adj, end)
                fringe.add_node(adj, cur_best_score[adj] + estimated_dist[adj])
            elif cur_cost + 1 < cur_best_score[adj]:
                cur_best_score[adj] = cur_cost + 1
                fringe.update_node(adj, cur_best_score[adj] + estimated_dist[adj])
    
    return None

def move_unit(unit, board, enemies):
    pos = unit.pos()

    if not enemies:
        return None
    
    possible_targets = []
    for e in enemies:
        if get_dist(e.pos(), pos) == 1:
            return False
        possible_targets.extend(adjacent_locs(board, e.pos()))
    
    if not possible_targets:
        return False
    
    # sort the possible targets by distance, then y pos, then x pos
    possible_targets = sorted(possible_targets, key=lambda x: (get_dist(pos, x), x[1], x[0]))
    
    target_dist = None
    best_targets = []
    for test_target in possible_targets:
        path_cost = search(board, pos, test_target)
        if path_cost is not None:
            if target_dist is None or path_cost < target_dist:
                target_dist = path_cost
                best_targets = [test_target]
            elif path_cost == target_dist:
                best_targets.append(test_target)
    
    if not best_targets:
        return False
    
    target = sorted(best_targets, key=lambda x:(x[1], x[0]))[0]
    possible_dests = []
    for ap in adjacent_locs(board, pos):
        path_cost = search(board, ap, target)
        if path_cost is not None:
            possible_dests.append((ap, path_cost))

    if not possible_dests:
        return False
    
    # sort by distance from adjacent point to target, then by reading position of ap
    possible_dests = sorted(possible_dests, key=lambda x: (x[1], x[0][1], x[0][0]))
    print('Moving from {} to {}, chasing {}. (possibilities: {}),'.format(pos, possible_dests[0][0], target, possible_dests))
    dest = possible_dests[0][0]

    board[pos[0]][pos[1]] = True
    board[dest[0]][dest[1]] = False
    unit.x = dest[0]
    unit.y = dest[1]

    return dest

def attack(unit, board, enemies):
    enemy_list = []
    for e in enemies:
        if get_dist(unit.pos(), e.pos()) == 1:
            enemy_list.append(e)

    if not enemy_list:
        return False
    
    enemy_list = sorted(enemy_list, key=lambda x: (x.hp, x.y, x.x))

    target = enemy_list[0]
    target.hp -= unit.attack
    if target.hp <= 0:
        enemies.remove(target)
        board[target.x][target.y] = True

def print_board(board, goblins, elves):
    result = []
    for _ in range(height):
        result.append('#' * width)
    
    for g in goblins:
        line = result[g.y]
        result[g.y] = line[:g.x] + 'G' + line[g.x + 1:]
    
    for e in elves:
        line = result[e.y]
        result[e.y] = line[:e.x] + 'E' + line[e.x + 1:]
    
    for y in range(height):
        line = result[y]
        for x in range(width):
            if board[x][y]:
                line = line[:x] + '.' + line[x + 1:]
        result[y] = line

    print('\n'.join(result))

turn_counter = 0
done = False
while True:
    if turn_counter > 10000:
        raise Exception('This is probably taking too long')
    #print(turn_counter)
    
    print('On turn {}, board is:'.format(turn_counter))
    print_board(board, goblins, elves)
    
    ordered_units = sorted(goblins + elves, key=lambda x: (x.y, x.x))
    for u in ordered_units:
        if u.hp <= 0:
            continue
        prev_pos = u.pos()
        if u.is_elf:
            enemies = goblins
        else:
            enemies = elves
        move = move_unit(u, board, enemies)
        if move is None:
            done = True
            break
        a = attack(u, board, enemies)
    
    if done:
        break
    
    turn_counter += 1

winner = 'goblins' if len(goblins) else 'elves'
winner_hp = sum([x.hp for x in (goblins + elves)])

print('After {} turns, {} won with {} hp. Result {}'.format(turn_counter, winner, winner_hp, winner_hp * turn_counter))
