
with open('input.txt', 'r') as dum:
    id_list = []
    for line in dum:
        id_list.append(line)

count_2 = 0
count_3 = 0
match_result = None

for idx, i in enumerate(id_list):
    cur_dict = {}
    for c in i:
        if c in cur_dict:
            cur_dict[c] += 1
        else:
            cur_dict[c] = 1
    
    done_2 = False
    done_3 = False
    for x in cur_dict:
        if not done_2 and cur_dict[x] == 2:
            count_2 += 1
            done_2 = True
        elif not done_3 and cur_dict[x] == 3:
            count_3 += 1
            done_3 = True

    if match_result is None:
        for jdx in range(idx):
            matching = []
            j = id_list[jdx]
            for kdx in range(len(i)):
                if kdx < len(j):
                    if i[kdx] == j[kdx]:
                        matching.append(i[kdx])
                    
            
            if len(matching) == len(i) - 1:
                match_result = ''.join(matching)
                break
        
                    
    
    print("Checksum: {}".format(count_2 * count_3))
    print("Matching result: {}".format(match_result))