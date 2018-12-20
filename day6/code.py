
infinites = set()
counts = {}
w = 0
h = 0
score_threshold = 10000
with open('input.txt', 'r') as dum:
    for line in dum:
        cur_points = line.split(',')
        cur_points = (int(cur_points[0].strip()), int(cur_points[1].strip()))
        if cur_points[0] > w:
            w = cur_points[0]
        if cur_points[1] > h:
            h = cur_points[1]
        counts[cur_points] = 0

def get_owner(x, y, points):
    owner = None
    score = w + h
    full_score = 0

    for p in points:
        cur_score = abs(x - p[0]) + abs(y - p[1])
        full_score += cur_score
        if cur_score < score:
            score = cur_score
            owner = p
        elif cur_score == score:
            owner = None
    
    return owner, full_score

region_count = 0
for i in range(w):
    for j in range(h):
        o, s = get_owner(i, j, counts)
        if o is not None:
            counts[o] += 1
        
        if s < score_threshold:
            region_count += 1
            if i == 0 or i == w - 1 or j == 0 or j == h - 1:
                print('hey-o, stretch that region check: {}, {}'.format(i, j))
        

# the idea here is to create a ring that is 50% bigger around the main occupied area
# if any point has ownership in this ring, then it should have infinite ownership, because all 'disputes' should be finished
# once you're this far out.
#
# so just mark any owners in this ring as infinites
for i in range((2 * w) - int(w / 2)):
    h1 = 0 - int(h / 2)
    h2 = int(1.5 * h)

    o, _ = get_owner(i, h1, counts)
    if o is not None:
        infinites.add(o)
    
    o, _ = get_owner(i, h2, counts)
    if o is not None:
        infinites.add(o)


for j in range((2 * h) - int(h / 2)):
    w1 = 0 - int(w / 2)
    w2 = int(1.5 * w)

    o, _ = get_owner(w1, j, counts)
    if o is not None:
        infinites.add(o)
    
    o, _ = get_owner(w2, j, counts)
    if o is not None:
        infinites.add(o)


max_area = 0
for p in counts:
    if p in infinites:
        continue
    if counts[p] > max_area:
        max_area = counts[p]

print('Max area: {}'.format(max_area))
print('Region count: {}'.format(region_count))