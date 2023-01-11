import numpy as np

class FinalStateNovelty:
    """Measures the novelty-based on the final state of an organism.""" 
    def __init__(self, args):
        self.args = args
        # List of novel final states 
        self.novel_archive = []

    def novelty(self, final_states: list):
        avg_dists = []
        for i, final_state in enumerate(final_states):
            state_dists = []
            for state in self.novel_archive + final_states[:i] + final_states[i+1:]:
                state_dists.append(self._dist(final_state, state))
            
            state_dists.sort()
            neighbor_dists = state_dists[:self.args.novelty_neighbors]
            avg_dist = sum(neighbor_dists) / len(neighbor_dists)
            self._attempt_add_queue(final_state, avg_dist)
            avg_dists.append(avg_dist)
        
        return avg_dists

    def avg_dist(self, final_state):
        if len(self.novel_archive) > 0:
            
            state_dists = []
            for state in self.novel_archive:
                state_dists.append(self._dist(final_state, state))
            
            state_dists.sort()
            neighbor_dists = state_dists[:self.args.novelty_neighbors]
            avg_dist = sum(neighbor_dists) / len(neighbor_dists)
            self._attempt_add_queue(final_state, avg_dist)
            #print("avg_dist", len(self.novel_archive), avg_dist)
            return avg_dist
        else:
            # The novel_archive has not been populated yet, so I guess just use the threshold?
            self.novel_archive.append(final_state)
            return self.args.novelty_threshold    
    
    def _attempt_add_queue(self, final_state, avg_dist):
        if avg_dist >= self.args.novelty_threshold:
            self.novel_archive.append(final_state)
            if len(self.novel_archive) >= self.args.novelty_queue_size:
                self.novel_archive = self.novel_archive[:self.args.novelty_queue_size] 


    def _dist(self, state_1, state_2):
        sum_sd = 0
        # Take the squared difference between all the elements in the state
        for i in range(len(state_1)):
            sum_sd += (state_1[i] - state_2[i]) ** 2
        
        # Return the L2 distance
        return sum_sd ** 0.5