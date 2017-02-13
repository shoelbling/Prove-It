"""
This is the expression module.
"""

from proveit._core_.defaults import defaults, USE_DEFAULTS
from proveit._core_.storage import storage
import re

class Expression:
    unique_id_map = dict() # map unique_id's to unique_rep's
    expr_to_prove = None # the theorem currently being proven (if there is one)
    
    # (expression, assumption) pairs for which conclude is in progress, tracked to prevent infinite
    # recursion in the `prove` method.
    in_progress_to_conclude = set() 
            
    def __init__(self, coreInfo, subExpressions=tuple()):
        '''
        Initialize an expression with the given coreInfo (information relevant at the core Expression-type
        level) which should be a list (or tuple) of strings, and a list (or tuple) of subExpressions.
        '''
        for coreInfoElem in coreInfo:
            if not isinstance(coreInfoElem, str):
                raise TypeError('Expecting coreInfo elements to be of string type')
        for subExpression in subExpressions:
            if not isinstance(subExpression, Expression):
                raise TypeError('Expecting subExpression elements to be of Expression type')
        # unique_rep is a unique representation based upon the coreInfo and unique_id's of sub-Expressions
        self._coreInfo, self._subExpressions = coreInfo, subExpressions
        self._unique_rep = self._generate_unique_rep(lambda expr : hex(expr._unique_id))
        # generate the unique_id based upon hash(unique_rep) but safely dealing with improbable collision events
        self._unique_id = hash(self._unique_rep)
        while self._unique_id in Expression.unique_id_map and Expression.unique_id_map[self._unique_id] != self._unique_rep:
            self._unique_id += 1
        Expression.unique_id_map[self._unique_id] = self._unique_rep
    
    def _generate_unique_rep(self, objectRepFn):
        '''
        Generate a unique representation string using the given function to obtain representations of other referenced Prove-It objects.
        '''
        return str(self.__class__) + '[' + ','.join(self._coreInfo) + '];[' + ','.join(objectRepFn(expr) for expr in self._subExpressions) + ']'
    
    @staticmethod
    def _referencedObjIds(unique_rep):
        '''
        Given a unique representation string, returns the list of representations
        of Prove-It objects that are referenced.
        '''
        # After the ';' comes the list of sub-Expressions.
        subExprs = unique_rep.split(';')[-1]
        objIds = re.split("\[|,|\]",subExprs) 
        return [objId for objId in objIds if len(objId) > 0]  
            
    def __setattr__(self, attr, value):
        '''
        Expressions should be read-only objects.  Attributes may be added, however; for example,
        the 'png' attribute which will be added whenever it is generated).
        '''
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")
        self.__dict__[attr] = value      
    
    def __repr__(self):
        return str(self) # just use the string representation
    
    def __eq__(self, other):
        if isinstance(other, Expression):
            return self._unique_id == other._unique_id
        else: return False # other must be an Expression to be equal to self
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return self._unique_id
    
    def __str__(self):
        '''
        Return a string representation of the Expression.
        '''
        return self.string()

    def string(self, **kwargs):
        '''
        Return a string representation of the Expression.  The kwargs can contain formatting
        directives (such as 'fence' used to indicate when a sub-expression should be wrapped in
        parentheses if there can be ambiguity in the order of operations).
        '''
        raise NotImplementedError("'string' method not implemented for " + str(self.__class__))

    def latex(self, **kwargs):
        '''
        Return a latex-formatted representation of the Expression.  The kwargs can contain formatting
        directives (such as 'fence' used to indicate when a sub-expression should be wrapped in
        parentheses if there can be ambiguity in the order of operations).
        '''
        raise NotImplementedError("'latex' method not implemented for " + str(self.__class__))
    
    def formatted(self, formatType, **kwargs):
        '''
        Returns a formatted version of the expression for the given formatType
        ('string' or 'latex').  In the keyword arguments, fence=True indicates
        that parenthesis around the sub-expression may be necessary to avoid 
        ambiguity.
        '''
        if formatType == 'string': return self.string(**kwargs)
        if formatType == 'latex': return self.latex(**kwargs)
    
    @classmethod
    def make(subClass, coreInfo, subExpressions):
        '''
        Should make the Expression object for the specific Expression sub-class based upon the coreInfo
        and subExpressions.  Must be implemented for each Expression sub-class that can be instantiated.
        '''
        raise MakeNotImplemented(subClass)
    
    def coreInfo(self):
        '''
        Copy out the core information.
        '''
        return tuple(self._coreInfo)
    
    def subExpr(self, idx):
        return self._subExpressions[idx]
        
    def subExprIter(self):
        '''
        Iterator over the sub-expressions of this expression.
        '''
        return iter(self._subExpressions)
    
    def prove(self, assumptions=USE_DEFAULTS, automation=USE_DEFAULTS):
        '''
        Attempt to prove this expression automatically under the
        given assumptions (if None, uses defaults.assumptions).  First
        it tries to find an existing KnownTruth, then it tries a simple
        proof by assumption (if self is contained in the assumptions),
        then it attempts to call the 'conclude' method.  If successful,
        the KnownTruth is returned, otherwise an exception is raised.
        Cyclic attempts to `conclude` the same expression under the
        same set of assumptions will be blocked, so `conclude` methods are
        free make attempts that may be cyclic.
        '''
        from proveit import KnownTruth, ProofFailure
        from proveit import Not
        assumptions = defaults.checkedAssumptions(assumptions)
        assumptionsSet = set(assumptions)
        if automation is USE_DEFAULTS:
            automation = defaults.automation
                
        foundTruth = KnownTruth.findKnownTruth(self, assumptionsSet)
        if foundTruth is not None: 
            return foundTruth # found an existing KnownTruth that does the job!
        
        if self in assumptionsSet:
            # prove by assumption
            from proveit._core_.proof import Assumption
            return Assumption(self).provenTruth
        
        if not automation:
            raise ProofFailure(self, assumptions, "No pre-existing proof")
                                                
        # Use Expression.in_progress_to_conclude set to prevent an infinite recursion
        in_progress_key = (self, tuple(sorted(assumptions)))
        if in_progress_key in Expression.in_progress_to_conclude:
            raise ProofFailure(self, assumptions, "Infinite 'conclude' recursion blocked.")
        Expression.in_progress_to_conclude.add(in_progress_key)        
        
        try:
            concludedTruth = None
            if isinstance(self, Not):
                # if it is a Not expression, try concludeNegation on the operand
                try:
                    concludedTruth = self.operands[0].concludeNegation(assumptions=assumptions)
                except NotImplementedError:
                    pass # that didn't work, try conclude on the Not expression itself
            if concludedTruth is None:
                concludedTruth = self.conclude(assumptions)
            if not isinstance(concludedTruth, KnownTruth):
                raise ValueError("'conclude' method should return a KnownTruth (or raise an exception)")
            if concludedTruth.expr != self:
                raise ValueError("'conclude' method should return a KnownTruth for this Expression object.")
            if not concludedTruth.assumptionsSet.issubset(assumptionsSet):
                raise ValueError("While proving " + str(self) + ", 'conclude' method returned a KnownTruth with extra assumptions: " + str(set(concludedTruth.assumptions) - assumptionsSet))
            return concludedTruth
        except NotImplementedError:
            raise ProofFailure(self, assumptions, "'conclude' method not implemented for proof automation")
        finally:
            Expression.in_progress_to_conclude.remove(in_progress_key)

    def disprove(self, assumptions=USE_DEFAULTS, automation=USE_DEFAULTS):
        '''
        Attempt to prove the logical negation (Not) of this expression. 
        If successful, the KnownTruth is returned, otherwise an exception
        is raised.  By default, this simply calls prove on the negated
        expression. Override `concludeNegation` for automation specific to
        the type of expression being negated.      
        '''
        from proveit import Not
        return Not(self).prove(assumptions=assumptions, automation=automation)
                        
    def conclude(self, assumptions=USE_DEFAULTS):
        '''
        Attempt to conclude, via automation, that this statement is true
        under the given assumptions.  Return the KnownTruth if successful,
        or raise an exception.  By default, concludeViaReduction and
        concludeViaImplication are attempted (in that order),
        but this may be overridden with other behavior for each particular
        Expression class.  This is called by the `prove` method when no 
        existing proof was found and it cannot be proven trivially via assumption.
        The `prove` method has a mechanism to prevent infinite recursion, 
        so there are no worries regarding cyclic attempts to conclude an expression.
        '''
        from proveit import concludeViaReduction, concludeViaImplication
        try:
            return concludeViaReduction(self, assumptions)
        except:
            return concludeViaImplication(self, assumptions)
    
    def concludeNegation(self, assumptions=USE_DEFAULTS):
        '''
        Attempt to conclude the negation of this expression under the given
        assumptions, using automation specific to the type of expression being negated.
        Return the KnownTruth if successful, or raise an exception.
        '''
        raise NotImplementedError("'concludeNegation' not implemented for " + str(self.__class__))
        
    def deriveSideEffects(self, knownTruth):
        '''
        Derive side effects, obvious and useful consequences that may be arise from
        proving that this expression is a known truth (under some set of assumptions).
        The default is to do nothing, but should be overridden as appropriate.
        It is best that the side effect derivations are trivial and limited.
        There is no need to call this manually; it is called automatically when
        the corresponding KnownTruth is created.  See tryDerivation which is
        a convenient method for specific implementations of deriveSideEffects.
        '''
        pass        
        
    def qed(self):
        return self.prove().qed()
        
    def substituted(self, exprMap, relabelMap = None, reservedVars = None):
        '''
        Returns this expression with the expressions substituted 
        according to the exprMap dictionary (mapping Expressions to Expressions --
        for specialize, this may only map Variables to Expressions).
        If supplied, reservedVars is a dictionary that maps reserved Variable's
        to relabeling exceptions.  You cannot substitute with an expression that
        uses a restricted variable and you can only relabel the exception to the
        restricted variable.  This is used to protect an Lambda function's "scope".
        '''
        if (exprMap is not None) and (self in exprMap):
            return exprMap[self]._restrictionChecked(reservedVars)
        else:
            return self
    
    def relabeled(self, relabelMap, reservedVars=None):
        '''
        A watered down version of substitution in which only variable labels are
        changed.  This may also involve substituting a MultiVariable with a list
        of Variables.
        '''
        return self.substituted(exprMap=dict(), relabelMap=relabelMap, reservedVars=reservedVars)
    
    def _validateRelabelMap(self, relabelMap):
        if len(relabelMap) != len(set(relabelMap.values())):
            raise ImproperRelabeling("Cannot relabel different Variables to the same Variable.")
    
    def usedVars(self):
        """
        Returns any variables used in the expression.
        """
        return set()
    
    def freeVars(self):
        """
        Returns the used variables that are not bound as an instance variable.
        """
        return set()    

    def freeMultiVars(self):
        """
        Returns the used multi-variables that are not bound as an instance variable
        or wrapped in a Bundle (see multiExpression.py).
        """
        return set()    

    def safeDummyVar(self):
        from proveit._core_.expression.label.var import safeDummyVar
        return safeDummyVar(self)

    def safeDummyVars(self, n):
        from proveit._core_.expression.label.var import safeDummyVar
        dummyVars = []
        for _ in range (n):
            dummyVars.append(safeDummyVar(*([self] + dummyVars)))
        return dummyVars
            
    def evaluate(self, assumptions=USE_DEFAULTS):
        '''
        If possible, return a KnownTruth of this expression equal to its
        irreducible value.  At the Expression level, this attempts to
        prove the expression and, if successful, return this expression
        equal to TRUE.  Override for other appropriate functionality.
        '''
        from proveit import defaultEvaluate
        return defaultEvaluate(self, assumptions)
    
    def orderOfAppearance(self, subExpressions):
        '''
        Yields the given sub-Expressions in the order in which they
        appear in this Expression.  There may be repeats.
        '''
        if self in subExpressions:
            yield self
        for subExpr in self._subExpressions:
            for expr in subExpr.orderOfAppearance(subExpressions):
                yield expr
        
    def _restrictionChecked(self, reservedVars):
        '''
        Check that a substituted expression (self) does not use any reserved variables
        (parameters of a Lambda function Expression).
        '''
        if not reservedVars is None and not self.freeVars().isdisjoint(reservedVars.keys()):
            raise ScopingViolation("Must not make substitution with reserved variables  (i.e., parameters of a Lambda function)")
        return self
    
    def _repr_png_(self):
        '''
        Generate a png image from the latex.  May be recalled from memory or
        storage if it was generated previously.
        '''
        if not hasattr(self,'png'):
            self.png = storage._retrieve_png(self, self.latex(), self._config_latex_tool)
        return self.png # previous stored or generated
    
    def _config_latex_tool(self, lt):
        '''
        Configure the LaTeXTool from IPython.lib.latextools as required by all
        sub-expressions.
        '''
        for sub_expr in self._subExpressions:
            sub_expr._config_latex_tool(lt)

    def exprInfo(self, details=False):
        from proveit._core_.expression.expr_info import ExpressionInfo
        return ExpressionInfo(self, details)

def tryDerivation(method, *args, **kwargs):
    '''
    An implementation of deriveSideEffects may call tryDerivation to
    simply attempt to derive a side-effect but skip it if it fails
    (for example, not all conditions are met or if a theorem is
    unavailable during a particular proof to avoid circular logic).
    '''
    try:
        method(*args, **kwargs)
    except:
        pass


class MakeNotImplemented(NotImplementedError):
    def __init__(self, exprSubClass):
        self.exprSubClass = exprSubClass
    def __str__(self):
        return "make method not implemented for " + str(self.exprSubClass)

class ImproperSubstitution(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class ImproperRelabeling(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class ScopingViolation(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message


    