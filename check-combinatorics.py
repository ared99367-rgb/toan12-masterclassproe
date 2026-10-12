from itertools import combinations
n=20
cnt=[0]*5
for C in combinations(range(n),4):
 e=sum((b-a==1) for a,b in zip(C,C[1:])) + (C[0]==0 and C[-1]==n-1)
 cnt[e]+=1
print('boundary_edges_distribution',cnt,'no_side',cnt[0], 'prob',cnt[0],'/4845')
