# just make it really big. hopefully big enough
scores = [None] * (29000000)
scores[0] = 3
scores[1] = 7
s_idx = 2
last_checked = 0
target = [int(x) for x in '074501']

e_1 = 0
e_2 = 1

done = False

while not done:
    s_1 = scores[e_1]
    s_2 = scores[e_2]
    result = s_1 + s_2

    if result < 10:
        scores[s_idx] = result
    else:
        scores[s_idx] = 1
        s_idx += 1
        if s_idx >= len(scores):
            raise Exception('Failed to generate sequence')
        scores[s_idx] = result % 10
    
    s_idx += 1
    if s_idx >= len(scores):
        raise Exception('Failed to generate sequence')
    
    while last_checked + len(target) <= s_idx:
        # print('Checking from {} to {}: {} vs {}'.format(last_checked, last_checked + len(target), target, scores[last_checked: last_checked + len(target)]))
        if target == scores[last_checked: last_checked + len(target)]:
            done = True
            break
        last_checked += 1
    
    e_1 += (s_1 + 1)
    e_1 = e_1 % s_idx
    e_2 += (s_2 + 1)
    e_2 = e_2 % s_idx

print('Sequence found after {}'.format(last_checked))
