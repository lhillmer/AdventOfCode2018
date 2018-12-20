
with open('input.txt', 'r') as dum:
    stuff_things = {}
    for line in dum:
        parts = line.split('@')
        data = parts[1].strip().split(':')
        
        offsets = data[0].strip().split(',')
        sizes = data[1].strip().split('x')

        offsets = (int(offsets[0]), int(offsets[1]))
        sizes = (int(sizes[0]), int(sizes[1]))

        stuff_things[parts[0].strip()] = (offsets[0], offsets[1], offsets[0] + sizes[0], offsets[1] + sizes[1])
    
coverage = {}
overlap_counts = 0
for entry_name in stuff_things:
    entry = stuff_things[entry_name]
    for x in range(entry[0], entry[2]):
        for y in range(entry[1], entry[3]):
            key = (x, y)
            if key in coverage and coverage[key] == 1:
                    overlap_counts += 1
            elif key not in coverage:
                coverage[key] = 0
            
            coverage[key] += 1

untouched = None
for entry_name in stuff_things:
    entry = stuff_things[entry_name]
    cur_untouched = True
    for x in range(entry[0], entry[2]):
        for y in range(entry[1], entry[3]):
            key = (x, y)
            if coverage[key] != 1:
                cur_untouched = False
                break
        if not cur_untouched:
            break

    if cur_untouched:
        if untouched is not None:
            print("wuh woh: {}".format(untouched))
        untouched = entry_name
    
    print("Overlaps: {}".format(overlap_counts))
    print("Untouched: {}".format(untouched))