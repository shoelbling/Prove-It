from proveit.basiclogic import FALSE, Equals, Implies
from proveit.basiclogic.variables import A

# A = FALSE
AeqF = Equals(A, FALSE)
# FALSE assuming A=FALSE and A
AeqF.deriveRightViaEquivalence().prove({AeqF, A})
# forall_{A} (A=FALSE) => [A => FALSE]
Implies(AeqF, Implies(A, FALSE)).generalize([A]).qed(__file__)