from itertools import permutations
D='0123456789'
As=[p for p in permutations(D,3) if p[0]!='0']
Bs=[p for p in permutations(D,4) if p[0]!='0']
count=0
for a in As:
 aset=set(a)
 count+=sum(len(aset.intersection(b))<=1 for b in Bs)
print(len(As),len(Bs),count,len(As)*len(Bs))
from fractions import Fraction
print(Fraction(count,len(As)*len(Bs)))
