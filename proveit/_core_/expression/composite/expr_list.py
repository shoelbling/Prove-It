from composite import Composite, NestedCompositeExpressionError
from proveit._core_.expression.expr import Expression, MakeNotImplemented

class ExpressionList(Composite, Expression, list):
    """
    An ExpressionList is a composite expr composed of an ordered list of member
    Expressions.  An ExpressionList is may not be nested.  Use of etcetera can allow
    substitutions that are absorbed into the containing ExpressionList.  For example
    ExpressionList(x, etcetera(y)) can become ExpressionList(x, y, z) by doing
    a substition of y to ExpressionList(y, z).
    """
    def __init__(self, *expressions):
        '''
        Initialize an ExpressionList from one or more expr arguments.
        '''
        list.__init__(self)
        if len(expressions) == 1 and not isinstance(expressions[0], Expression): 
            expressions = expressions[0] # allowed to pass in a single list argument
        for expr in expressions:
            if isinstance(expr, ExpressionList):
                raise NestedCompositeExpressionError('May not nest ExpressionLists (do you need to use etcetera? or ExpressionTensor?)')
            if not isinstance(expr, Expression):
                raise TypeError('ExpressionList must be created out of Expressions)')
            #if isinstance(expr, Block):
            #    raise TypeError('A Block expression may only be used in an ExpressionTensor (you may use an etcetera Operation in an ExpressionList)')
            self.append(expr)
        self.shape = (len(self),)
        Expression.__init__(self, ['ExpressionList'], self)
        
    @classmethod
    def make(subClass, coreInfo, subExpressions):
        if subClass != ExpressionList: 
            MakeNotImplemented(subClass)
        if len(coreInfo) != 1 or coreInfo[0] != 'ExpressionList':
            raise ValueError("Expecting ExpressionList coreInfo to contain exactly one item: 'ExpressionList'")
        return ExpressionList(*subExpressions)        
        
    def string(self, **kwargs):
        return self.formatted('string', **kwargs)

    def latex(self, **kwargs):
        return self.formatted('latex', **kwargs)
    
    def formatted(self, formatType, fence=True, subFence=True, formattedOperator=None):
        from proveit._core_.expression.bundle.etcetera import Etcetera
        outStr = ''
        if len(self) == 0: return '()' # for an empty list, show the parenthesis to show something.
        spc = '~' if formatType == 'latex' else ' ' 
        if formattedOperator is None:
            formattedOperator = ','
        formattedSubExpressions = [] 
        for subExpr in self:
            if isinstance(subExpr, Etcetera):
                if len(formattedSubExpressions) > 0 and formattedSubExpressions[-1] == '..'+spc:
                    # instead of having "..  .." back-to-back, do ".."
                    formattedSubExpressions[-1] = '...'
                else:
                    formattedSubExpressions.append(spc+'..')
                formattedSubExpressions.append(' ' + subExpr.bundledExpr.formatted(formatType, fence=subFence) + ' ')
                formattedSubExpressions.append('..'+spc)
            else:
                formattedSubExpressions.append(' ' + subExpr.formatted(formatType, fence=subFence) + ' ')
        # put a comma between each of formattedSubExpressions
        if formatType == 'string':
            if fence: outStr += '('
            outStr += formattedOperator.join(formattedSubExpressions)
            if fence: outStr += ')'
        elif formatType == 'latex':
            if fence: outStr += r'\left('
            outStr += formattedOperator.join(formattedSubExpressions)
            if fence: outStr += r'\right)'
        return outStr           
    
    def substituted(self, exprMap, relabelMap = None, reservedVars = None):
        '''
        Returns this expression with the substitutions made 
        according to exprMap and/or relabeled according to relabelMap.
        Flattens nested ExpressionLists that arise from etcetera substitutions.
        '''
        from proveit._core_.expression.bundle.etcetera import Etcetera
        if (exprMap is not None) and (self in exprMap):
            return exprMap[self]._restrictionChecked(reservedVars)
        def subbedGen():
            for expr in self:
                subbed_expr = expr.substituted(exprMap, relabelMap, reservedVars)
                if isinstance(expr, Etcetera):
                    # expand the etcetera substitution              
                    for etc_expr in subbed_expr if isinstance(subbed_expr, ExpressionList) else [subbed_expr]:
                        yield etc_expr
                else: yield subbed_expr # yield an individual ExpressionList element
        return ExpressionList(*list(subbedGen()))
        
    def usedVars(self):
        '''
        Returns the union of the used Variables of the sub-Expressions.
        '''
        return set().union(*[expr.usedVars() for expr in self])
        
    def freeVars(self):
        '''
        Returns the union of the free Variables of the sub-Expressions.
        '''
        return set().union(*[expr.freeVars() for expr in self])

    def freeMultiVars(self):
        '''
        Returns the union of the free MultiVariables of the sub-Expressions.
        '''
        return set().union(*[expr.freeMultiVars() for expr in self])
