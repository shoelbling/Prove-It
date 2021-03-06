from proveit import Etcetera
from proveit.logic import Forall, InSet, Equals, NotEquals
from proveit.number import Integers, Naturals, NaturalsPos, Reals, RealsPos, Complexes
from proveit.number import Exp, sqrt, Add, Mult, Sub, Neg, frac, Abs, GreaterThan, GreaterThanEquals, LessThan, LessThanEquals
from proveit.common import a, b, c, d, n, x, y, z, xEtc, xMulti
from proveit.number.common import zero, one, two
from proveit import beginTheorems, endTheorems

beginTheorems(locals())

# transferred & updated 2/20/2020
expNatClosure = Forall((a, b), InSet(Exp(a, b), NaturalsPos), domain=Naturals, conditions=[NotEquals(a, zero)])
expNatClosure

# transferred & updated 2/20/2020
expRealClosure = Forall([a, b], InSet(Exp(a, b), Reals), domain=Reals,
                       conditions=[GreaterThanEquals(a, zero), GreaterThan(b, zero)])
expRealClosure

# transferred & updated 2/20/2020
expRealPosClosure = Forall([a, b], InSet(Exp(a, b), RealsPos), domain=Reals,
                       conditions=[GreaterThan(a, zero)])
expRealPosClosure

# transferred & updated 2/20/2020
expComplexClosure = Forall([a, b], InSet(Exp(a, b), Complexes), domain=Complexes,
                    conditions=[NotEquals(a, zero)])
expComplexClosure

sqrtRealClosure = Forall([a], InSet(sqrt(a), Reals), domain=Reals,
                         conditions=[GreaterThanEquals(a, zero)])
sqrtRealClosure

sqrtRealPosClosure = Forall([a], InSet(sqrt(a), RealsPos), domain=RealsPos)
sqrtRealPosClosure

sqrtComplexClosure = Forall([a], InSet(sqrt(a), Complexes), domain=Complexes)
sqrtComplexClosure

# Should generalize to even power closure, but need to define and implement evens set to do this.

# transferred & updated 2/20/2020
sqrdPosClosure = Forall(a, InSet(Exp(a, two), RealsPos),
                        domain=Reals, conditions=[NotEquals(a, zero)])
sqrdPosClosure

# transferred & updated 2/20/2020
squarePosIneq = Forall([a,b],
                        LessThanEquals(Exp(Abs(a),two),Exp(b,two)),
                        domain = Reals,
                        conditions = (LessThanEquals(Abs(a),b),))
squarePosIneq

# transferred & updated 2/20/2020
squarePosEq = Forall(a,
                     Equals(Exp(Abs(a),two),Exp(a,two)),
                     domain = Reals)
squarePosEq

# transferred & updated 2/20/2020
expNotEqZero = Forall([a, b], NotEquals(Exp(a,b), zero), domain=Complexes, conditions=[NotEquals(a, zero)])
expNotEqZero

# already present in new _theorems_
expZeroEqOne = Forall([a], Equals(Exp(a, zero), one), domain=Complexes, conditions=[NotEquals(a, zero)])
expZeroEqOne

# already present in new _theorems_
exponentiatedZero = Forall([x], Equals(Exp(zero, x), zero), domain=Complexes, conditions=[NotEquals(x, zero)])
exponentiatedZero

# already present in new _theorems_
exponentiatedOne = Forall([x], Equals(Exp(one, x), one), domain=Complexes)
exponentiatedOne

# transferred & updated 2/20/2020
sumInExp = Forall([a,b,c],
                Equals(Exp(a,Add(b,c)),
                       Mult(Exp(a,b),Exp(a,c))),
                domain = Complexes, conditions=[NotEquals(a, zero)])
sumInExp

# transferred & updated 2/20/2020
# probably don't need both this and previous thm?
sumInExpRev = Forall([a,b,c],
                Equals(Mult(Exp(a,b),Exp(a,c)),
                       Exp(a,Add(b,c))),
                domain = Complexes, conditions=[NotEquals(a, zero)])
sumInExpRev

# transferred & updated 2/20/2020
addOneRightInExp = Forall([a,b],
                Equals(Exp(a,Add(b,one)),
                       Mult(Exp(a,b),a)),
                domain = Complexes, conditions=[NotEquals(a, zero)])
addOneRightInExp

# transferred & updated 2/20/2020
# probably don't need both this and previous thm?
addOneRightInExpRev = Forall([a,b],
                Equals(Mult(Exp(a,b),a),
                       Exp(a,Add(b,one))),
                domain = Complexes, conditions=[NotEquals(a, zero)])
addOneRightInExpRev

# transferred & updated 2/20/2020
addOneLeftInExp = Forall([a,b],
                Equals(Exp(a,Add(one, b)),
                       Mult(a, Exp(a,b))),
                domain = Complexes, conditions=[NotEquals(a, zero)])
addOneLeftInExp

# transferred & updated 2/20/2020
# probably don't need both this and previous thm?
addOneLeftInExpRev = Forall([a,b],
                Equals(Mult(a, Exp(a,b)),
                       Exp(a,Add(one, b))),
                domain = Complexes, conditions=[NotEquals(a, zero)])
addOneLeftInExpRev

# transferred & updated 2/20/2020
diffInExp = Forall([a,b,c],
                Equals(Exp(a,Sub(b,c)),
                       Mult(Exp(a,b),Exp(a,Neg(c)))),
                domain = Complexes, conditions=[NotEquals(a, zero)])
diffInExp

# transferred & updated 2/20/2020
# probably don't need both this and previous thm?
diffInExpRev = Forall([a,b,c],
                Equals(Mult(Exp(a,b),Exp(a,Neg(c))),
                       Exp(a,Sub(b,c))),
                domain = Complexes, conditions=[NotEquals(a, zero)])
diffInExpRev

# transferred & updated 2/20/2020
diffFracInExp = Forall([a,b,c,d],
                Equals(Exp(a,Sub(b,frac(c, d))),
                       Mult(Exp(a,b),Exp(a,frac(Neg(c), d)))),
                domain = Complexes, conditions=[NotEquals(a, zero), NotEquals(d, zero)])
diffFracInExp

# transferred & updated 2/20/2020
# probably don't need both this and previous thm?
diffFracInExpRev = Forall([a,b,c,d],
                Equals(Mult(Exp(a,b),Exp(a,frac(Neg(c), d))),
                       Exp(a,Sub(b,frac(c, d)))),
                domain = Complexes, conditions=[NotEquals(a, zero), NotEquals(d, zero)])
diffFracInExpRev

# transferred & updated 2/20/2020
# prompting a grouping error, though, that needs addressed
# works because log[a^c b^c] = c log a + c log b
expOfPositivesProd = Forall(c, Forall((a, b),
                             Equals(Exp(Mult(a,b),c),
                                    Mult(Exp(a,c),Exp(b,c))),
                             domain=RealsPos),
                domain=Complexes)
expOfPositivesProd

# transferred & updated 2/20/2020
# prompting a grouping error, though, that needs addressed
# probably don't need both this and previous thm?
expOfPositivesProdRev = Forall(c, Forall((a, b),
                             Equals(Mult(Exp(a,c),Exp(b,c)),
                                   Exp(Mult(a,b),c)),
                             domain=RealsPos),
                domain=Complexes)
expOfPositivesProdRev

# transferred & updated 2/20/2020
# prompting a grouping error, though, that needs addressed
# Works for integers powers by the commutivity of complex numbers (or their inverses when n < 0).
# Does not work for fractional powers.  Consider sqrt(-1)*sqrt(-1) = -1 not sqrt((-1)*(-1)) = 1.
intExpOfProd = Forall(n, Forall((a, b),
                                Equals(Exp(Mult(a,b),n),
                                       Mult(Exp(a,n),Exp(b,n))),
                                domain=Complexes, conditions=[NotEquals(a, zero), NotEquals(b, zero)]),
                      domain=Integers)
intExpOfProd

# transferred & updated 2/20/2020
# prompting a grouping error, though, that needs addressed
# probably don't need both this and previous thm?
intExpOfProdRev = Forall(n, Forall((a, b),
                                   Equals(Mult(Exp(a,n),Exp(b,n)),
                                          Exp(Mult(a,b),n)),
                                   domain=Complexes, conditions=[NotEquals(a, zero), NotEquals(b, zero)]),
                         domain=Integers)
intExpOfProdRev

# transferred 2/20/2020
natsPosExpOfProd = Forall(n, Forall((a, b),
                                    Equals(Exp(Mult(a,b),n),
                                           Mult(Exp(a,n),Exp(b,n))),
                                    domain=Complexes),
                          domain=NaturalsPos)
natsPosExpOfProd

# omitted from transfer (essentially duplicates above) 2/20/2020
natsPosExpOfProdRev = Forall(n, Forall((a, b),
                                       Equals(Mult(Exp(a,n),Exp(b,n)),
                                              Exp(Mult(a,b),n)),
                                       domain=Complexes),
                             domain=NaturalsPos)
natsPosExpOfProdRev

# transferred 2/20/2020
# Works for integers powers through repetition of a^b (or a^{-b}) and adding exponents.
# Does not work for fractional powers.  Consider sqrt[(-1)^2] = 1 not (-1)^{2*(1/2)} = -1.
intExpOfExp = Forall(n, Forall((a, b),
                            Equals(Exp(Exp(a, b), n),
                                   Exp(a, Mult(b, n))),
                            domain=Complexes, conditions=[NotEquals(a, zero)]),
                  domain=Integers)
intExpOfExp

# transferred 2/20/2020
intExpOfNegExp = Forall(n, Forall((a, b),
                               Equals(Exp(Exp(a, Neg(b)), n),
                                      Exp(a, Neg(Mult(b, n)))),
                               domain=Complexes, conditions=[NotEquals(a, zero)]),
                        domain=Integers)
intExpOfNegExp

# transferred 2/20/2020
negIntExpOfExp = Forall(n, Forall((a, b),
                            Equals(Exp(Exp(a, b), Neg(n)),
                                   Exp(a, Neg(Mult(b, n)))),
                               domain=Complexes, conditions=[NotEquals(a, zero)]),
                        domain=Integers)

negIntExpOfExp

# transferred 2/20/2020
negIntExpOfNegExp = Forall(n, Forall((a, b),
                                     Equals(Exp(Exp(a, Neg(b)), Neg(n)),
                                            Exp(a, Mult(b, n))),
                               domain=Complexes, conditions=[NotEquals(a, zero)]),
                           domain=Integers)

negIntExpOfNegExp

# transferred 2/20/2020
diffSquareComm = Forall([a,b],
                        Equals(
                            Exp(Sub(a,b),two),
                            Exp(Sub(b,a),two)),
                        domain = Complexes)
diffSquareComm

# transferred 2/20/2020
oneExp = Forall([x],
               Equals(Exp(x,one),
                      x),
               domain = Complexes)
oneExp

# already transferred
expOne = Forall([x],
               Equals(Exp(one,x),
                     one),
               domain = Complexes)
expOne

# transferred 2/20/2020
sameExpDistribute = Forall([x,y,z],
                            Equals(Mult(Exp(x,y),Exp(z,y)),
                                 Exp(Mult(x,z),y)),
                            domain = Complexes)
sameExpDistribute

# transferred 2/20/2020
sqrtOfProd = Forall(xEtc, Equals(sqrt(Mult(xEtc)),
                              Mult(Etcetera(sqrt(xMulti)))),
                  domain=RealsPos)
sqrtOfProd

# transferred 2/20/2020
prodOfSqrts = Forall(xEtc, Equals(Mult(Etcetera(sqrt(xMulti))),
                                  sqrt(Mult(xEtc))),
                     domain=RealsPos)
prodOfSqrts

# transferred 2/20/2020
sqrtTimesItself = Forall(x, Equals(Mult(sqrt(x), sqrt(x)), x),
                         domain=Reals, conditions=[GreaterThanEquals(x, zero)])
sqrtTimesItself

endTheorems(locals(), __package__)
