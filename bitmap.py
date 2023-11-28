import math
import random
'''
    This script implements a bitmap sketch for single-flow spread estimation
'''
class BitmapSketch:
    def __init__(self, num_bits):
        self.num_bits = num_bits
        self.bitmap = [0] * num_bits
        self.hash_fn = 11 # We will choose a prime number here

    def reset_bitmap(self):
        self.bitmap = [0] * self.num_bits

    def record_flow(self, flow_id):
        hash_value = (flow_id * self.hash_fn) % self.num_bits
        self.bitmap[hash_value] = 1

    def estimate_spread(self):
        num_zeros = self.bitmap.count(0)

        percent_zeros = num_zeros/len(self.bitmap)

        if percent_zeros == 0:
            percent_zeros = 1/len(self.bitmap)

        estimated_spread = -len(self.bitmap)*math.log2(percent_zeros)
        return estimated_spread

if __name__ == '__main__':
    # Set the number of bits in the bitmap
    num_bits = 10000

    bitmap_sketch = BitmapSketch(num_bits)

    # List of flow spreads
    flow_spreads = [100, 1000, 10000, 100000, 1000000]

    flow_arrays = []
    for flow_spread in flow_spreads:
        flows = []
        for index in range(flow_spread):
            element_id = random.randrange(1000000000)
            flows.append(element_id)

        flow_arrays.append(flows)

    # Record flows and estimate spread for each flo
    estimated_spreads = []
    for i,flows in enumerate(flow_arrays):
        for flow in flows:
            bitmap_sketch.record_flow(flow)
        true_spread = flow_spreads[i]
        estimated_spread = bitmap_sketch.estimate_spread()
        bitmap_sketch.reset_bitmap()
        estimated_spreads.append(estimated_spread)

    #Write to file
    with open("bitmap.txt", "w") as file:
        for i,spread in enumerate(flow_spreads):
            file.write(f"{spread} {estimated_spreads[i]} \n")