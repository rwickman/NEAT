
class InvocationCounter:
    """Keeps track of GID of nodes across all networks."""
    def __init__(self):
        self.gid_counter = 0
        self.link_dict = {} # Contains GIDs for in to out
    
    def get_GID(self, old_in_gid, old_out_gid, count):
        """Get GID based on old in_node GID and old out_node GID.
        ARGS:
            old_in_gid: GID of old incoming node
            old_out_node: GID of outgoing node
            count: the number of times this type of node has been added between these two nodes
        """
        gid_tuple = (old_in_gid, old_out_gid, count)
        if gid_tuple in self.link_dict:
            # A node has already been added between these links, so increase counter
            return self.link_dict[gid_tuple]
        else:
            
            # A node must have not been added between these nodes before 
            # Set the GID to return
            new_node_gid = self.gid_counter
            
            # Increment the GID counter
            self.gid_counter += 1
            
            # Add GID to dict
            self.link_dict[gid_tuple] = new_node_gid

            return new_node_gid
        