'''
common.py

Commonly used Variables and simple expressions involving them.
'''

from proveit.expression import Variable, Operation
from proveit.multiExpression import Etcetera

a = Variable('a')
b = Variable('b')
c = Variable('c')
A = Variable('A')
B = Variable('B')
C = Variable('C')
P = Variable('P')
Q = Variable('Q')
R = Variable('R')
S = Variable('S')
X = Variable('X') 
f = Variable('f')
g = Variable('g')
x = Variable('x')
y = Variable('y')
z = Variable('z')

PofA = Operation(P, A) # P(A)
Px = Operation(P, x) # P(x)
Py = Operation(P, y) # P(y)
Pxy = Operation(P, (x, y)) # P(x, y)
Qx = Operation(Q, x) # Q(x)
Qy = Operation(Q, y) # Q(x)
Ry = Operation(R, y) # R(y)
fa = Operation(f, a) # f(a)
fb = Operation(f, b) # f(b)
fab = Operation(f, (a, b)) # f(a, b)
fx = Operation(f, x) # f(x)
fy = Operation(f, y) # f(y)
fxy = Operation(f, (x, y)) # f(x, y)
gx = Operation(g, x) # g(x)
gy = Operation(g, y) # g(y)

Aetc = Etcetera(A) # ..A..
Cetc = Etcetera(C) # ..C..
Qetc = Etcetera(Q) # ..Q..
Retc = Etcetera(R) # ..R..
xEtc = Etcetera(x) # ..x..
yEtc = Etcetera(y) # ..y..
zEtc = Etcetera(z) # ..z..
PxEtc = Operation(P, xEtc) # P(..x..)
PyEtc = Operation(P, yEtc) # P(..y..)
PxyEtc = Operation(P, (xEtc, yEtc)) # P(..x.., ..y..)
etc_QxEtc = Etcetera(Operation(Q, xEtc)) # ..Q(..x..)..
etc_QyEtc = Etcetera(Operation(Q, yEtc)) # ..Q(..y..)..
etc_RyEtc = Etcetera(Operation(R, yEtc)) # ..R(..y..)..