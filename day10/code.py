import copy

pos = {}
vel = {}
node_counter = 0

with open('input.txt', 'r') as f:
    for line in f:
        parts = line.split('<')
        cur_pos = parts[1].split('>')[0]
        cur_vel = parts[2].split('>')[0]

        cur_pos = cur_pos.split(',')
        cur_vel = cur_vel.split(',')

        pos[node_counter] = (int(cur_pos[0].strip()), int(cur_pos[1].strip()))
        vel[node_counter] = (int(cur_vel[0].strip()), int(cur_vel[1].strip()))
        node_counter += 1

threshold = 0.95
done = False

time = 0

def get_occupied_area(pos):
    min_x = pos[0][0]
    min_y = pos[0][0]
    max_x = pos[0][1]
    max_y = pos[0][1]

    for p in pos:
        if pos[p][0] < min_x:
            min_x = pos[p][0]
        if pos[p][0] > max_x:
            max_x = pos[p][0]
        if pos[p][1] < min_y:
            min_y = pos[p][1]
        if pos[p][1] > max_y:
            max_y = pos[p][1]
    
    return (max_x - min_x + 1) * (max_y - min_y + 1)


while True:
    print('Checking time {}'.format(time))
    # safeguard
    if time > 50000:
        raise Exception('something probably went wrong')
    # calculate the current number of adjencies
    # but onl if the bounded area is below some other abitrary threshold
    if get_occupied_area(pos) < 50000:
        adj_count = 0
        for p in pos:
            for p2 in pos:
                if p != p2:
                    if abs(pos[p][0] - pos[p2][0]) + abs(pos[p][1] - pos[p2][1]) <= 1:
                        adj_count += 1
                        # only count once per point
                        break

        # if we're above the abitrary threshold, then we probably found it
        if (float(adj_count) / float(node_counter)) >= threshold:
            break
    
    # otherwise, step time
    for p in pos:
        pos[p] = (pos[p][0] + vel[p][0], pos[p][1] + vel[p][1])
    time += 1

def print_pos(pos):
    min_x = pos[0][0]
    min_y = pos[0][0]
    max_x = pos[0][1]
    max_y = pos[0][1]

    for p in pos:
        if pos[p][0] < min_x:
            min_x = pos[p][0]
        if pos[p][0] > max_x:
            max_x = pos[p][0]
        if pos[p][1] < min_y:
            min_y = pos[p][1]
        if pos[p][1] > max_y:
            max_y = pos[p][1]

    board = []    
    for idx in range(min_x, max_x + 1):
        board.append([False] * ((max_y + 1) - min_y))
    
    for p in pos:
        board[pos[p][0] - min_x][pos[p][1] - min_y] = True

    for jdx in range(max_y - min_y + 1):
        cur_line = ''
        for idx in range(max_x - min_x + 1):
            if board[idx][jdx]:
                cur_line += '#'
            else:
                cur_line += '.'
        print(cur_line)
    
print_pos(pos)
print('Stopped at time {}'.format(time))


