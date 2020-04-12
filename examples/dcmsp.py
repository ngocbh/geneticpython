import geneticpython

# read input
n, m = (0, 0)
edges = []
with open('in.txt',mode='r') as f:
    n, m = list(map(int, f.readline().split()))
    for line in f.readlines():
        u, v, c = list(map(int, line.split()))
        edges.append((u,v,c))


