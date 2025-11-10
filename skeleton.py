
MAX_CONSTANTS = 10

#------------------------------------------------------------------------------------------------------------------------------:
# Helper Functions

def balanced_parentheses(fmla: str) -> bool:
    depth = 0
    for char in fmla:
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
            if depth < 0:
                return False
    return depth == 0

def main_connective(fmla: str) -> tuple[int|None, str|None]:
    if not fmla:
        return None, None
    if fmla[0] != '(' or fmla[-1] != ')':
        return None, None
    if not balanced_parentheses(fmla):
        return None, None

    depth = 0
    i = 0
    while i < len(fmla):
        char = fmla[i]
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1

        # Only check for main connective when at depth 1 (highest level)
        if depth == 1:
            if char == '-' and i + 1 < len(fmla) and fmla[i+1] == '>':
                return i, '->'
            if char == '\\' and i + 1 < len(fmla) and fmla[i+1] == '/':
                return i, '\\/'
            if char == '&':
                return i, '&'
        i += 1
    return None, None

def is_prop_atom(f: str) -> bool:
    return f in ['p', 'q', 'r', 's']

def is_fol_atom(f: str) -> bool:
    # Must exactly match the pattern: CapitalLetter ( var , var )
    if len(f) != 6:
        return False
    if f[0] not in ['P', 'Q', 'R', 'S']:
        return False
    if f[1] != '(' or f[3] != ',' or f[5] != ')':
        return False
    if f[2] not in ['x', 'y', 'z', 'w'] or f[4] not in ['x', 'y', 'z', 'w']:
        return False
    return True


#------------------------------------------------------------------------------------------------------------------------------:
# Testing

def test_balanced_parentheses():
    assert balanced_parentheses('(P&Q)')
    assert balanced_parentheses('((P\\/Q)->R)')
    assert balanced_parentheses('(P->(Q&R))')
    assert not balanced_parentheses('(P&(Q->R)')
    assert not balanced_parentheses('P&Q)')
    assert balanced_parentheses('((P&Q)->(R\\/S))')
    print("Balanced Parentheses: All tests passed.\n")


def test_main_connective():
    assert main_connective('(P&Q)') == (2, '&')
    assert main_connective('((P\\/Q)->R)') == (7, '->')
    assert main_connective('(P->(Q&R))') == (2, '->')
    assert main_connective('(P)') == (None, None)
    assert main_connective('((P&Q)\\/(R->S))') == (6, '\\/')
    assert main_connective('p->q') == (None, None)          # no outer brackets
    assert main_connective('') == (None, None)
    print("Main Connective: All tests passed.\n")


def test_is_prop_atom():
    assert is_prop_atom('p')
    assert is_prop_atom('q')
    assert is_prop_atom('r')
    assert is_prop_atom('s')
    assert not is_prop_atom('P')
    assert not is_prop_atom('x')
    assert not is_prop_atom('(p&q)')
    print("Propositional Atom: All tests passed.\n")


def test_is_fol_atom():
    assert is_fol_atom('P(x,y)')
    assert is_fol_atom('Q(z,w)')
    assert is_fol_atom('R(x,x)')
    assert is_fol_atom('S(y,z)')
    assert not is_fol_atom('P(x)')
    assert not is_fol_atom('P(x,y,z)')
    assert not is_fol_atom('P(a,b)')
    assert not is_fol_atom('p')
    assert not is_fol_atom('(P(x,y)&Q(z,w))')
    print("First-Order Logic Atom: All tests passed.\n")

test_balanced_parentheses()
test_main_connective()
test_is_prop_atom()
test_is_fol_atom()
print("================================\n\n")

#------------------------------------------------------------------------------------------------------------------------------:
# Main Tableau Functions

# Parse a formula, consult parseOutputs for return values.
def parse(fmla: str) -> int:
    return 0

# Return the LHS of a binary connective formula
def lhs(fmla: str) -> str:
    i, connective = main_connective(fmla)
    if i is None or connective is None:
        return ''
    return fmla[1:i]

# Return the connective symbol of a binary connective formula
def con(fmla: str) -> str:
    _, connective = main_connective(fmla)
    if connective is None:
        return ''
    return connective

# Return the RHS symbol of a binary connective formula
def rhs(fmla: str) -> str:
    i, connective = main_connective(fmla)
    if i is None or connective is None:
        return ''
    return fmla[i+len(connective):-1]

# You may choose to represent a theory as a set or a list
def theory(fmla: str) -> list[str]:  # initialise a theory with a single formula in it
    return None

#check for satisfiability
def sat(tableau) -> int:
#output 0 if not satisfiable, output 1 if satisfiable, output 2 if number of constants exceeds MAX_CONSTANTS
    return 0

#------------------------------------------------------------------------------------------------------------------------------:
#                                            DO NOT MODIFY THE CODE BELOW THIS LINE!                                           :
#------------------------------------------------------------------------------------------------------------------------------:

f = open('input.txt')

parseOutputs = ['not a formula',
                'an atom',
                'a negation of a first order logic formula',
                'a universally quantified formula',
                'an existentially quantified formula',
                'a binary connective first order formula',
                'a proposition',
                'a negation of a propositional formula',
                'a binary connective propositional formula']

satOutput = ['is not satisfiable', 'is satisfiable', 'may or may not be satisfiable']



firstline = f.readline()

PARSE = False
if 'PARSE' in firstline:
    PARSE = True

SAT = False
if 'SAT' in firstline:
    SAT = True

for line in f:
    if line[-1] == '\n':
        line = line[:-1]
    parsed = parse(line)

    if PARSE:
        output = "%s is %s." % (line, parseOutputs[parsed])
        if parsed in [5,8]:
            output += " Its left hand side is %s, its connective is %s, and its right hand side is %s." % (lhs(line), con(line) ,rhs(line))
        print(output)

    if SAT:
        if parsed:
            tableau = [theory(line)]
            print('%s %s.' % (line, satOutput[sat(tableau)]))
        else:
            print('%s is not a formula.' % line)