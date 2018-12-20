import copy

prereqs = {}
mentioned_steps = set()
with open('input.txt', 'r') as dum:
    for line in dum:
        tokens = line.split(' ')
        target = tokens[7]
        req = tokens[1]

        mentioned_steps.add(target)
        mentioned_steps.add(req)

        if target in prereqs:
            prereqs[target].append(req)
        else:
            prereqs[target] = [req]

frontier = []

for s in list(mentioned_steps):
    if s not in prereqs:
        frontier.append(s)

f2 = copy.deepcopy(frontier)
p2 = copy.deepcopy(prereqs)

def do_step(step, cur_result, prereqs, frontier):
    for s in prereqs:
        if step in prereqs[s]:
            prereqs[s].remove(step)
            if not prereqs[s]:
                frontier.append(s)
                
    for s in frontier:
        if s in prereqs:
            del prereqs[s]
    
    cur_result += step

    return cur_result

result = ''
while frontier:
    next_step = sorted(frontier)[0]
    frontier.remove(next_step)
    result = do_step(next_step, result, prereqs, frontier)

print('Result: {}'.format(result))

# timed version
workers = {}
for worker in range(5):
    workers[worker] = (0, '')

timed_result = ''
time_taken = 0
offset = ord('A') - 1

def get_next_free_worker(workers):
    free_workers = [w for w in workers if workers[w][1] == '']
    if free_workers:
        return free_workers[0]
    return None

def get_shortest_works(workers):
    shortest_work = 200
    result = []
    for w in workers:
        if workers[w][0] != 0 and workers[w][0] < shortest_work:
            result = [w]
            shortest_work = workers[w][0]
        elif workers[w][0] != 0 and workers[w][0] == shortest_work:
            result.append(w)
    
    return result

def jump_time(workers, time):
    for w in workers:
        if workers[w][0] != 0:
            workers[w] = (workers[w][0] - time, workers[w][1])

def all_workers_idle(workers):
    return sum([workers[w][0] for w in workers]) == 0

while True:
    # first, queue up every available worker
    next_worker = get_next_free_worker(workers)
    while next_worker is not None and f2:
        next_step = sorted(f2)[0]
        f2.remove(next_step)

        workers[next_worker] = (60 + (ord(next_step) - offset), next_step)
        next_worker = get_next_free_worker(workers)
    
    # then, find the amount of time needed to jump to complete next task
    # we can ignore 0's because that just means we have more workers than tasks
    next_workers = get_shortest_works(workers)
    if not next_workers:
        raise Exception('C\'mon man')
    
    # execute all completed tasks, and move forward the appropriate amount of time
    jump = 0
    for worker_id in next_workers:
        # all jumps should be the same, so just grab the first
        if jump == 0:
            jump = workers[worker_id][0]
        
        timed_result = do_step(workers[worker_id][1], timed_result, p2, f2)

        workers[worker_id] = (0, '')

    if jump == 0:
        raise Exception('really?')
    time_taken += jump
    jump_time(workers, jump)

    if all_workers_idle(workers) and not f2:
        break


print('Timed result: {} takes {} s'.format(timed_result, time_taken))