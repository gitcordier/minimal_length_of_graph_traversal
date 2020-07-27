import sys
from operator import itemgetter
from math import sqrt, inf


# Reads the input: First line for N, any other one for a node.
# The nodes list is "y-sorted", i.e. 
# y of node i is smaller than y of node j (i < j).
N = int(sys.stdin.readline())

def parse_input(line):
    a = str(line).split(' ')
    return [float(x) for x in a]

node_ = sorted(map(parse_input, sys.stdin), key=itemgetter(1))

def compute_edge_costs(cost_function):
    return [
        [cost_function(node_[i], node_[j]) for i in range(j)] 
        for j in range(0, N)
    ]

def Euclidian_distance(a, b):
    """
        Input:  Two vectors a = [x, y, z], b = [x', y', z'].
        Output: The euclidian norm |a-b|.
    """
    return sqrt(sum(pow(b[i]-a[i], 2) for i in (0, 1, 2)))

cost_ = compute_edge_costs(Euclidian_distance)

def cost(i, j):
    if i < j :
        return cost_[j][i]
    elif i > j:
        return cost_[i][j]
    else:
        return 0
    
# s(k) := d(k, k+1) + ... + d(N-2, N-1)    (k=0, 1, …, N-1)
#       = d(k, k+1) + s(k+1)
s = [0]*N
for k in range(N-2, -1, -1):
    s[k] = cost(k, k+1) + s[k+1] 

# 'csum' for 'cumulative sum'
# We first define csum(k, m) with k < m:
# csum(k, m) := cost(k, k+1) + ... + cost(m-1, m)
#             = cost(k, k+1) + ... + cost(m-1, m) + csum(m, N-1) - csum(m, N-1)
#             = csum(k, N-1) - csum(m, N-1)
#             = s(k) - s(m)
# Next we extend the definition, as follows: 
# csum(k, m) = abs(s[k] - s[m]) 
def cumulative_cost(m, n):
    if m == n:
        return 0 
    else:
        return abs(s[m] - s[n])
    

def compute_min():
    """
        Puts everything together and so compute the desired min.
    """
    min_ = [inf] * (N-2)
    
# k = 0
    min_[0] = cost(0, 1)
    minimal_cost_0 = min_[0] + cost(0, N-1) + cumulative_cost(N-1, 1)

# k = 1
    min_[1]        = min_[0] + cost(0, 2)
    minimal_cost_1 = min_[1] + cost(1, N-1) + cumulative_cost(N-1, 2)
    
# So, for now, 
    minimal_cost = min(minimal_cost_0, minimal_cost_1)

# k = 2, 3, ..., N-3 (N > 4)
    for k in range(2, N-2): 
        min_k_regular = min(
            sum((
                    min_[j], 
                    cost(j, k), 
                    cost(k+1, k-1), 
                    cumulative_cost(k-1, j+1)
                ))
            for j in range(k-1)
        )
        #j = k-1
        min_k_special = min(
            sum((
                    min_[i],
                    cumulative_cost(i+1, k-1), 
                    cost(k-1, k),
                    cost(k+1, i)
                 ))
            for i in range(k-1)
        )
        #
        min_[k] = min(min_k_regular, min_k_special)
        #
        if min_[k] < minimal_cost:
            minimal_cost_k = min_[k] + cost(k, N-1) + cumulative_cost(N-1, k+1)
            minimal_cost   = min(minimal_cost, minimal_cost_k)
    #
    return minimal_cost
#
 
print(int(compute_min()))

# END

