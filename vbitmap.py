import math
import random
'''
    This script implements a 
'''
class VirtualBitmapSketch:
    def __init__(self, num_bits, num_v_bits, num_flows):
        self.num_bits = num_bits
        self.bitmap = [0] * num_bits
        self.virtual_bitmaps = [[0] * num_v_bits for _ in range(num_flows)]
        self.hash_fns = random.sample(range(1, 1000000000), num_v_bits)

    # Update the physical bitmap according to the flow_id
    # Update the virtual bitmap by recording unique(random) flows
    def update(self, flow_id, num_flows):
        id_parts = str(flow_id).split('.')
        flow_id_to_hash = int(id_parts[0] + id_parts[1] + id_parts[2] + id_parts[3])

        for _ in range(num_flows):
            element_id = random.randrange(1000000000)
            hash_index = 
    
    #Estimates the spread of each flow using formula:
    #   n_f = l*ln(V_b) - l*ln(V_f)
    def estimate_spread(self, flow_id):
        id_parts = str(flow_id).split('.')
        flow_id_to_hash = int(id_parts[0] + id_parts[1] + id_parts[2] + id_parts[3])
        
        return estimated_spread

if __name__ == '__main__':

    num_bits = 500000
    num_v_bits = 500
    
    # Reading in flows
    flows = []
    with open("project3input.txt", "r") as f:
        for i, x in enumerate(f):
            if i == 0:
                num_flows = int(x)
            else:
                flow_id, curr_flow_count = x.split()
                curr_flow_count = int(curr_flow_count)
                flows.append((flow_id, curr_flow_count))

    vms = VirtualBitmapSketch(num_bits=num_bits, num_v_bits=num_v_bits)

    for flow_id, num_flows in flows:
        vms.update(flow_id, num_flows)

    #Write to file
    with open("bitmap.txt", "w") as file:
        for i,spread in enumerate(flow_spreads):
            file.write(f"{spread} {estimated_spreads[i]} \n")