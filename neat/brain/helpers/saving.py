import json

from neat.helpers.saving import save_population as neat_save_pop, load_population as neat_load_pop

from neat.brain.brain_network import BrainNetwork
from neat.brain.electrical_node import ElectricalNode
from neat.brain.chemical_node import ChemicalNode
from neat.brain.brain_output_node import BrainOutputNode
from neat.brain.util import BrainNodeType
from neat.nets.basic_nets import build_basic_brain_net

def save_population(population, save_file):
    pop_dict = neat_save_pop(population, save_file)
    
    # Allows for fast look up of organisms
    org_cache = {}
    for org in population.orgs:
        org_cache[org.id] = org

    # Iterate over all organisms
    for org_dict in pop_dict["orgs"]:
        org = org_cache[org_dict["id"]]

        # Iterate over all nodes in a organism's network
        for gid, node_dict in org_dict["network"]["nodes"].items():
            if isinstance(org.net.nodes[gid], ElectricalNode):
                node_dict["brain_node_type"] = BrainNodeType.ELECTRICAL
                node_dict["active_sum"] = org.net.nodes[gid].active_sum
            elif isinstance(org.net.nodes[gid], ChemicalNode):
                node_dict["brain_node_type"] = BrainNodeType.CHEMICAL
                node_dict["active_sum"] = org.net.nodes[gid].active_sum
            elif isinstance(org.net.nodes[gid], BrainOutputNode):
                node_dict["brain_node_type"] = BrainNodeType.OUT
    
    # Save the population JSON
    with open(save_file, "w") as f:
        json.dump(pop_dict, f)
    
    return pop_dict


def load_population(args):
    print("LOADING BRAIN POP")
    population = neat_load_pop(args, brain=True)
    
    
    # Load the population dictionary
    with open(args.save_file) as f:
        pop_dict = json.load(f)
    population.base_org.net = build_basic_brain_net(
        args, len(population.base_org.net.depth_to_node[0]), pop_dict["base_org"]["network"]["out_size"])

    # Allows for fast look up of organisms
    org_cache = {}
    for org in population.orgs:
        org_cache[org.id] = org
    
    # Iterate over all organisms
    for org_dict in pop_dict["orgs"]:
        org = org_cache[org_dict["id"]]

        # Iterate over all nodes in a organism's network
        for gid, node_dict in org_dict["network"]["nodes"].items():
            if "brain_node_type" in node_dict:
                #org.net.nodes[gid]
                gid = int(gid)
                old_node = org.net.nodes[gid]

                if node_dict["brain_node_type"] == BrainNodeType.ELECTRICAL:     
                    org.net.nodes[gid] = ElectricalNode(
                        args, old_node.gid, old_node.depth, old_node.node_type, old_node.activation_type)
                elif node_dict["brain_node_type"] == BrainNodeType.CHEMICAL:
                    #print("CREATING CHEMICAL NODE")
                    org.net.nodes[gid] = ChemicalNode(
                        args, old_node.gid, old_node.depth, old_node.node_type, old_node.activation_type)
                elif node_dict["brain_node_type"] == BrainNodeType.OUT:
                    org.net.nodes[gid] = BrainOutputNode(
                        old_node.gid, old_node.depth, old_node.node_type, old_node.activation_type, old_node.out_pos)
                else:
                    assert False

                if "active_sum" in node_dict:
                    org.net.nodes[gid].active_sum = node_dict["active_sum"]
                    if org.net.nodes[gid].active_sum != -0.09 and org.net.nodes[gid].active_sum != 0.0:
                        print(org.net.nodes[gid].active_sum)

                org.net.nodes[gid].incoming_links = old_node.incoming_links
                org.net.nodes[gid].outgoing_links = old_node.outgoing_links
                
                for link in org.net.nodes[gid].outgoing_links:
                    link.in_node = org.net.nodes[gid]

                for link in org.net.nodes[gid].incoming_links:
                    link.out_node = org.net.nodes[gid]
                
                for node in org.net.depth_to_node[org.net.nodes[gid].depth]:
                    if node.gid == gid:
                        org.net.depth_to_node[org.net.nodes[gid].depth].remove(node)
                        break

                org.net.depth_to_node[org.net.nodes[gid].depth].append(org.net.nodes[gid]) 

    return population








