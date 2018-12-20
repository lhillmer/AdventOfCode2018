
board = None
carts = []
cart_id = 0
horizontal_chars = ['-', '+', '<', '>']
intersection = 'urld'

class Cart:
    def __init__(self, x, y, direction):
        global cart_id
        self.id = cart_id
        cart_id += 1

        self.x = x
        self.y = y
        self.dir = direction
        self.next_turn = 'l'

with open('input.txt', 'r') as f:
    data = f.read().split('\n')

    height = len(data)
    width = max([len(line) for line in data])
    board = []
    for x in range(width):
        board.append([None] * height)

    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == '|':
                board[x][y] = 'ud'
            elif char == 'v':
                board[x][y] = 'ud'
                carts.append(Cart(x, y, 'd'))
            elif char == '^':
                board[x][y] = 'ud'
                carts.append(Cart(x, y, 'u'))
            elif char == '-':
                board[x][y] = 'lr'
            elif char == '>':
                carts.append(Cart(x, y, 'r'))
                board[x][y] = 'lr'
            elif char == '<':
                carts.append(Cart(x, y, 'l'))
                board[x][y] = 'lr'
            elif char == '/':
                if x - 1 >= 0 and line[x - 1] in horizontal_chars:
                    board[x][y] = 'lu'
                else:
                    board[x][y] = 'dr'
            elif char == '\\':
                if x - 1 >= 0 and line[x - 1] in horizontal_chars:
                    board[x][y] = 'ld'
                else:
                    board[x][y] = 'ur'
            elif char == '+':
                board[x][y] = intersection
            elif char != ' ':
                raise Exception('Something\'s up: {}'.format(char))

print('Have {} carts'.format(len(carts)))

ticker = 0
crash = None
turn_order = ['l', 's', 'r']
turn_helper = ['l', 'd', 'r', 'u']

def turn(starting_dir, turn):
    if turn == 's':
        return starting_dir
    
    idx = turn_helper.index(starting_dir)
    if turn == 'l':
        idx += 1
    else:
        idx -= 1
    
    return turn_helper[idx % len(turn_helper)]

def get_curve_dir(starting_dir, tile):
    if starting_dir == 'u':
        opposite_dir = 'd'
    elif starting_dir == 'd':
        opposite_dir = 'u'
    elif starting_dir == 'r':
        opposite_dir = 'l'
    else:
        opposite_dir = 'r'
    
    return tile.replace(opposite_dir, '')

def push_cart(board, cart):
    if cart.dir == 'u':
        next_pos = (cart.x, cart.y - 1)
    elif cart.dir == 'd':
        next_pos = (cart.x, cart.y + 1)
    elif cart.dir == 'l':
        next_pos = (cart.x - 1, cart.y)
    elif cart.dir == 'r':
        next_pos = (cart.x + 1, cart.y)
    else:
        raise Exception('Invalid direction: {}'.format(cart.dir))
    
    if next_pos[0] < 0 or next_pos[0] >= width or next_pos[1] < 0 or next_pos[1] >= height:
        raise Exception('Trying to access invalid location: {}'.format(next_pos))
    
    tile = board[next_pos[0]][next_pos[1]] 
    if tile is None:
        raise Exception('Trying to move to empty board location: {}'.format(next_pos))
    
    if tile == intersection:
        next_dir = turn(cart.dir, cart.next_turn)
        cart.next_turn = turn_order[(turn_order.index(cart.next_turn) + 1) % len(turn_order)]
    elif tile in ['lu', 'dr', 'ld', 'ur']:
        next_dir = get_curve_dir(cart.dir, tile)
    else:
        if len(tile) != 2:
            raise Exception('Weird tile: {}'.format(tile))
        next_dir = cart.dir
    
    cart.x = next_pos[0]
    cart.y = next_pos[1]
    cart.dir = next_dir

def collision(cart_list, cart):
    for c_idx in range(len(cart_list)):
        c = cart_list[c_idx]
        if c.id == cart.id:
            continue
        if cart.x == c.x and cart.y == c.y:
            cart_list.remove(cart)
            cart_list.remove(c)
            break

while len(carts) != 1:
    ticker += 1
    if ticker > 100000:
        raise Exception('This is probably taking too long')
    ordered_carts = sorted(carts, key=lambda c: c.y * 1000 + c.x)
    for c in ordered_carts:
        push_cart(board, c)
        collision(carts, c)

print('After {} turns, last cart at {}'.format(ticker, (carts[0].x, carts[0].y)))

