import math
from functools import reduce
from numpy import arange

def Q_exp(n):
    def product(i):
        return mu + i/teta
    products = [product(i) for i in range(n+1)]
    return math.factorial(n) / reduce(lambda x, y: x*y, products)

def Q_fixed(n):
    def sum(i):
        return (mu*teta)**i / math.factorial(i)

    sums = [sum(i) for i in range(n)]
    sums = reduce(lambda x, y:x+y, sums)

    return math.factorial(n) * (1 - math.e**(-1*mu*teta)*sums) / mu**(n+1)

def X(i, landa):
    if i == 1:
        return landa / mu
    elif i > 1:
        return (landa**i)*Q(i-1)/math.factorial(i-1)


def Q(n):
    if type == 'fixed':
        return Q_fixed(n)
    else:
        return Q_exp(n)


with open('parameters.conf', 'r') as f:
    teta = int(f.readline())
    mu = int(f.readline())

types = ['fixed', 'exp']
landas = [i for i in arange(0.1, 20.1, 0.1)]
for type in types:
    string = ''
    for landa in landas:
        Xs = [X(i, landa) for i in range(1, 13)]
        P0 = 1 / (1 + reduce(lambda x, y:x+y, Xs))
        pb = Xs[-1] * P0
        pd = 1 - mu*(1-P0)/landa - pb
        string += str(landa) + '\t' + str(pd) + '\t' + str(pb) +'\n'
    print(type)
    print(string)
