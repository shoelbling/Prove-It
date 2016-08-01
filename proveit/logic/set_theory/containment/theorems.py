from proveit.logic import Forall, Implies, SubsetEq, SupersetEq, InSet
from proveit.common import A, B, x
from proveit import beginTheorems, endTheorems

beginTheorems(locals())

unfoldSubsetEq = Forall((A, B), Implies(SubsetEq(A, B), Forall(x, InSet(x, B), A)))
unfoldSubsetEq

foldSubsetEq = Forall((A, B), Implies(Forall(x, InSet(x, B), A), SubsetEq(A, B)))
foldSubsetEq

unfoldSupersetEq = Forall((A, B), Implies(SupersetEq(A, B), Forall(x, InSet(x, A), B)))
unfoldSupersetEq

foldSupersetEq = Forall((A, B), Implies(Forall(x, InSet(x, A), B), SupersetEq(A, B)))
foldSupersetEq

endTheorems(locals(), __package__)

