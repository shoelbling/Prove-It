from basiclogic import *

# hypothesis = [P(TRUE) and P(FALSE)]
hypothesis = And(PofTrue, PofFalse)
# inBool(A=TRUE), inBool(A=FALSE), inBool(P(A) = TRUE)
AeqT = Equals(A, TRUE)
AeqF = Equals(A, FALSE)
PofAeqT = Equals(PofA, TRUE)
for eqExpr in (AeqT, AeqF, PofAeqT):
    eqExpr.deduceInBool()
# P(TRUE), P(FALSE) assuming hypothesis
for case in hypothesis.decompose(): case.prove({hypothesis})
# A=TRUE => P(A)=TRUE assuming hypothesis
Implies(AeqT, deriveStmtEqTrue(AeqT.lhsSubstitute(A, PofA))).prove({hypothesis})
# A=FALSE => P(A)=TRUE assuming hypothesis
Implies(AeqF, deriveStmtEqTrue(AeqF.lhsSubstitute(A, PofA))).prove({hypothesis})
# P(A) assuming hypothesis, (A in BOOLEANS)
inBool(A).unfold().deriveCommonConclusion(PofAeqT).deriveViaBooleanEquality().prove({hypothesis, inBool(A)})
# forall_{P} P(TRUE) and P(FALSE) => forall_{A in BOOLEANS} P(A)
booleans.qed('foldForallOverBool', Implies(hypothesis, PofA.generalize(A, inBool(A))).generalize(P))
