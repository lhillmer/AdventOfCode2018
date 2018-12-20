
big_string = ""
with open('input.txt', 'r') as dum:
    big_string = dum.read()

def fully_react(inp):
    def react(inp, pos_1, pos_2):
        while True:
            if pos_1 < 0 or pos_2 >= len(inp):
                break

            if inp[pos_1] != inp[pos_2] and inp[pos_1].upper() == inp[pos_2].upper():
                pos_1 -= 1
                pos_2 += 1
            else:
                break
        
        return inp[:pos_1 + 1] + inp[pos_2:], pos_1, pos_2

    no_change = False
    while not no_change:
        offset = 0
        for idx in range(len(inp)):
            actual_idx = idx + offset
            if actual_idx >= len(inp) - 1:
                break

            inp, start_pos, end_pos = react(inp, idx, idx + 1)
            if start_pos + 1 != end_pos:
                # there was a reaction, correct the offset
                offset_piece = ((end_pos - 1) - start_pos) / 2
                if offset_piece != int(offset_piece):
                    print('wuh woh: {}, {},  {}'.format(start_pos, end_pos, offset_piece))
                    break
                offset += offset_piece
        
        if offset == 0:
            no_change = True
    
    return inp

problem_letters = {}
for x in big_string:
    if x.upper() not in problem_letters:
        problem_letters[x.upper()] = 0

orig_string = big_string

big_string = fully_react(big_string)

shortest_len = len(orig_string)
for x in problem_letters:
    print('Handling letter: {}'.format(x))
    cur_len = len(fully_react(orig_string.replace(x, '').replace(x.lower(), '')))
    if cur_len < shortest_len:
        shortest_len = cur_len



print('Resulting length: {}'.format(len(big_string)))
print('Resulting optimized length: {}'.format(shortest_len))





