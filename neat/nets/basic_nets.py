from neat.network import Network
from neat.node import Node, OutNode
from neat.link import Link
from neat.util import NodeType, ActivationType

def build_basic_net(config, num_sensor, num_output, out_activation_type=ActivationType.SIGMOID):
    """Create a basic fully connected network."""
    net = Network(num_output)
    sensor_nodes = []
    # Create the sensor nodes
    for i in range(num_sensor):
        sensor_node = Node(i, 0, NodeType.SENSOR, ActivationType.IDENTITY)
        sensor_nodes.append(sensor_node)

        net.add_node(sensor_node)
    
    # Create the output nodes
    for i in range(num_output):
        cur_id = i+num_sensor
        out_node = OutNode(cur_id, 1, NodeType.OUT, out_activation_type, out_pos=i)
        net.add_node(out_node)

        # Add links between sensor and out nodes
        for sensor_node in sensor_nodes:
            link = Link(config, sensor_node, out_node)
            net.add_link(link)

    return net