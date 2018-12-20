import datetime
date_format = "%Y-%m-%d %H:%M"

dates = {}
with open('input.txt', 'r') as dum:
    for line in dum:
        parts = line.split(']')
        cur_date = datetime.datetime.strptime(parts[0].strip('['), date_format)

        if cur_date.hour == 23:
            cur_date = cur_date + datetime.timedelta(days=1)
        elif cur_date.hour != 0:
            print('ahhhhhhh: {}'.format(line))

        date_key = (cur_date.year, cur_date.month, cur_date.day)
        if date_key not in dates:
            dates[date_key] = []
        
        raw = parts[1].strip()
        if raw.startswith('wakes'):
            data = 1
        elif raw.startswith('falls'):
            data = 0
        else:
            data = raw.split('#')[1].split(' ')[0]

        if cur_date.hour != 0 and not isinstance(data, str):
            print('whoa there bessy: {}'.format(line))
        elif cur_date.hour != 0:
            cur_date = cur_date.replace(hour=0, minute=0)
        
        dates[date_key].append((cur_date.minute, data))

for d in dates:
    dates[d] = sorted(dates[d], key=lambda x: x[0])
    if len(dates[d]) > 1 and dates[d][0][0] == 0 and dates[d][1][0] == 0:
        if dates[d][2][0] == 0:
            print("PANIC: {}".format(dates[d]))
        if isinstance(dates[d][1][1], str):
            dates[d][1], dates[d][0] = dates[d][0], dates[d][1]

guards = {}

for d in dates:
    guard_id = None
    asleep_times = []
    last_data = -1
    last_data_time = -1
    for entry in dates[d]:
        if guard_id is None:
            if not isinstance(entry[1], str):
                print("Expected Guard ID for date {}, got {}".format(d, entry[1]))
                break
            guard_id = entry[1]
            if guard_id not in guards:
                guards[guard_id] = {}
            last_data = 1
            last_data_time = entry[0]
        else:
            if last_data == -1:
                print("whoa there, something went wrong {}".format(dates[d]))
                break
            if last_data == entry[1]:
                print("whoa there, identical values? {}".format(dates[d]))
                break

            if last_data == 0 and entry[1] == 1:
                if last_data_time == -1:
                    print('really, error checking is very annoying')
                asleep_times.append((last_data_time, entry[0]))
                last_data = entry[1]
                last_data_time = entry[0]
            elif last_data == 1 and entry[1] == 0:
                last_data = entry[1]
                last_data_time = entry[0]
            else:
                print('somethings fucky')
    
    if last_data == 0:
        print('really?')
    
    # now we have a list of (inclusive, non-inclusive) sleep time tuples
    todays_sleeping = {}
    for i in range(0, 60):
        todays_sleeping[i] = False
    
    for sleep in asleep_times:
        for i in range(sleep[0], sleep[1]):
            todays_sleeping[i] = True
    
    guards[guard_id][d] = todays_sleeping

# now we have the data stored by minute, per date, by guard
sleepiest_guard = None
most_sleeps = 0
for guard_id in guards:
    sleep_total = 0
    for d in guards[guard_id]:
        shift_sleeps = guards[guard_id][d]
        for m in shift_sleeps:
            if shift_sleeps[m]:
                sleep_total += 1
    
    if sleep_total > most_sleeps:
        sleepiest_guard = guard_id
        most_sleeps = sleep_total

# now we have the sleepiest guard, find the most common minute
sleep_heatmap = {}
for i in range(0, 60):
    sleep_heatmap[i] = 0

for d in guards[sleepiest_guard]:
    shift_sleeps = guards[sleepiest_guard][d]
    for m in shift_sleeps:
        if shift_sleeps[m]:
            sleep_heatmap[m] += 1

sleepiest_minute = 0
most_sleeps = 0
for m in sleep_heatmap:
    if sleep_heatmap[m] > most_sleeps:
        sleepiest_minute = m
        most_sleeps = sleep_heatmap[m]

# code for second strategy
guard_sleep_heatmaps = {}
strat_two_sleepiest_minute = 0
strat_two_sleepiest_guard = None
strat_two_sleeps = 0
for guard_id in guards:
    cur_heatmap = {}
    for i in range(0, 60):
        cur_heatmap[i] = 0
    
    for d in guards[guard_id]:
        shift_sleeps = guards[guard_id][d]
        for m in shift_sleeps:
            if shift_sleeps[m]:
                cur_heatmap[m] += 1
                if cur_heatmap[m] > strat_two_sleeps:
                    strat_two_sleeps = cur_heatmap[m]
                    strat_two_sleepiest_minute = m
                    strat_two_sleepiest_guard = guard_id

print("Sleepiest guard: {}, best minute: {}, result: {}".format(
    sleepiest_guard, sleepiest_minute,
    int(sleepiest_guard) * sleepiest_minute
))
print("Strat 2 sleepiest guard: {}, best minute: {}, result: {}".format(
    strat_two_sleepiest_guard, strat_two_sleepiest_minute,
    int(strat_two_sleepiest_guard) * strat_two_sleepiest_minute
))