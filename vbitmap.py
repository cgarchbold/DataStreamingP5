import math
import random
import matplotlib.pyplot as plt
'''
    This script implements a 
'''
class VirtualBitmapSketch:
    def __init__(self, num_bits, num_v_bits, num_flows):
        self.num_bits = num_bits
        self.num_v_bits = num_v_bits
        self.bitmap = [0] * num_bits
        self.virtual_bitmaps = [[0] * num_v_bits for _ in range(num_flows)]
        self.hash_fn = 37 #We will choose a prime number for our hash function

    # Update the physical bitmap according to the flow_id
    # Update the virtual bitmap by recording unique(random) flows
    def update(self, flow_index, flow_id, num_flows):
        id_parts = str(flow_id).split('.')
        flow_id_to_hash = int(id_parts[0] + id_parts[1] + id_parts[2] + id_parts[3])

        for _ in range(num_flows):
            element_id = random.randrange(1000000000)
            v_hash_value = (element_id * self.hash_fn) % self.num_v_bits
            #insert into the virtual bitmap
            self.virtual_bitmaps[flow_index][v_hash_value] = 1
            
            #From the virtual bitmap insert into physical bitmap
            p_hash_value = (flow_id_to_hash * self.hash_fn) % self.num_bits
            self.bitmap[p_hash_value] = 1
    
    #Estimates the spread of each flow using formula:
    #   n_f = l*ln(V_b) - l*ln(V_f)
    #       l = Virtual bitmap length
    #       V_b and V_f = percent of zeros in physical and virtual bitmap respectively
    def estimate_spread(self, flow_index):
        physical_bitmap_percent_zeroes = self.bitmap.count(0) / self.num_bits
        
        if self.virtual_bitmaps[flow_index].count(0) != 0:
            virtual_bitmap_percent_zeroes = self.virtual_bitmaps[flow_index].count(0) / self.num_v_bits
        else:
            virtual_bitmap_percent_zeroes = 1 / self.num_v_bits
            
        estimated_spread = self.num_v_bits * math.log(physical_bitmap_percent_zeroes) - self.num_v_bits * math.log(virtual_bitmap_percent_zeroes)
            
        return estimated_spread

if __name__ == '__main__':

    NUM_BITS = 500000
    NUM_V_BITS = 500
    
    # Reading in flows
    flows = []
    with open("project5input.txt", "r") as f:
        for i, x in enumerate(f):
            if i == 0:
                num_flows = int(x)
            else:
                flow_id, curr_flow_count = x.split()
                curr_flow_count = int(curr_flow_count)
                flows.append((flow_id, curr_flow_count))

    vms = VirtualBitmapSketch(num_bits=NUM_BITS, num_v_bits=NUM_V_BITS, num_flows=num_flows)

    index = 0
    for flow_id, num_flows in flows:
        vms.update(index, flow_id, num_flows)
        index+=1
        
    estimated = []
    actual = []
    index = 0
    for flow_id, num_flows in flows:
        val = vms.estimate_spread(index)
        actual.append(num_flows)
        estimated.append(val)
        index+=1
        
    #Plot graph using matplotlib
    plt.scatter(actual, estimated, color='blue', marker = '+', s = 20)
    plt.xlim([0, 500])
    plt.ylim([0, 700])
    plt.xlabel("actual spread", fontsize=15)
    plt.ylabel("estimated spread", fontsize=15)
    plt.savefig("flow_spread.png")
    plt.close()

    #Write to file
    #with open("bitmap.txt", "w") as file:
    #    for i,spread in enumerate(flow_spreads):
    #        file.write(f"{spread} {estimated_spreads[i]} \n")