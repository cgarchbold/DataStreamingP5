import math
import random
import matplotlib.pyplot as plt
'''
    This script implements a Virtual Bitmap Sketch for counting a fixed number of flows from multiple sources.
    To run this script:

    python vbitmap.py
'''
class VirtualBitmapSketch:
    def __init__(self, num_bits, num_v_bits):
        self.num_bits = num_bits
        self.num_v_bits = num_v_bits
        self.bitmap = [0] * num_bits
        self.hash_fns = random.sample(range(1, 100000000000000), num_v_bits)
        self.v_hash = 4019

    def update(self, flow_id, num_flows):
        id_parts = str(flow_id).split('.')
        flow_id_to_hash = int(id_parts[0] + id_parts[1] + id_parts[2] + id_parts[3])

        for _ in range(num_flows):

            element_id = random.randrange(1000000000)
            virtual_hash = (element_id % self.v_hash) % self.num_v_bits
            #From the virtual bitmap insert into physical bitmap
            p_hash_value = (flow_id_to_hash ^ self.hash_fns[virtual_hash]) % self.num_bits
            self.bitmap[p_hash_value] = 1
    

    def estimate_spread(self, flow_id):
        id_parts = str(flow_id).split('.')
        flow_id_to_hash = int(id_parts[0] + id_parts[1] + id_parts[2] + id_parts[3])

        v_bitmap = []
        for hash in self.hash_fns:
            v_bitmap.append(self.bitmap[(flow_id_to_hash ^ hash) % self.num_bits])
        
        if v_bitmap.count(0) == 0:
            virtual = 1 / self.num_v_bits
        else:
            virtual = v_bitmap.count(0) / self.num_v_bits
        physical = self.bitmap.count(0) / self.num_bits
            
        estimated_spread = self.num_v_bits * math.log(physical) - self.num_v_bits * math.log(virtual)
            
        return estimated_spread

if __name__ == '__main__':

    INPUT_FILE = "project5input.txt"
    NUM_BITS = 500000
    NUM_V_BITS = 500
    
    # Reading in flows
    flows = []
    with open(INPUT_FILE, "r") as f:
        for i, x in enumerate(f):
            if i == 0:
                num_flows = int(x)
            else:
                flow_id, curr_flow_count = x.split()
                curr_flow_count = int(curr_flow_count)
                flows.append((flow_id, curr_flow_count))

    vms = VirtualBitmapSketch(num_bits=NUM_BITS, num_v_bits=NUM_V_BITS)

    # Add flows to the sketch
    for flow_id, num_flows in flows:
        vms.update( flow_id, num_flows)
    
    # Estimate spreads
    estimated = []
    actual = []
    for flow_id, num_flows in flows:
        estimate = vms.estimate_spread(flow_id)
        actual.append(num_flows)
        estimated.append(estimate)
        
    #Plot graph using matplotlib
    plt.scatter(actual, estimated, color='blue', marker = '+', s = 20)
    plt.plot([0, 500], [0, 500], color='red', linestyle='--')
    plt.xlim([0, 500])
    plt.ylim([0, 700])
    plt.xlabel("actual spread", fontsize=15)
    plt.ylabel("estimated spread", fontsize=15)
    plt.savefig("flow_spread.png")
    plt.close()

    #Write results to file
    with open("vbitmap.txt", "w") as file:
        for i, est in enumerate(estimated): 
            file.write(f"Actual: {actual[i]:<5} Estimated {est:<5} \n")