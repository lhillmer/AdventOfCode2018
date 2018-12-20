
with open('part1_input.txt', 'r') as dum:
    cur = 0
    prevs = [cur]
    changes = []
    for line in dum:
        if line.startswith('+'):
            line = line[1:]
        
        changes.append(int(line))

dupe_found = False
idx = 0
while not dupe_found:
    cur += changes[idx]
    idx += 1
    idx = idx % len(changes)
    if cur in prevs:
        dupe_found = True
    else:
        prevs.append(cur)

print(cur)