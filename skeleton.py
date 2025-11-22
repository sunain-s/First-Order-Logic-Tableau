MAX_CONSTANTS = 10

#------------------------------------------------------------------------------------------------------------------------------:
# Parsing Functions

def balanced_parentheses(fmla: str) -> bool:
    '''Check if parentheses in the formula are balanced'''
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
    '''Return index and type of the main connective of the formula'''
    if not fmla:
        return None, None
    if not (fmla.startswith("(") and fmla.endswith(")")):
        return None, None
    if not balanced_parentheses(fmla):
        return None, None

    depth = 0
    for i in range(len(fmla)):
        ch = fmla[i]
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        if depth == 1:
            if ch == '-' and i + 1 < len(fmla) and fmla[i + 1] == '>':
                return i, '->'
            if ch == '&':
                return i, '&'
            if ch == '\\' and i + 1 < len(fmla) and fmla[i + 1] == '/':
                return i, '\\/'
    return None, None

def is_prop_atom(fmla: str) -> bool:
    '''Must be one of {p, q, r, s}'''
    return fmla in ['p', 'q', 'r', 's']

def is_fol_atom(fmla: str) -> bool:
    '''Must match pattern P(t1,t2) where P in {P, Q, R, S} and t1,t2 are terms'''
    if len(fmla) != 6:
        return False
    if fmla[0] not in ['P', 'Q', 'R', 'S']:
        return False
    if fmla[1] != '(' or fmla[3] != ',' or fmla[5] != ')':
        return False
    
    VARS = ['x', 'y', 'z', 'w']
    CONSTS = [chr(c) for c in range(ord('a'), ord('z')+1)]
    TERMS = VARS + CONSTS
    return fmla[2] in TERMS and fmla[4] in TERMS

def lhs(fmla: str) -> str:
    '''Return left hand side of the main connective'''
    i, connective = main_connective(fmla)
    if i is None or connective is None:
        return ''
    return fmla[1:i]

def con(fmla: str) -> str:
    '''Return the main connective of the formula'''
    _, connective = main_connective(fmla)
    if connective is None:
        return ''
    return connective

def rhs(fmla: str) -> str:
    '''Return right hand side of the main connective'''
    i, connective = main_connective(fmla)
    if i is None or connective is None:
        return ''
    return fmla[i+len(connective):-1]

def parse(fmla: str) -> int:
    '''Parse the formula and return its output index'''
    if not fmla:
        return 0 # not a formula
    if ' ' in fmla or '\t' in fmla or '\n' in fmla:
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
    
    # Binary Connectives (only if enclosed in parentheses)
    if not balanced_parentheses(fmla):
        return 0 # not a formula

    if fmla.startswith('(') and fmla.endswith(')'):
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
            return 5 # a binary connective first order logic formula
        return 0 # not a formula  
    return 0 # not a formula

#------------------------------------------------------------------------------------------------------------------------------:
# Tableau Implementation

def is_literal(fmla: str) -> bool:
    '''Check if a formula is a literal (atom or negated atom)'''
    if is_fol_atom(fmla) or is_prop_atom(fmla):
        return True
    if fmla.startswith('~') and len(fmla) > 1:
        subfmla = fmla[1:]
        if is_fol_atom(subfmla) or is_prop_atom(subfmla):
            return True
    return False

def has_contradiction(formulas: list[str]) -> bool:
    '''Check for a contradiction in the branch list'''
    for fmla in formulas:
        if fmla.startswith('~'):
            if fmla[1:] in formulas:
                return True
        else:
            if '~' + fmla in formulas:
                return True
    return False

def get_constants(branch: list[str]) -> set:
    '''Recursively collect all constants in the branch'''
    constants = set()
    VARS = ['x', 'y', 'z', 'w']

    # Recursively enter formula and collect constants
    def collect(fmla: str):
        if not fmla:
            return
        
        if fmla.startswith('~'):
            collect(fmla[1:])
            return
        
        if is_fol_atom(fmla):
            t1, t2 = fmla[2], fmla[4]
            if t1 not in VARS:
                constants.add(t1)
            if t2 not in VARS:
                constants.add(t2)
            return
        
        if len(fmla) > 2 and fmla[0] in ['A', 'E'] and fmla[1] in VARS:
            collect(fmla[2:])
            return
        
        if fmla.startswith('(') and fmla.endswith(')'):
            connective = con(fmla)
            if connective:
                left = lhs(fmla)
                right = rhs(fmla)
                collect(left)
                collect(right)
                return
        return
    
    for fmla in branch:
        collect(fmla)
    return constants

def substitute(fmla: str, var: str, const: str) -> str:
    '''Substitute all free occurrences of var with const in fmla'''
    if not fmla:
        return fmla
    
    if fmla.startswith('~'):
        return '~' + substitute(fmla[1:], var, const)
    
    if is_fol_atom(fmla):
        P, t1, t2 = fmla[0], fmla[2], fmla[4]
        if t1 == var:
            t1 = const
        if t2 == var:
            t2 = const
        return f"{P}({t1},{t2})"
    
    if len(fmla) > 2 and fmla[0] in ['A', 'E'] and fmla[1] in ['x', 'y', 'z', 'w']:
        quant_var = fmla[1]
        if quant_var == var:
            return fmla  # Bound variable - don't substitute
        else:
            return fmla[0] + fmla[1] + substitute(fmla[2:], var, const)
    
    if fmla.startswith('(') and fmla.endswith(')'):
        left = lhs(fmla)
        right = rhs(fmla)
        connective = con(fmla)
        if left and right and connective:
            return '(' + substitute(left, var, const) + connective + substitute(right, var, const) + ')'
    return fmla

class TableauBranch:
    '''Represents a branch in the tableau with its formulas and applied gamma instances'''

    def __init__(self, formulas: list[str], gamma_instances: dict = None):
        self.formulas = formulas
        # Key: gamma formula, Value: set of constants instantiated with
        self.gamma_instances = gamma_instances if gamma_instances else {}
    
    def copy(self):
        return TableauBranch(self.formulas.copy(),
                             {k: v.copy() for k, v in self.gamma_instances.items()}
                             )
    
    def add_formula(self, fmla: str):
        if fmla not in self.formulas:
            self.formulas.append(fmla)
    
    def remove_formula(self, fmla: str):
        if fmla in self.formulas:
            self.formulas.remove(fmla)
    
    def has_gamma_instance(self, gamma_fmla: str, const: str) -> bool:
        '''Check if we already instantiated this gamma formula with this constant'''
        if gamma_fmla not in self.gamma_instances:
            return False
        return const in self.gamma_instances[gamma_fmla]
    
    def add_gamma_instance(self, gamma_fmla: str, const: str):
        '''Record that we instantiated this gamma formula with this constant'''
        if gamma_fmla not in self.gamma_instances:
            self.gamma_instances[gamma_fmla] = set()
        self.gamma_instances[gamma_fmla].add(const)

def select_target_formula(branch: TableauBranch) -> str | None:
    '''Find the next formula to expand, priority: double negation > negated quantifiers > alpha > beta > delta > gamma'''
    target = None
    priority = 1000 # lower number = higher priority
    for fmla in branch.formulas:
        if is_literal(fmla):
            continue
        current_priority = 1000

        # Double negations
        if fmla.startswith('~~'):
            current_priority = 0

        # Negated quantifiers
        elif fmla.startswith('~A') or fmla.startswith('~E'):
            if len(fmla) > 2 and fmla[2] in ['x', 'y', 'z', 'w']:
                current_priority = 1

        # Alpha rules
        elif fmla.startswith('~('):
            inner = fmla[1:]
            conn = con(inner) if inner.startswith('(') else ''
            if conn in ['->', '\\/']:
                current_priority = 2
        else:
            p = parse(fmla)
            if p in [5, 8] and con(fmla) == '&':
                current_priority = 2

        # Beta rules
        if current_priority == 1000:
            if fmla.startswith('~('):
                inner = fmla[1:]
                conn = con(inner) if inner.startswith('(') else ''
                if conn == '&':
                    current_priority = 10
            else:
                p = parse(fmla)
                if p in [5, 8] and con(fmla) in ['->', '\\/']:
                    current_priority = 10

        # Delta rule
        if current_priority == 1000 and parse(fmla) == 4:
            current_priority = 20

        # Gamma rule — only if there is a new instantiation available
        if current_priority == 1000 and parse(fmla) == 3:
            var = fmla[1]
            sub = fmla[2:]
            constants = get_constants(branch.formulas) or {'a'}
            for c in constants:
                if not branch.has_gamma_instance(fmla, c):
                    inst = substitute(sub, var, c)
                    if inst not in branch.formulas:
                        current_priority = 30
                        break

        if current_priority < priority:
            priority = current_priority
            target = fmla
    return target

def expand_tableau(branch: TableauBranch) -> list[TableauBranch]:
    '''Expand a formula in the branch'''
    target = select_target_formula(branch)
    if target is None:
        return [branch]
    p = parse(target)

    # Double negation
    if target.startswith('~~'):
        new_branch = branch.copy()
        new_branch.remove_formula(target)
        new_branch.add_formula(target[2:])
        return [new_branch]

    # Replacing negated quantifiers
    if target.startswith('~A') and len(target) > 2 and target[2] in ['x', 'y', 'z', 'w']:
        new_branch = branch.copy()
        new_branch.remove_formula(target)
        var = target[2]
        sub = target[3:]
        new_branch.add_formula(f"E{var}~{sub}")
        return [new_branch]

    if target.startswith('~E') and len(target) > 2 and target[2] in ['x', 'y', 'z', 'w']:
        new_branch = branch.copy()
        new_branch.remove_formula(target)
        var = target[2]
        sub = target[3:]
        new_branch.add_formula(f"A{var}~{sub}")
        return [new_branch]

    # Alpha expansions
    inner = target[1:] if target.startswith('~') else target
    conn = con(inner) if inner.startswith('(') and inner.endswith(')') else ''

    if target.startswith('~(') and conn == '->':
        new_branch = branch.copy()
        new_branch.remove_formula(target)
        new_branch.add_formula(lhs(inner))
        new_branch.add_formula('~' + rhs(inner))
        return [new_branch]

    if target.startswith('~(') and conn == '\\/':
        new_branch = branch.copy()
        new_branch.remove_formula(target)
        new_branch.add_formula('~' + lhs(inner))
        new_branch.add_formula('~' + rhs(inner))
        return [new_branch]

    if p in [5, 8] and conn == '&':
        new_branch = branch.copy()
        new_branch.remove_formula(target)
        new_branch.add_formula(lhs(target))
        new_branch.add_formula(rhs(target))
        return [new_branch]

    # Beta expansions
    if target.startswith('~(') and conn == '&':
        b1 = branch.copy()
        b1.remove_formula(target)
        b1.add_formula('~' + lhs(inner))
        b2 = branch.copy()
        b2.remove_formula(target)
        b2.add_formula('~' + rhs(inner))
        return [b1, b2]

    if p in [5, 8] and conn == '->':
        b1 = branch.copy()
        b1.remove_formula(target)
        b1.add_formula('~' + lhs(target))
        b2 = branch.copy()
        b2.remove_formula(target)
        b2.add_formula(rhs(target))
        return [b1, b2]

    if p in [5, 8] and conn == '\\/':
        b1 = branch.copy()
        b1.remove_formula(target)
        b1.add_formula(lhs(target))
        b2 = branch.copy()
        b2.remove_formula(target)
        b2.add_formula(rhs(target))
        return [b1, b2]

    # Delta expansions
    if p == 4:
        var = target[1]
        sub = target[2:]
        new_branch = branch.copy()
        new_branch.remove_formula(target)
        used = get_constants(new_branch.formulas)
        for c in "abcdefghijklmnopqrstuvwxyz":
            if c not in used:
                new_const = c
                break
        instance = substitute(sub, var, new_const)
        new_branch.add_formula(instance)
        return [new_branch]

    # Gamma expansions
    if p == 3:
        var = target[1]
        sub = target[2:]
        new_branch = branch.copy()
        constants = get_constants(new_branch.formulas) or {'a'}
        for c in constants:
            if not new_branch.has_gamma_instance(target, c):
                inst = substitute(sub, var, c)
                if inst not in new_branch.formulas:
                    new_branch.add_formula(inst)
                    new_branch.add_gamma_instance(target, c)
        return [new_branch]
    return [branch]

def theory(fmla: str) -> list[str]:
    return [fmla]

def sat(tableau) -> int:
    '''Determine satisfiability of a formula using tableau method'''
    if not tableau:
        return 0 # is not satisfiable
    
    branches = [TableauBranch(branch) for branch in tableau]
    initial_constants = set()
    for branch in branches:
        initial_constants.update(get_constants(branch.formulas))
    
    max_iterations = 10000
    iterations = 0
    while branches and iterations < max_iterations:
        iterations += 1
        new_branches = []
        for branch in branches:
            if has_contradiction(branch.formulas):
                continue  # Closed branch

            # Can change this to remove initial constants?
            current_constants = get_constants(branch.formulas)
            new_const_count = len(current_constants - initial_constants)
            if new_const_count > MAX_CONSTANTS:
                return 2 # may or may not be satisfiable
            
            expanded = expand_tableau(branch)
            if len(expanded) == 1 and expanded[0].formulas == branch.formulas:
                # Check if truly complete - all literals or only gamma with all instances
                all_expandable_done = True
                for fmla in branch.formulas:
                    if not is_literal(fmla):
                        if parse(fmla) == 3:
                            constants = get_constants(branch.formulas)
                            if not constants:
                                constants = {'a'}
                            var = fmla[1]
                            sub = fmla[2:]
                            for c in constants:
                                inst = substitute(sub, var, c)
                                if inst not in branch.formulas:
                                    all_expandable_done = False
                                    break
                        else:
                            all_expandable_done = False
                            break
                if all_expandable_done:
                    return 1 # is satisfiable
            new_branches.extend(expanded)
        branches = new_branches
        if not branches:
            return 0 # is not satisfiable
    
    # Timeout reached
    # Check if any branches are not closed
    for branch in branches:
        if not has_contradiction(branch.formulas):
            all_literals_or_gamma = True
            for fmla in branch.formulas:
                if not is_literal(fmla) and parse(fmla) != 3:
                    all_literals_or_gamma = False
                    break
            if all_literals_or_gamma:
                return 1 # is satisfiable
    return 2 # may or may not be satisfiable

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