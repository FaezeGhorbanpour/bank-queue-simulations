import math
from functools import reduce
from numpy import arange


def y_exp(n):
    if n == 0:
        return 0
    elif n > 0:
        return n / teta


def y_fixed(n):
    if n == 0:
        return 0
    else:
        return mu / ((math.e ** (mu * teta / n)) - 1)


def P(n, land, typ):
    def denominator(i):
        if typ == 'fixed':
            return mu + y_fixed(i)
        else:
            return mu + y_exp(i)
    if n >= 1:
        denominators = [denominator(i) for i in range(1, n + 1)]
        return (land ** n) / reduce(lambda x, y: x * y, denominators)
    else:
        print('Error')

def P0(k, land, typ):
    equation = [P(i, land, typ) for i in range(1, k + 1)]
    equation_sum = reduce(lambda x, y: x + y, equation)
    return (1 + equation_sum) ** -1


with open('parameters.conf', 'r') as f:
    teta = int(f.readline())
    mu = int(f.readline())
k = 12
types = ['fixed', 'exp']
landas = [i for i in arange(0.1, 20.1, 0.1)]
print('fixed')
string = ''
for landa in landas:
    pb = P0(k, landa, 'fixed') * P(k, landa, 'fixed')
    pd = 1 - mu * (1 - P0(k, landa, 'fixed')) / landa - pb
    string += str(landa) + '\t' + str(pd) + '\t' + str(pb) + '\n'
with open('PS_fixed_t.txt', 'w') as f:
    f.write(string)
print(string)
print('exp')
string = ''
for landa in landas:
    pb = P0(k, landa, 'exp') * P(k, landa, 'exp')
    pd = 1 - mu * (1 - P0(k, landa, 'exp')) / landa - pb
    string += str(landa) + '\t' + str(pd) + '\t' + str(pb) + '\n'
with open('PS_exp_t.txt', 'w') as f:
    f.write(string)
print(string)