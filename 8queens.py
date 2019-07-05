# (c) imreszakal.com

from ortools.sat.python import cp_model
import time
d
import numpy as np
from matplotlib import pyplot as plt

start = time.time()
table_size = 8
model = cp_model.CpModel()

queen = {}
horizontal = [i for i in range(table_size)]
vertical = [j for j in range(table_size)]
for i in horizontal:
    for j in vertical:
        n = 'queen_{}.{}'.format(i,j)
        queen[(i,j)] = model.NewBoolVar(n)

cover = {}
for i in horizontal:
    for j in vertical:
        d1 = [[i+k,j+k] for k in range(-7, 8) if
                (i+k>=0 and i+k<=7 and j+k>=0 and j+k<=7)]
        d1.remove([i,j])
        d2 = [[i+k,j-k] for k in range(-7, 8) if
                (i+k>=0 and i+k<=7 and j-k>=0 and j-k<=7)]
        d2.remove([i,j])
        d = d1 + d2

        h = [[i,k] for k in vertical]
        v = [[l,j] for l in horizontal]
        hv = h + v
        hv.remove([i,j])
        hv.remove([i,j])

        cover[(i,j)] = d + hv # [i,j] is not in it

for i in horizontal:
    for j in vertical:
        for k in cover[(i,j)]:
            model.Add(queen[(i,j)] + queen[(k[0],k[1])] <= 1)

model.Maximize(sum(queen[(i,j)] for i in horizontal for j in vertical))

solver = cp_model.CpSolver()
solver.Solve(model)

print()
end = time.time()
print('Time:')
print('{:.8f} seconds'.format(end - start))
print()
print('Result:')
result = []
for i in horizontal:
    for j in vertical:
        if solver.Value(queen[(i,j)]) == 1:
            result.append([i,j])
print(result)

data = np.array(result)
x, y = data.T
plt.scatter(x,y)
plt.show()

print('......................................................................................................................................................')
