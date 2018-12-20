import math

width = 300
height = 300
serial = 5719

board = []

def calc(x, y):
    global serial
    rack_id = x + 10
    result = rack_id * y
    result += serial
    result *= rack_id
    # get hundreds digit
    result = result % 1000
    if not isinstance(result, int):
        raise Exception('wah wah wah {}'.format(type(result)))
    result = math.floor(result / 100)
    return result - 5

for i in range(width):
    board.append([])
    for j in range(height):
        board[i].append(calc(i, j))

# lowest value possible for a 3x3 grid
m_val = -45
m_pos = None

for i in range(width - 2):
    for j in range(height - 2):
        val = 0
        for k in range(3):
            for l in range(3):
                val += board[i + k][j + l]
        if val > m_val:
            m_val = val
            m_pos = (i, j)

print('Best Location: {} with a score of {}'.format(m_pos, m_val))

m_val = -45
m_pos = None

for i in range(width):
    for j in range(height):
        print((i, j))
        sq_size = 0
        val = 0
        max_width = width - i
        max_height = height - j
        max_sq_size = min(max_width, max_height)

        while sq_size < max_sq_size:
            sq_size += 1

            # add the edges for the next square size
            for k in range(sq_size):
                try:
                    val += board[i + k][j + sq_size - 1]
                except Exception as e:
                    print('{} + {}, {} + {} - 1'.format(i, k , j, sq_size))
                    raise e
                # don't double count the one square that's on each edge
                if k != (sq_size - 1):
                    val += board[i + sq_size - 1][j + k]
            
            if val > m_val:
                m_val = val
                m_pos = (i, j, sq_size)

print ('Best square of any size: {} with a score of {}'.format(m_pos, m_val))