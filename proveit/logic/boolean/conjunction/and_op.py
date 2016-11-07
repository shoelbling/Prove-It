from proveit import Literal, AssociativeOperation, USE_DEFAULTS
from proveit.logic.boolean.booleans import TRUE, FALSE, deduceInBool
from proveit.common import A, B, Aetc, Cetc

AND = Literal(__package__, stringFormat = 'and', latexFormat = r'\land')

class And(AssociativeOperation):
    def __init__(self, *operands):
        r'''
        And together any number of operands: :math:`A \land B \land C`
        '''
        AssociativeOperation.__init__(self, AND, *operands)
        
    @classmethod
    def operatorOfOperation(subClass):
        return AND
    
    def conclude(self, assumptions):
        '''
        Try to automatically conclude this conjunction via composing the constituents.
        That is, conclude some :math:`A \land B \and ... \land Z` via
        :math:'A', :math:'B', ..., :math:'Z' individually.
        '''
        return self.concludeViaComposition(assumptions)    
    
    def deriveSideEffects(self, knownTruth):
        '''
        From a conjunction, automatically derive the individual constituents.
        That is, deduce :math:'A', :math:'B', ..., :math:'Z' from
        :math:`A \land B \and ... \land Z`.
        '''
        for i in xrange(len(self.operands)):
            self.deriveInPart(i, assumptions=knownTruth.assumptions) # uses axiom
        
    def deriveInPart(self, indexOrExpr, assumptions=USE_DEFAULTS):
        r'''
        From :math:`(A \land ... \land X \land ... \land Z)` derive :math:`X`.  indexOrExpr specifies 
        :math:`X` either by index or the expr.
        '''
        from _axioms_ import andImpliesEach
        from proveit.common import Aetc, Cetc
        idx = indexOrExpr if isinstance(indexOrExpr, int) else list(self.operands).index(indexOrExpr)
        return andImpliesEach.specialize({Aetc:self.operands[:idx], B:self.operands[idx], Cetc:self.operands[idx+1:]}).deriveConclusion(assumptions)
    
    def concludeViaComposition(self, assumptions=USE_DEFAULTS):
        '''
        Prove and return some (A and B ... and ... Z) via A, B, ..., Z each proven individually.
        See also the compose method to do this constructively.
        '''
        return compose(self.operands, assumptions)
    
    def evaluate(self, assumptions=USE_DEFAULTS):
        '''
        Given operands that evaluate to TRUE or FALSE, derive and
        return the equality of this expression with TRUE or FALSE. 
        '''
        from _axioms_ import andTT, andTF, andFT, andFF # load in truth-table evaluations    
        from _theorems_ import conjunctionTrueEval, conjunctionFalseEval
        falseIndex = -1
        for i, operand in enumerate(self.operands):
            if operand != TRUE and operand != FALSE:
                # The operands are not always true/false, so try the default evaluate method
                # which will attempt to evaluate each of the operands.
                return AssociativeOperation.evaluate(self, assumptions)
            if operand == FALSE:
                falseIndex = i
        if falseIndex >= 0:
            # one operand is FALSE so the whole conjunction evaluates to FALSE.
            return conjunctionFalseEval.specialize({Aetc:self.operands[:falseIndex], Cetc:self.operands[falseIndex+1:]})
        else:
            # no operand is FALSE so the whole disjunction evaluates to TRUE.
            return conjunctionTrueEval.specialize({Aetc:self.operands})
        
    def deduceInBool(self, assumptions=USE_DEFAULTS):
        '''
        Attempt to deduce, then return, that this 'and' expression is in the set of BOOLEANS.
        '''
        from _theorems_ import conjunctionClosure
        return conjunctionClosure.specialize({Aetc:self.operands}, assumptions=assumptions)
    
def compose(expressions, assumptions=USE_DEFAULTS):
    '''
    Returns [A and B and ...], the And operator applied to the collection of given arguments,
    derived from each separately.
    '''
    from _theorems_ import conjunctionIntro
    return conjunctionIntro.specialize({Aetc:expressions}, assumptions=assumptions)
