
MAX_CONSTANTS = 10

#------------------------------------------------------------------------------------------------------------------------------:
# Parsing Functions

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
    # Must match: PRED(term, term) where term is variable or constant
    if len(f) != 6:
        return False
    if f[0] not in ['P', 'Q', 'R', 'S']:
        return False
    if f[1] != '(' or f[3] != ',' or f[5] != ')':
        return False

    VARS = ['x', 'y', 'z', 'w']
    CONSTS = [chr(c) for c in range(ord('a'), ord('z') + 1)]
    TERMS = VARS + CONSTS

    return f[2] in TERMS and f[4] in TERMS


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


# Parse a formula, consult parseOutputs for return values.
def parse(fmla: str) -> int:
    if not fmla:
        return 0 # not a formula
    
    if is_prop_atom(fmla):
        return 6 # a proposition
    
    if is_fol_atom(fmla):
        return 1 # an atom
    
    # Negation
    if fmla[0] == '~':
        subfmla = fmla[1:]
        subfmla_parsed = parse(subfmla)
        if subfmla_parsed == 0:
            return 0 # not a formula
        if subfmla_parsed in [6, 7, 8]:
            return 7 # a negation of a propositional formula
        if subfmla_parsed in [1, 2, 3, 4, 5]:
            return 2 # a negation of a first order logic formula
        return 0 # not a formula

    # FOL Quantifiers
    if len(fmla) > 2 and fmla[0] in ['A', 'E'] and fmla[1] in ['x', 'y', 'z', 'w']:
        subfmla = fmla[2:]
        subfmla_parsed = parse(subfmla)
        if subfmla_parsed == 0:
            return 0 # not a formula
        if fmla[0] == 'A':
            return 3 # a universally quantified formula
        elif fmla[0] == 'E':
            return 4 # an existentially quantified formula
        return 0 # not a formula
    
    # Only binary connectives require parentheses checking
    if not balanced_parentheses(fmla):
        return 0 # not a formula 

    # Binary Connectives
    if fmla[0] == '(' and fmla[-1] == ')':
        connective = con(fmla)
        left = lhs(fmla)
        right = rhs(fmla)

        if not connective or not left or not right:
            return 0 # not a formula

        lparsed = parse(left)
        rparsed = parse(right)
        if lparsed == 0 or rparsed == 0:
            return 0 # not a formula
        
        if lparsed in [6, 7, 8] and rparsed in [6, 7, 8]:
            return 8 # a binary connective propositional formula
        elif lparsed in [1, 2, 3, 4, 5] or rparsed in [1, 2, 3, 4, 5]:
            return 5 # a binary connective first order formula
        return 0 # not a formula
        
    return 0 # not a formula


#------------------------------------------------------------------------------------------------------------------------------:
# Parsing Testing

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
    assert main_connective('p->q') == (None, None)
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

# test_balanced_parentheses()
# test_main_connective()
# test_is_prop_atom()
# test_is_fol_atom()
# print("================================\n\n")

#------------------------------------------------------------------------------------------------------------------------------:
# Satisfiability Functions

def is_literal(fmla: str) -> bool:
    if is_fol_atom(fmla) or is_prop_atom(fmla):
        return True
    if fmla.startswith('~'):
        subfmla = fmla[1:]
        if is_fol_atom(subfmla) or is_prop_atom(subfmla):
            return True
    return False

def branch_contradiction(branch: list[str]) -> bool:
    for fmla in branch:
        if fmla.startswith('~'):
            if fmla[1:] in branch:
                return True
        else:
            if ('~' + fmla) in branch:
                return True
    return False

def expand(branch: list[str]) -> list[list[str]]:

    target_fmla = None
    for fmla in branch:
        if not is_literal(fmla):
            target_fmla = fmla
            break
    
    if target_fmla is None:
        return [branch]
    
    t = target_fmla
    p = parse(t)

    def rest() -> list[str]:
        new_branch = branch.copy()
        if t in new_branch:
            new_branch.remove(t)
        return new_branch
    
    inner = t[1:] if t.startswith('~') else t
    inner_connective = con(inner) if inner and inner.startswith('(') and inner.endswith(')') else ''

    # Alpha expansions
    if t.startswith('~(') and inner_connective == '->':
        A = lhs(inner)
        B = rhs(inner)
        new_branch = rest()
        new_branch += [A, "~" + B]
        return [new_branch]
    
    if t.startswith('~(') and inner_connective == '\\/':
        A = lhs(inner)
        B = rhs(inner)
        new_branch = rest()
        new_branch += ["~" + A, "~" + B]
        return [new_branch]

    if p in [5, 8] and inner_connective == '&':
        A = lhs(t)
        B = rhs(t)
        new_branch = rest()
        new_branch += [A, B]
        return [new_branch]
    
    # Beta expansions
    if t.startswith("~(") and inner_connective == '&':
        A = lhs(inner)
        B = rhs(inner)
        base = rest()
        return [base + ["~" + A], base + ["~" + B]]
    
    if p in [5, 8] and inner_connective == '->':
        A = lhs(t)
        B = rhs(t)
        base = rest()
        return [base + ["~" + A], base + [B]]
    
    if p in [5, 8] and inner_connective == '\\/':
        A = lhs(t)
        B = rhs(t)
        base = rest()
        return [base + [A], base + [B]]
    
    # Delta expansions
    if p == 4:
        var = t[1]
        sub_fmla = t[2:]
        base = rest()

        used_constants = set()
        for fmla in base:
            inner = fmla[1:] if fmla.startswith('~') else fmla
            if is_fol_atom(inner):
                used_constants.add(inner[2])
                used_constants.add(inner[4])

        new_const = None
        for c in "abcdefghijklmnopqrstuvwxyz":
            if c not in used_constants:
                new_const = c
                break
        if new_const is None:
            new_const = 'a'
        
        instance = sub_fmla.replace(var, new_const)
        return [base + [instance]]
    
    # Gamma expansions
    if p == 3:
        var = t[1]
        sub_fmla = t[2:]
        base = rest()

        constants = set()
        for fmla in base:
            inner = fmla[1:] if fmla.startswith('~') else fmla
            if is_fol_atom(inner):
                constants.add(inner[2])
                constants.add(inner[4])

        if not constants:
            constants = {'a'}

        instantiations = [sub_fmla.replace(var, c) for c in constants]
        return [base + instantiations]

    return [branch]
    
#------------------------------------------------------------------------------------------------------------------------------:
# Satisfiability Testing

def test_is_literal():
    assert is_literal('p')
    assert is_literal('q')
    assert is_literal('P(x,y)')
    assert is_literal('Q(w,x)')
    assert is_literal('R(z,z)')
    assert is_literal('~p')
    assert is_literal('~s')
    assert is_literal('~P(x,y)')
    assert is_literal('~Q(w,w)')
    assert is_literal('~Q(w,x)')
    assert not is_literal('(p&q)')
    assert not is_literal('~(p&q)')
    assert not is_literal('AxP(x,x)')
    assert not is_literal('(P(x,y)->Q(y,y))')
    print("is_literal: All tests passed.\n")

def test_branch_contradiction():
    assert not branch_contradiction(['p'])
    assert not branch_contradiction(['p', 'q'])
    assert not branch_contradiction(['P(x,y)'])
    assert not branch_contradiction(['P(x,y)', '~Q(x,x)'])
    assert branch_contradiction(['p', '~p'])
    assert branch_contradiction(['~p', 'p'])
    assert branch_contradiction(['P(x,y)', '~P(x,y)'])
    assert branch_contradiction(['~Q(z,z)', 'Q(z,z)'])
    assert branch_contradiction(['p', '(p->q)', '~q', '~p'])
    assert branch_contradiction(['P(x,y)', 'R(x,x)', '~R(x,x)'])
    assert not branch_contradiction(['(p->q)', '~(q&r)'])
    print("branch_contradiction: All tests passed.\n")

def beq(a, b):
    assert a == b, f"Actual {a} != Expected {b}"

def test_expand_alpha_and():
    b = ['(p&q)']
    beq(expand(b), [['p', 'q']])

def test_expand_alpha_neg_imp():
    b = ['~(p->q)']
    beq(expand(b), [['p', '~q']])

def test_expand_alpha_neg_or():
    b = ['~(p\\/q)']
    beq(expand(b), [['~p', '~q']])

def test_expand_beta_or():
    b = ['(p\\/q)']
    beq(expand(b), [['p'], ['q']])

def test_expand_beta_imp():
    b = ['(p->q)']
    beq(expand(b), [['~p'], ['q']])

def test_expand_beta_neg_and():
    b = ['~(p&q)']
    beq(expand(b), [['~p'], ['~q']])

def test_expand_delta():
    b = ['ExP(x,x)']
    out = expand(b)
    assert len(out) == 1
    br = out[0]
    assert any(is_fol_atom(f) and f[2] == 'a' for f in br)

def test_expand_delta_avoids_existing_const():
    b = ['P(a,a)', 'ExP(x,x)']
    out = expand(b)
    br = out[0]
    inst = [f for f in br if is_fol_atom(f) and f not in ['P(a,a)']]
    assert inst
    assert inst[0][2] != 'a'

def test_expand_gamma_with_existing_const():
    b = ['P(a,a)', 'AxP(x,x)']
    out = expand(b)
    br = out[0]
    assert 'P(a,a)' in br

def test_expand_gamma_no_const():
    b = ['AxP(x,x)']
    out = expand(b)
    br = out[0]
    assert 'P(a,a)' in br

def test_expand_noop():
    b = ['p', '~q']
    beq(expand(b), [b])

def test_expand():
    test_expand_alpha_and()
    test_expand_alpha_neg_imp()
    test_expand_alpha_neg_or()
    test_expand_beta_or()
    test_expand_beta_imp()
    test_expand_beta_neg_and()
    test_expand_delta()
    test_expand_delta_avoids_existing_const()
    test_expand_gamma_with_existing_const()
    test_expand_gamma_no_const()
    test_expand_noop()
    print("expand(): all tests passed.\n")

test_is_literal()
test_branch_contradiction()
test_expand()
print("================================\n\n")

# You may choose to represent a theory as a set or a list
def theory(fmla: str) -> list[str]:  # initialise a theory with a single formula in it
    return [fmla]

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