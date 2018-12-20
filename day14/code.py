
scores = [None] * (74501 + 10)
scores[0] = 3
scores[1] = 7
s_idx = 2

e_1 = 0
e_2 = 1


while True:
    s_1 = scores[e_1]
    s_2 = scores[e_2]
    result = s_1 + s_2

    if result < 10:
        scores[s_idx] = result
    else:
        scores[s_idx] = 1
        s_idx += 1
        if s_idx >= len(scores):
            break
        scores[s_idx] = result % 10
    
    s_idx += 1
    if s_idx >= len(scores):
        break
    
    e_1 += (s_1 + 1)
    e_1 = e_1 % s_idx
    e_2 += (s_2 + 1)
    e_2 = e_2 % s_idx

result_location = 74501
result = ''.join([str(x) for x in scores[result_location: result_location + 10]])
print('Result after {} is {}'.format(result_location, result))