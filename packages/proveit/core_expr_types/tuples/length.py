from proveit import (Expression, Operation, Literal, 
                     singleOrCompositeExpression, ExprTuple,
                     ExprRange, InnerExpr, defaults, USE_DEFAULTS)
from proveit._common_ import a, b, c, d, e, f, g, h, i, j, k, x, y

class Len(Operation):
    # operator of the Length operation.
    _operator_ = Literal(stringFormat='length', context=__file__)   
    
    def __init__(self, operand):
        '''
        Len takes a single operand which should properly be an
        ExprTuple or an expression (such as a variable) that
        represents a tuple.
        '''
        operand = singleOrCompositeExpression(operand)
        if isinstance(operand, ExprTuple):
            # Nest an ExprTuple operand in an extra ExprTuple as
            # a clear indication that Len has a single operand
            # that is an ExprTuple rather than multiple operands.
            operand = ExprTuple(operand)
        # In order to always recognize that Len only takes a single
        # operand, we must wrap it as an ExprTuple with one entry.
        Operation.__init__(self, Len._operator_, operand)
        if defaults.automation==True:
            # Handle some automation for dealing with
            # ExprTuple length requirements in the expansion of 
            # iterated parameters (see Lambda.apply).
            try:
                self.autoInvocations()                            
            finally:
                defaults.automation = True
    
    def autoInvocations(self):
        '''
        Invoke useful axioms/theorems pertaining to this Len expression
        for automation purposes.  In particular, these are meant for
        dealing with ExprTuple length requirements in the expansion of 
        iterated parameters (see Lambda.apply).
        '''
        # Avoid infinite recursion:
        prev_automation = defaults.automation
        defaults.automation = False 
        try:
            operand = self.operand
            if (isinstance(operand, ExprTuple) and len(operand)==1 
                    and isinstance(operand[0], ExprRange)):
                # In the special case of needing the length of an
                # iteration of the form (1, ..., n) where n is a decimal,
                # import theorems that may be relevant.  For example:
                # (1, 2, 3) = (1, ..., 3)
                # |(1, 2, 3)| = |(1, ..., 3)|
                from proveit.number import one
                import proveit.number.numeral.deci
                from proveit.number.numeral.deci import DIGITS
                range_entry = operand[0]
                start_index = range_entry.start_index
                end_index = range_entry.end_index
                lambda_map = range_entry.lambda_map
                if range_entry.body == range_entry.parameter:
                    if (start_index == one and end_index in DIGITS):
                        n = end_index.asInt()
                        proveit.number.numeral.deci._theorems_\
                            .__getattr__('count_to_%d'%n)
                        proveit.number.numeral.deci._theorems_\
                            .__getattr__('count_to_%d_len'%n)
                try:
                    if start_index==one:
                        from proveit.core_expr_types.tuples._theorems_ import (
                                simple_range_len, simple_range_len_val)    
                        thm1, thm2 = simple_range_len, simple_range_len_val
                        for thm in (thm1, thm2):
                            thm.instantiate({f:lambda_map,
                                             i:end_index})
                    else:
                        from proveit.core_expr_types.tuples._theorems_ import (
                                range_len, range_len_val)
                        thm1, thm2 = range_len, range_len_val
                        for thm in (thm1, thm2):
                            thm.instantiate({f:lambda_map,
                                             i:start_index, j:end_index})
                except:
                    pass
                    
            elif isinstance(operand, ExprTuple) and \
                    not any(isinstance(entry, ExprRange) for entry in operand):
                if 0 < len(operand) < 10:
                    # Automatically get the count and equivalence with
                    # the length of the proper iteration starting from
                    # 1.  For example,
                    # |(a, b, c)| = 3
                    # |(a, b, c)| = |(1, .., 3)|
                    import proveit.number.numeral.deci
                    n = len(operand)
                    len_thm = proveit.number.numeral.deci._theorems_\
                                .__getattr__('tuple%d_len'%n)
                    iter_len_thm = proveit.number.numeral.deci._theorems_\
                                    .__getattr__('tuple%d_range_len'%n)
                    repl_map = dict()
                    for param, entry in zip(len_thm.explicitInstanceParams(),
                                            operand):
                        repl_map[param] = entry
                    len_thm.specialize(repl_map)
                    iter_len_thm.specialize(repl_map)
            elif isinstance(operand, ExprTuple) and len(operand)==2 \
                    and not isinstance(operand[1], ExprRange):
                # see if we can apply 'extension_range_len'
                from proveit.number import Add, one
                assert isinstance(operand[0], ExprRange)
                range_lambda = operand[0].lambda_map
                range_start = operand[0].start_index
                range_end = operand[0].end_index
                if operand[1] == range_lambda.apply(Add(range_end, one)):
                    from proveit.core_expr_types.tuples._theorems_ import (
                                extension_range_len)
                    extension_range_len.instantiate({f:range_lambda,
                                                     i:range_start,
                                                     j:range_end})
        finally:
            # Restore the defaults.automation flag.
            defaults.automation = prev_automation
    
    @staticmethod
    def extractInitArgValue(argName, operator_or_operators, operand_or_operands):
        if argName=='operand':
            return operand_or_operands[0]
        
    def string(self, **kwargs):
        return '|' + self.operand.string() + '|'
    
    def latex(self, **kwargs):
        return '|' + self.operand.latex() + '|'
    
    def computation(self, assumptions=USE_DEFAULTS):
        '''
        
        '''
        from proveit.number import one
        if not isinstance(self.operand, ExprTuple):
            # Don't know how to compute the length if the operand is
            # not a tuple. For example, it could be a variable that
            # represent a tuple.  So just return the self equality.
            from proveit.logic import Equals
            return Equals(self, self).prove()
        entries = self.operand
        has_range = any(isinstance(entry, ExprRange) for entry in entries)
        if len(entries)==1 and has_range:
            # Compute the length of a single range.  Examples:
            # |(f(1), ..., f(n))| = n
            # |(f(i), ..., f(j))| = j-i+1
            range_entry = entries[0]
            start_index = range_entry.start_index
            end_index = range_entry.end_index
            lambda_map = range_entry.lambda_map
            if start_index==one:
                from proveit.core_expr_types.tuples._theorems_ import \
                    simple_range_len_val
                return simple_range_len_val.instantiate({f:lambda_map, i:end_index},
                                                        assumptions=assumptions)
            else:
                from proveit.core_expr_types.tuples._theorems_ import range_len_val
                return range_len_val.instantiate({f:lambda_map, i:start_index, j:end_index},
                                                assumptions=assumptions)
        elif not has_range:
            # Case of all non-range entries.
            if len(entries) == 0:
                # zero length.
                from proveit.core_expr_types.tuples._axioms_ import tuple_len_0
                return tuple_len_0
            elif len(entries) < 10:
                # Automatically get the count and equivalence with
                # the length of the proper iteration starting from
                # 1.  For example,
                # |(a, b, c)| = 3
                # |(a, b, c)| = |(1, .., 3)|
                import proveit.number.numeral.deci
                n = len(entries)
                len_thm = proveit.number.numeral.deci._theorems_\
                            .__getattr__('tuple%d_len'%n)
                repl_map = dict()
                for param, entry in zip(len_thm.explicitInstanceParams(),
                                        entries):
                    repl_map[param] = entry
                return len_thm.specialize(repl_map)
        elif len(entries)==2 and not isinstance(entries[1], ExprRange):
            from proveit.core_expr_types.tuples._theorems_ import \
                simple_extension_range_len_val
            assert isinstance(entries[0], ExprRange)
            range_lambda = entries[0].lambda_map
            range_start = entries[0].start_index
            range_end = entries[0].end_index
            if range_start==one:
                return simple_extension_range_len_val.instantiate(
                        {f:range_lambda, b:entries[1], i:range_end})
        raise NotImplementedError("Len.computation not implemented for "
                                  "this case yet: %s"%self)

    def rangeLengthReduction(self, assumptions=USE_DEFAULTS):
        '''
        
        '''
        from proveit.number import one
        operand = self.operand
        if isinstance(operand, ExprTuple) and isinstance(operand[0], ExprRange):
            # In the special case of needing the length of an
            # iteration of the form (1, ..., n) where n is a decimal,
            # import theorems that may be relevant.  For example:
            # (1, 2, 3) = (1, ..., 3)
            # |(1, 2, 3)| = |(1, ..., 3)|
            range_entry = operand[0]
            start_index = range_entry.start_index
            end_index = range_entry.end_index
            lambda_map = range_entry.lambda_map
            if start_index==one:
                from proveit.core_expr_types.tuples._theorems_ import \
                    simple_range_len
                return simple_range_len.instantiate({f:lambda_map, i:end_index},
                                                    assumptions=assumptions)
            else:
                from proveit.core_expr_types.tuples._theorems_ import range_len
                return range_len.instantiate({f:lambda_map, i:start_index, j:end_index},
                                             assumptions=assumptions)
        
        raise NotImplementedError("Len.computation not implemented for "
                                  "this case yet: %s"%self)        
    
    def simplification(self, assumptions=USE_DEFAULTS, automation=True):
        if not automation:
            return Expression.simplification(self, assumptions, automation=False)
        from proveit.relation import TransRelUpdater
        eq = TransRelUpdater(self, assumptions)
        expr = eq.update(self.computation(assumptions))
        expr = eq.update(expr.simplification(assumptions))
        return eq.relation
    
    def deduceInNumberSet(self, number_set):
        from proveit.core_expr_types.tuples._theorems_ import (
                range_len_in_nats, simple_len_in_nats)
        from proveit.number import Naturals, one
        operand = self.operand
        if number_set == Naturals:
            if len(operand)==1 and isinstance(operand[0], ExprRange):
                # Special case of proving that the length
                # of a single range is in the set of Naturals.
                range_start = operand[0].start_index
                range_end = operand[0].end_index   
                range_lambda = operand[0].lambda_map
                if range_start == one:
                    return simple_len_in_nats.instantiate({f:range_lambda,
                                                           i:range_end})
                else:
                    return range_len_in_nats.instantiate({f:range_lambda,
                                                          i:range_start,
                                                          j:range_end})
    
    
    
    
    
    
    
    
    
    
    
    
    def _computation(self, must_evaluate=False, assumptions=USE_DEFAULTS):
        '''
        Return the proven equivalence between this Len expression and its
        computed value which may or may not be an irreducible value.  If
        must_evaluate is True, then it must compute an irreducible value or
        raise a SimplificationError.
        '''
        from proveit import ExprTuple, Iter
        from proveit.iteration._axioms_ import tupleLen0
        from proveit.iteration._theorems_ import (singleElemLen, iterLen,
                                                  concatElemLen, concatIterLen, 
                                                  concatSimpleIterLen)
        from proveit.number.numeral.deci._theorems_ import tupleLen1, tupleLen2, tupleLen3, tupleLen4, tupleLen5
        from proveit.number.numeral.deci._theorems_ import tupleLen6, tupleLen7, tupleLen8, tupleLen9
        from proveit.number import one
        
        if len(self.operands) == 0:
            return tupleLen0
        
        has_iter = False
        for operand in self.operands:
            if isinstance(operand, Iter):
                has_iter = True
        
        if not has_iter and len(self.operands) < 10:
            if len(self.operands) == 0:
                return tupleLen0
            elif len(self.operands) == 1:
                return tupleLen1.specialize({a:self.operands[0]})
            elif len(self.operands) == 2:
                a_, b_ = self.operands
                return tupleLen2.specialize({a:a_, b:b_})
            elif len(self.operands) == 3:
                a_, b_, c_ = self.operands
                return tupleLen3.specialize({a:a_, b:b_, c:c_})
            elif len(self.operands) == 4:
                a_, b_, c_, d_ = self.operands
                return tupleLen4.specialize({a:a_, b:b_, c:c_, d:d_})
            elif len(self.operands) == 5:
                a_, b_, c_, d_, e_ = self.operands
                return tupleLen5.specialize({a:a_, b:b_, c:c_, d:d_, e:e_})
            elif len(self.operands) == 6:
                a_, b_, c_, d_, e_, f_ = self.operands
                return tupleLen6.specialize({a:a_, b:b_, c:c_, d:d_, e:e_, f:f_})
            elif len(self.operands) == 7:
                a_, b_, c_, d_, e_, f_, g_ = self.operands
                return tupleLen7.specialize({a:a_, b:b_, c:c_, d:d_, e:e_, f:f_,
                                             g:g_})
            elif len(self.operands) == 8:
                a_, b_, c_, d_, e_, f_, g_, h_ = self.operands
                return tupleLen8.specialize({a:a_, b:b_, c:c_, d:d_, e:e_, f:f_, 
                                             g:g_, h:h_})
            elif len(self.operands) == 9:
                a_, b_, c_, d_, e_, f_, g_, h_, i_ = self.operands
                return tupleLen9.specialize({a:a_, b:b_, c:c_, d:d_, e:e_, f:f_, 
                                             g:g_, h:h_, i:i_})
        else:
            items = self.operands
            last_item_is_iter = isinstance(items[-1], Iter)
            if len(items) > 1: # Multiple items in the ExprTuple
                _a = ExprTuple(*items[:-1]) # leave off the end
                _i = _a.length(assumptions) # Obtain length of the first part.
                if last_item_is_iter:
                    # Multiple items with the last one being an Iter.
                    _f = items[-1].unconditionedMap()
                    if items[-1].start_index == one:
                        _j = items[-1].end_index
                        valuation = \
                            concatSimpleIterLen.specialize({i:_i, j:_j, aa:_a, f:_f},
                                                           assumptions=assumptions)
                    else:
                        _j = items[-1].start_index
                        _k = items[-1].end_index
                        valuation = \
                            concatIterLen.specialize({i:_i, j:_j, k:_k, aa:_a, f:_f},
                                                     assumptions=assumptions)
                else:
                    # Multiple items with the last one being a singular element.
                    valuation = concatElemLen.specialize({i:_i, aa:_a, b:items[-1]})
            elif last_item_is_iter:
                # A single iteration item.
                _f = items[-1].unconditionedMap()
                _i = items[-1].start_index
                _j = items[-1].end_index
                valuation = iterLen.specialize({f:_f, i:_i, j:_j}, 
                                               assumptions=assumptions)
            else:
                # Just a singular element.
                valuation = singleElemLen.specialize({a:items[0]}, 
                                                      assumptions=assumptions)
        
        if must_evaluate:
            rhs_simplification = valuation.rhs.evaluation(assumptions)
        else:
            rhs_simplification = valuation.rhs.simplification(assumptions)
        return valuation.applyTransitivity(rhs_simplification, assumptions)

    def doReducedSimplification(self, assumptions=USE_DEFAULTS):
        '''
        A simplification of a Len operation computes the length as a sum
        of the lengths of each item of the ExprTuple operand, returning
        the equivalence between the Len expression and this computation,
        simplified to the extent possible.  An item may be a singular element
        (contribution 1 to the length) or an iteration contributing its length.
        '''
        return self._computation(must_evaluate=False, assumptions=assumptions)
    
    def doReducedEvaluation(self, assumptions=USE_DEFAULTS):
        '''
        Return the evaluation of the length which equates that Len expression
        to an irreducible result.
        '''
        return self._computation(must_evaluate=True, assumptions=assumptions)
    
    def deduceInNaturalSet(assumptions=USE_DEFAULTS):
        pass
    
# Register these expression equivalence methods:
InnerExpr.register_equivalence_method(Len, 'computation', 'computed', 'compute')