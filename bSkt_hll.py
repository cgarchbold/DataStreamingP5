import random
import matplotlib.pyplot as plt

'''
    This script implements a HLL Bitmap Sketch for counting a fixed number of flows from multiple sources.
    To run this script:

    $ python bSkt_hll.py
'''
class HyperLogLog:

    def __init__(self, num_registers):
        self.num_registers = num_registers
        self.registers = [0] * num_registers
        self.hash_fn1 = random.randint(100000000,10000000000)
        self.hash_fn2 = 4019

    def reset_registers(self):
        """
        Construct a new 'Foo' object.

        :param name: The name of foo
        :param age: The ageof foo
        :return: returns nothing
        """
        self.registers = [0] * self.num_registers

    def geometric_hash(self, id):
        # Obtaining binary input and removing '0b'
        binary = bin(id)[2:]
    
        # Count zeroes
        g = 32 - len(binary) # max 32 bits

        return g

    def record_flow(self, flow_id):
        hash_value = (flow_id ^ self.hash_fn1) % self.num_registers
        hash_value2 = (flow_id * self.hash_fn2) % (2**32)

        g_prime = self.geometric_hash(hash_value2) + 1

        self.registers[hash_value] = max(self.registers[hash_value], g_prime) % 32 # 5 bits long

    def estimate_spread(self):
        estimated_flow_spread = 0
        alpha = 0.7213/(1 + 1.079/self.num_registers)

        # Calculating estimated flow using harmonic mean
        for register_value in self.registers:
            estimated_flow_spread += 1/(2 ** register_value)
        estimated_flow_spread = estimated_flow_spread ** -1
        estimated_flow_spread = estimated_flow_spread * (self.num_registers ** 2) * alpha

        return estimated_flow_spread
    
class HLLBitmapSketch:
    def __init__(self, num_hll, num_hashes, num_registers):
        self.num_hll = num_hll
        self.hash_fns = random.sample(range(100000000, 10000000000), num_hashes)
        self.hlls = [HyperLogLog(num_registers=num_registers) for _ in range(num_hll)]

    def update(self, flow_id, num_flows):
        id_parts = str(flow_id).split('.')
        flow_id_to_hash = int(id_parts[0] + id_parts[1] + id_parts[2] + id_parts[3])

        for _ in range(num_flows):
            element_id = random.randrange(1000000000)
            for hash in self.hash_fns:
                hash_value = (flow_id_to_hash ^ hash) % self.num_hll
                self.hlls[hash_value].record_flow(element_id)
            
    
    def estimate_spread(self, flow_id):
        id_parts = str(flow_id).split('.')
        flow_id_to_hash = int(id_parts[0] + id_parts[1] + id_parts[2] + id_parts[3])
        
        estimated_spreads = []
        for hash in self.hash_fns:
            hash_value = (flow_id_to_hash ^ hash) % self.num_hll
            estimated_spreads.append(self.hlls[hash_value].estimate_spread())

        return min(estimated_spreads)

if __name__ == '__main__':

    NUM_HLL = 4000
    NUM_HASHES = 3
    NUM_REGISTERS = 128
    INPUT_FILE = "project5input.txt"
    
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
    
    #Initialize and fill
    bskt_hll = HLLBitmapSketch(num_hll=NUM_HLL,num_hashes=NUM_HASHES,num_registers=NUM_REGISTERS)

    index = 0
    for i, (flow_id, num_flows) in enumerate(flows):
        bskt_hll.update(flow_id,num_flows)
        index+=1
        
    estimated = []
    actual = []
    index = 0
    for flow_id, num_flows in flows:
        val = bskt_hll.estimate_spread(flow_id)
        actual.append(num_flows)
        estimated.append(val)
        index+=1

    sorted_estimates = sorted(zip(estimated, actual), key=lambda x: x[0], reverse=True)

    with open("bSKt_hll.txt", "w") as file:
        file.write("Top 25 Estimates:\n")
        for i, (est, act) in enumerate(sorted_estimates[:25]):
            file.write(f"Rank {i+1:<3} Actual: {act:<5} Estimated: {est:<5} \n")