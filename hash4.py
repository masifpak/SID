import itertools

stuff = [0,1]
for L in range(0, len(stuff)+1):
    for subset in itertools.combinations(stuff, L):
        print (subset)