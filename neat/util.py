from enum import Enum

class NodeType(Enum):
    SENSOR = 1
    HIDDEN = 2
    OUT = 3

class ActivationType(Enum):
    SIGMOID = 1
    IDENTITY = 2
    SOFTMAX = 3

def clamp(val, min_val, max_val):
    return min(max(val, min_val), max_val)

def detect_cycle(in_node, out_node):
    visited = set()
    to_visit = [in_node] + [link.in_node for link in in_node.incoming_links]
    
    while to_visit:
        visit_node = to_visit.pop(0)
        visited.add(visit_node.gid)

        if visit_node.gid == out_node.gid:
            return True
        to_visit += [link.in_node for link in visit_node.incoming_links if link.in_node not in visited]
    
    return False

def compute_depth(node, depth):
    if len(node.incoming_links) == 0:
        return depth
    visited = []
    max_depth = -1
    for child_node in node.incoming_links:
        max_depth = max(compute_depth(child_node.in_node, depth + 1), max_depth)
    
    return max_depth
