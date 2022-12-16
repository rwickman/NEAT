import json, os

from neat.population import Population
from neat.organism import Organism
from neat.network import Network
from neat.node import Node, OutNode
from neat.link import Link
from neat.species import Species
from neat.util import NodeType

def _create_link_dict(net):
    """Create dictionary for all the links in a network."""
    link_list = []
    for gid_tuple, link in net.links.items():
        link_list.append({
            "gid_tuple": gid_tuple,
            "weight": link.trait.weight,
            "bias": link.trait.bias,
            "is_recur": link.is_recur,
            "enabled": link.enabled
        })
    
    return link_list

def _create_node_dict(net):
    """Create dictionary for all the nodes in a network."""
    node_dict = {}
    for node in net.nodes.values():
        node_dict[node.gid] = {
            "depth": node.depth,
            "node_type": node.node_type,
            "activation_type": node.activation_type
        }
        if node.node_type == NodeType.OUT:
            node_dict[node.gid]["out_pos"] = node.out_pos
    
    return node_dict

def _create_link_count_dict(net):
    link_count_list = []
    for gid_tuple, count in net.link_dict.items():
        link_count_list.append({
            "gid_tuple": gid_tuple,
            "count": count
        })
    
    return link_count_list


def _create_net_dict(net):
    return {
        "links": _create_link_dict(net),
        "nodes": _create_node_dict(net),
        "net_depth": len(net.depth_to_node),
        "out_size": net.out_size,
        "link_count_list": _create_link_count_dict(net)}

def _create_inv_counter_dict(inv_counter):

    # Create invocation counter dictionary
    inv_link_list = []
    for gid_tuple, gid in inv_counter.link_dict.items():
        inv_link_list.append({
            "gid_tuple": gid_tuple,
            "gid": gid
        })
    
    inv_dict = {
        "inv_link_list": inv_link_list,
        "gid_counter": inv_counter.gid_counter
    }

    return inv_dict

def save_population(population: Population, save_file: str):
    # For each organsism, save the ID and fitness_sum and num_updates
    # Save the depth of each node so you can recreate the depth_to_node dictionary
    # Have Dict of links, key is (in_node GID, out_node GID, is_recur) -> weight, bias
    # Save cur_id used to assign new ids for
    # Save the invocation counter  
    orgs = []
    for org in population.orgs:
        org_dict = {
            "id": org.id,
            "avg_fitness": org.avg_fitness,
            "generation": org.generation,
            "best_fitness": org.best_fitness,
            "num_updates": org._num_updates
        }

        org_dict["network"] = _create_net_dict(org.net)

        orgs.append(org_dict)

    # Save the species list
    species_list = []
    for species in population.species_list:
        species_dict = {
            "id": species.species_id,
            "org_ids" : [org.id for org in species.orgs],
            "age": species.age
        }
        species_list.append(species_dict)

    # Save the base organism
    base_org = {
        "id": population.base_org.id,
        "network": _create_net_dict(population.base_org.net),
        "generation": 0
    }

    # Aggregate everything into this population dictionary
    pop_dict = {
        "orgs": orgs,
        "generation": population.generation,
        "cur_id": population.cur_id,
        "inv_dict": _create_inv_counter_dict(population.inv_counter),
        "base_org": base_org,
        "species_list": species_list
    }

    # # Create the save directory if it doesn't exist
    # if not os.path.exists(save_dir):
    #     os.mkdir(save_dir)
    
    # Save the population JSON
    with open(save_file, "w") as f:
        json.dump(pop_dict, f)



def _load_link_count_dict(link_count_list):
    """This must be called AFTER links/nodes have been added."""
    link_count_dict = {}
    for link_dict in link_count_list:
        link_count_dict[tuple(link_dict["gid_tuple"])] = link_dict["count"]
    
    return link_count_dict

def _load_organism(config, org_dict: dict):
    net_dict = org_dict["network"]
    net = Network(net_dict["out_size"])
    # Load the nodes
    net.depth_to_node = [[] for i in range(net_dict["net_depth"])]
    for node_gid, node_dict in net_dict["nodes"].items():
        if node_dict["node_type"] == NodeType.OUT:
            # Create an output node
            node = OutNode(
                int(node_gid),
                node_dict["depth"],
                node_dict["node_type"],
                node_dict["activation_type"],
                node_dict["out_pos"])
        else:
            # Create a hidden/input node
            node = Node(
                int(node_gid),
                node_dict["depth"],
                node_dict["node_type"],
                node_dict["activation_type"])
            
        net.add_node(node)

    # Load the links
    for link_dict in net_dict["links"]:
        
        in_node_gid, out_node_gid, is_recur = link_dict["gid_tuple"]

        # Create the link
        in_node = net.nodes[in_node_gid]
        out_node = net.nodes[out_node_gid]
        link = Link(config, in_node, out_node, is_recur)
        
        # Load the link traits
        link.trait.weight = link_dict["weight"]
        link.trait.bias = link_dict["bias"]
        link.enabled = link_dict["enabled"]

        # Add the link to the network
        net.add_link(link)

    net.link_dict = _load_link_count_dict(net_dict["link_count_list"])

    # Create the organism
    org = Organism(config, net, gen=org_dict["generation"], id=org_dict["id"])
    if "best_fitness" in org_dict:
        org.best_fitness = org_dict["best_fitness"]

    if "avg_fitness" in org_dict:
        # Bit of a heuristic to assume avg_fitness is fitness sum
        org._num_updates = org_dict["num_updates"]
        org._fitness_avg = org_dict["avg_fitness"]

    return org

def _load_inv_counter_links(inv_link_list):
    link_dict = {}
    for inv_link in inv_link_list:
        link_dict[tuple(inv_link["gid_tuple"])] = inv_link["gid"]

    return link_dict


def load_population(config):
    # Load the population dictionary
    with open(config.save_file) as f:
        pop_dict = json.load(f)
    
    population = Population(config)
    
    # Load the invocation counter
    population.inv_counter.gid_counter = pop_dict["inv_dict"]["gid_counter"]
    population.inv_counter.link_dict = _load_inv_counter_links(
        pop_dict["inv_dict"]["inv_link_list"])

    population.cur_id = pop_dict["cur_id"]
    population.generation = pop_dict["generation"]

    # Create the base organism
    population.base_org = _load_organism(config, pop_dict["base_org"])

    # Load the organisms
    org_index = {} # Used to quickly retrieve organisms
    for org_dict in pop_dict["orgs"]:
        org = _load_organism(config, org_dict)
        population.orgs.append(org)
        org_index[org.id] = org

    # Load the species
    for species_dict in pop_dict["species_list"]:
        species = Species(config, species_dict["id"])
        species.age = species_dict["age"]

        # Add the organisms to the species

        for org_id in species_dict["org_ids"]:
            species.add(org_index[org_id])
        
        population.add_species(species)
    
    return population




    



# class SaveManager:
# #     """Manages saving and loading networks."""
