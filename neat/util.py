from enum import IntEnum

class NodeType(IntEnum):
    SENSOR = 1
    HIDDEN = 2
    OUT = 3

class ActivationType(IntEnum):
    SIGMOID = 1
    IDENTITY = 2
    SOFTMAX = 3

def clamp(val, min_val, max_val):
    return min(max(val, min_val), max_val)

def detect_cycle(in_node, out_node):
    visited = set()
    to_visit = [in_node] + [link.in_node for link in in_node.incoming_links if not link.is_recur]
    
    while to_visit:
        visit_node = to_visit.pop(0)
        visited.add(visit_node.gid)

        if visit_node.gid == out_node.gid:
            return True
        to_visit += [link.in_node for link in visit_node.incoming_links if link.in_node not in visited and not link.is_recur]
    
    return False

def compute_depth(node, depth):
    if len(node.incoming_links) == 0:
        return depth
    visited = []
    max_depth = -1
    for child_link in node.incoming_links:
        if not child_link.is_recur:
            max_depth = max(compute_depth(child_link.in_node, depth + 1), max_depth)
 
    return max_depth
