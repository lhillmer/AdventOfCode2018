
def load():
    with open('input.txt', 'r') as f:
        locs = []
        top = None
        left = None
        right = None
        bottom = None
        for line in f:
            parts = line.split(', ')
            p1 = parts[0].split('=')
            p1_is_x = p1[0] == 'x'
            p1_val = int(p1[1])
            p2 = parts[1].split('=')
            p2_range = p2[1].split('..')
            for i in range(int(p2_range[0]), int(p2_range[1]) + 1):
                if p1_is_x:
                    x_val = p1_val
                    y_val = i
                else:
                    x_val = i
                    y_val = p1_val

                locs.append((x_val, y_val))
                if top is None:
                    top = y_val
                    bottom = y_val
                    left = x_val
                    right = x_val
                
                if top < y_val:
                    top = y_val
                if bottom > y_val:
                    bottom = y_val
                if left > x_val:
                    left = x_val
                if right < x_val:
                    right = x_val
    
    return locs, (bottom, left - 1), (top, right + 1)

def get_water_bottom(board, height, start):
    cur_pos = start
    hit_bottom = False
    while True:
        if board[cur_pos[0]][cur_pos[1]]:
            break
        elif cur_pos[1] == height:
            hit_bottom = True
            break
        cur_pos = (cur_pos[0], cur_pos[1] + 1)
    return cur_pos, hit_bottom

def get_water_width(board, width, height, start):
    cur_pos = start
    left_fall = False
    right_fall = False
    while True:
        if cur_pos[1] + 1 != height and board[cur_pos[0]][cur_pos[1] + 1]:
            left_fall = True
            break
        elif board[cur_pos[0] - 1][cur_pos[1]]:
            break
        cur_pos = (cur_pos[0] - 1, cur_pos[1])

    left_pos = cur_pos
    cur_pos = start

    while True:
        if cur_pos[1] + 1 != height and board[cur_pos[0]][cur_pos[1] + 1]:
            right_fall = True
            break
        elif board[cur_pos[0] + 1][cur_pos[1]]:
            break
        cur_pos = (cur_pos[0] + 1, cur_pos[1])
    
    return left_pos, left_fall, cur_pos, right_fall

def update_board(board, start, stop, is_vertical, is_standing_water):
    if is_vertical:
        static = start[0]
        s1 = start[0]
        s2 = stop[1]
    else:
        static = start[1]
        s1 = start[1]
        s2 = stop[0]

    if is_standing_water:
        data = False
    else:
        data = True
    
    for i in range(s1, s2 + 1):
        if is_vertical:
            board[static][i] = data
        else:
            board[i][static] = data
    

def fill_water(standing_water, width, height, spawn):
    all_spawns = [spawn]
    while all_spawns:
        cur_spawn = all_spawns.pop(0)
        # let the water fall until you hit something
        stop_pos, hit_bottom = get_water_bottom(standing_water, height, cur_spawn)

        update_board(board, cur_spawn, stop_pos, True, False)
        # if we hit the bottom, this spawn point is done
        if hit_bottom:
            continue
        
        # otherwise, spread at the point where we hit something
        left_pos, left_fall, right_pos, right_fall = get_water_width(board, width, height, stop_pos)

        # if we filled to the edges, than update with standing water
        if not left_fall and not right_fall:
            update_board(board, left_pos, right_pos, False, True)

            # we need to restart with the current spawn point, to see where it falls on top of the water
            all_spawns.append(cur_spawn)
        else:
            # if we didn't fill to the edges, than update with flowing water
            update_board(board, left_pos, right_pos, False, False)

            # conditionally add either side if they led to falling
            if left_fall:
                all_spawns.append(left_pos)

            if right_fall:
                all_spawns.append(right_pos)
    

def part_one():
    # in this case bottom_left is the lowest x and y values
    # top_right is the highest x and y values

    locs, bottom_left, top_right = load()
    init_spawn = (500, 0)

    if init_spawn[1] < bottom_left[1]:
        bottom_left = (bottom_left[0], init_spawn[1])
    elif init_spawn[1] > top_right[1]:
        top_right = (top_right[0], init_spawn[1])

    if init_spawn[0] < bottom_left[0]:
        bottom_left = (init_spawn[0], bottom_left[1])
    elif init_spawn[0] > top_right[0]:
        top_right = (init_spawn[0], top_right[1])

    x_offset = bottom_left[0]
    y_offset = bottom_left[1]

    init_spawn = (init_spawn[0] - x_offset, init_spawn[1] - y_offset)

    width = top_right[0] - bottom_left[0]
    height = top_right[1] - bottom_left[1]
    
    print('Board is {} wide and {} tall'.format(width, height))

    standing_water, flowing_water = fill_water(locs, width, height, init_spawn)

    print('Part 1 result: {}'.format(len(standing_water) + len(flowing_water)))

part_one()

    