player_count = 459
marble_count = 7132000

class Node:
    def __init__(self, val, prev_node=None, next_node=None):
        if prev_node is None:
            prev_node = self
        if next_node is None:
            next_node = self
        self.next_node = next_node
        self.prev_node = prev_node
        self.val = val

class LinkedList:
    def __init__(self, start_val):
        self.start_node = Node(start_val)
        self.cur_node = self.start_node
    
    def add_node(self, val, offset):
        fwd = True if offset > 0 else False
        loc = self.cur_node
        for i in range(abs(offset)):
            if fwd:
                loc = loc.next_node
            else:
                loc = loc.prev_node
        
        node = Node(val, prev_node=loc, next_node=loc.next_node)
        loc.next_node = node
        node.next_node.prev_node = node
        self.cur_node = node
    
    def remove_node(self, offset):
        fwd = True if offset > 0 else False
        loc = self.cur_node

        for i in range(abs(offset)):
            if fwd:
                loc = loc.next_node
            else:
                loc = loc.prev_node
        
        loc.prev_node.next_node = loc.next_node
        loc.next_node.prev_node = loc.prev_node
        self.cur_node = loc.next_node

        return loc
            
board = LinkedList(0)
cur_marble_score = 0
cur_player = 0

player_score = {}
for i in range(1, player_count + 1):
    player_score[i] = 0

for i in range(marble_count):
    # update current player
    cur_player += 1
    if cur_player > player_count:
        cur_player = 1
    
    # update marble score
    cur_marble_score += 1
    
    # first, check if the current marble is a multiple of 23
    if cur_marble_score % 23 == 0:
        # here, we actually do stuff
        node = board.remove_node(-7)
        player_score[cur_player] += cur_marble_score + node.val
    else:
        # 'normal' turn
        board.add_node(cur_marble_score, 1)

best_player = 0
best_score = 0
for p in player_score:
    if player_score[p] > best_score:
        best_score = player_score[p]
        best_player = p

print('Player {} won with a score of {}'.format(best_player, best_score))