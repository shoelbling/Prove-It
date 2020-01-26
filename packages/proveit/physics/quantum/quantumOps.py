from proveit import Operation, Literal

pkg = __package__ # delete this later; will no longer be needed

class Bra(Operation):
    '''
    Class to represent a Dirac bra vector of the form ⟨0| or ⟨1|.
    '''
    # the literal operator of the Bra operation
    _operator_ = Literal(stringFormat='BRA', context=__file__)

    def __init__(self, label):
        Operation.__init__(self, Bra._operator_, label)
        self.label = self.operands[0] # might need to change
    
    def _formatted(self, formatType, fence=False):
        if formatType == 'latex':
            return (r'\langle '
                    + self.label.formatted(formatType, fence=False)
                    + r' \rvert')
        else: # using the unicode \u2329 for the left angle bracket
            return (u'\u2329'
                    + self.label.formatted(formatType, fence=False)
                    + '|')


class Ket(Operation):
    '''
    Class to represent a Dirac ket vector of the form |0⟩ or |1⟩.
    '''
    # the literal operator of the Ket operation
    _operator_ = Literal(stringFormat='KET', context=__file__)

    def __init__(self, label):
        Operation.__init__(self, Ket._operator_, label)
        self.label = self.operands[0]
    
    def _formatted(self, formatType, fence=False, no_lvert=False):
        leftStr = r'\lvert ' if formatType == 'latex' else '|'
        if no_lvert: leftStr = ''
        if formatType == 'latex':
            return (leftStr +
                    self.label.formatted(formatType, fence=False) +
                    r' \rangle')
        else: # using the unicode \u232A for the right angle bracket
            return (leftStr
                    + self.label.formatted(formatType, fence=False)
                    + u'\u232A')

# class RegisterBra(Operation):
#     def __init__(self, label, size):
#         Operation.__init__(self, REGISTER_BRA, [label, size])
#         self.label = label
#         self.size = size # size of the register
    
#     def _config_latex_tool(self, lt):
#         Operation._config_latex_tool(self, lt)
#         if not 'mathtools' in lt.packages:
#             lt.packages.append('mathtools')
                
#     def formatted(self, formatType, fence=False):
#         formattedLabel = self.label.formatted(formatType, fence=False)
#         formattedSize = self.size.formatted(formatType, fence=False)
#         if formatType == LATEX:
#             return r'\prescript{}{' + formattedSize + r'}\langle ' + formattedLabel + r' \rvert'
#         else:
#             return '{' + formattedSize + '}_<'+formattedLabel+'|'

# REGISTER_BRA = Literal(pkg, 'REGISTER_BRA', operationMaker = lambda operands : RegisterBra(*operands))

# class RegisterKet(Operation):
#     def __init__(self, label, size):
#         Operation.__init__(self, REGISTER_KET, [label, size])
#         self.label = label
#         self.size = size # size of the register
    
#     def formatted(self, formatType, fence=False, no_lvert=False):
#         formattedLabel = self.label.formatted(formatType, fence=False)
#         formattedSize = self.size.formatted(formatType, fence=False)
#         leftStr = r'\lvert ' if formatType == LATEX else '|'
#         if no_lvert: leftStr = ''
#         if formatType == LATEX:
#             return leftStr + formattedLabel + r' \rangle_{' + formattedSize + '}'
#         else:
#             return leftStr + formattedLabel + '>_{' + formattedSize + '}'

# REGISTER_KET = Literal(pkg, 'REGISTER_KET', operationMaker = lambda operands : RegisterKet(*operands))
    
# class Meas(Operation):
#     def __init__(self, ket):
#         Operation.__init__(self, MEAS, ket)
#         self.ket = ket
    
# MEAS = Literal(pkg, 'MEAS', {LATEX: r'{\cal M}'}, operationMaker = lambda operands : Meas(*operands))

