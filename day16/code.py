import copy


def load():
    part_1 = []
    part_2 = []

    with open('input.txt', 'r') as f:
        data = f.read().split('\n')
        cur_loc = 0
        while True:
            cur = data[cur_loc:cur_loc + 4]
            if not cur[0] and not cur[1]:
                break
            r_in = [int(x.strip()) for x in cur[0].split('[')[1].split(']')[0].split(',')]
            inp = [int(x.strip()) for x in cur[1].split(' ')]
            r_out = [int(x.strip()) for x in cur[2].split('[')[1].split(']')[0].split(',')]
            part_1.append((inp, r_in, r_out))
            cur_loc += 4
        
        for i in range(cur_loc + 2, len(data)):
            part_2.append([int(x) for x in data[i].split(' ')])
        
    return part_1, part_2


all_ops = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']
def handle_op(op, registers, input_vals):
    if op == 'addr':
        result = registers[input_vals[1]] + registers[input_vals[2]]
    elif op == 'addi':
        result = registers[input_vals[1]] + input_vals[2]
    elif op == 'mulr':
        result = registers[input_vals[1]] * registers[input_vals[2]]
    elif op == 'muli':
        result = registers[input_vals[1]] * input_vals[2]
    elif op == 'banr':
        result = registers[input_vals[1]] & registers[input_vals[2]]
    elif op == 'bani':
        result = registers[input_vals[1]] & input_vals[2]
    elif op == 'borr':
        result = registers[input_vals[1]] | registers[input_vals[2]]
    elif op == 'bori':
        result = registers[input_vals[1]] | input_vals[2]
    elif op == 'setr':
        result = registers[input_vals[1]]
    elif op == 'seti':
        result = input_vals[1]
    elif op == 'gtir':
        result = 1 if input_vals[1] > registers[input_vals[2]] else 0
    elif op == 'gtri':
        result = 1 if registers[input_vals[1]] > input_vals[2] else 0
    elif op == 'gtrr':
        result = 1 if registers[input_vals[1]] > registers[input_vals[2]] else 0
    elif op == 'eqir':
        result = 1 if input_vals[1] == registers[input_vals[2]] else 0
    elif op == 'eqri':
        result = 1 if registers[input_vals[1]] == input_vals[2] else 0
    elif op == 'eqrr':
        result = 1 if registers[input_vals[1]] == registers[input_vals[2]] else 0

    registers = copy.copy(registers)
    registers[input_vals[3]] = result
    return registers

def test_all_ops(input_vals, reg_in, reg_out):
    global all_ops
    result = []
    for o in all_ops:
        if reg_out == handle_op(o, reg_in, input_vals):
            result.append(o)
    
    return result

def part_one():
    input_list, _ = load()
    threshold = 3
    result = 0
    for idx, i in enumerate(input_list):
        if len(test_all_ops(i[0], i[1], i[2])) >= threshold:
            result += 1
    print('Part 1 result: {}'.format(result))

def find_match(potential_matches):
    results = {}
    for pm in potential_matches:
        code = pm[0]
        if len(pm[1]) == 1:
           return pm[0], pm[1][0]
        cur_set = set(pm[1])
        if code in results:
            results[code] = cur_set.intersection(results[code])
            if len(results[code]) == 1:
                return code, results[code].pop()
        else:
            results[code] = cur_set
    
    return None
        

def identify_op_codes(input_list):
    global all_ops
    potential_matches = [(i[0][0], test_all_ops(i[0], i[1], i[2])) for i in input_list]
    result = {}
    while len(result) != len(all_ops):
        latest_match = find_match(potential_matches)
        if latest_match is None:
            raise Exception('Failed to find match from {}'.format(potential_matches))
        result[latest_match[0]] = latest_match[1]
        
        potential_matches = [pm for pm in potential_matches if pm[0] != latest_match[0]]
        for pdx in range(len(potential_matches)):
            pm = potential_matches[pdx]
            if latest_match[1] in pm[1]:
                pm[1].remove(latest_match[1])
    
    return result
                
def part_two():
    samples, program = load()
    op_codes = identify_op_codes(samples)

    reg_in = [0, 0, 0, 0]
    for op in program:
        reg_in = handle_op(op_codes[op[0]], reg_in, op)
    
    print('Part 2 result: {}'.format(reg_in[0]))

part_one()
part_two()

