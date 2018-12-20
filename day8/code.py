nodes = {}
META_KEY = 'metadata'
CHILD_KEY = 'child_nodes'
PARENT_KEY = 'parent_node'
VALUE_KEY = 'value'
node_counter = 0

def read_node(pos, parent_node, data, nodes):
    global node_counter
    child_count = data[pos]
    children = []
    meta_count = data[pos + 1]
    metadata = []
    node_id = node_counter
    node_counter += 1

    new_pos = pos + 2
    for _ in range(child_count):
        new_pos, child_id = read_node(new_pos, node_id, data, nodes)
        children.append(child_id)
    
    for _ in range(meta_count):
        metadata.append(data[new_pos])
        new_pos += 1
    
    node = {
        PARENT_KEY: parent_node,
        CHILD_KEY: children,
        META_KEY: metadata
    }

    nodes[node_id] = node
    return new_pos, node_id

with open('input.txt', 'r') as f:
    data = list(map(int, f.read().split(' ')))
    pos, root_id = read_node(0, None, data, nodes)

    if pos != len(data):
        print('Something went wrong')

meta_total = 0
for n_id in nodes:
    n = nodes[n_id]
    for m in n[META_KEY]:
        meta_total += m

print('Metadata total: {}'.format(meta_total))

def get_node_value(node_id, nodes):
    n = nodes[node_id]
    if VALUE_KEY in n:
        return n[VALUE_KEY]
    
    value = 0
    if len(n[CHILD_KEY]) == 0:
        value = sum(n[META_KEY])
    else:
        for m in n[META_KEY]:
            if m > 0 and m <= len(n[CHILD_KEY]):
                child_val = get_node_value(n[CHILD_KEY][m-1], nodes) 
                value += child_val

    n[VALUE_KEY] = value
    return value

print('Value of root: {}'.format(get_node_value(root_id, nodes)))