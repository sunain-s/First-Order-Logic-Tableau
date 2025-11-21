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
    return fmla in ['p', 'q', 'r', 's']

def is_fol_atom(fmla: str) -> bool:
    # Must match: PRED(term, term) where term is variable or constant
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
            return 5 # a binary connective first order formula
        return 0 # not a formula
        
    return 0 # not a formula

#------------------------------------------------------------------------------------------------------------------------------:
# Satisfiability Functions

def substitute(fmla, var, const):
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
            return fmla
        else:
            return fmla[0] + fmla[1] + substitute(fmla[2:], var, const)
    
    if fmla.startswith('(') and fmla.endswith(')'):
        left = lhs(fmla)
        right = rhs(fmla)
        connective = con(fmla)
        if left and right and connective:
            return '(' + substitute(left, var, const) + connective + substitute(right, var, const) + ')'
    
    return fmla

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

def get_constants(branch: list[str]) -> set:
    constants = set()
    VARS = ['x', 'y', 'z', 'w']

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

def count_new_constants(branch: list[str], initial_constants: set) -> int:
    current_constants = get_constants(branch)
    return len(current_constants - initial_constants)

def select_target_formula(branch: list[str]) -> str | None:
    """
    Select the best formula to expand based on priority.
    Returns None if all formulas are literals (branch is complete).
    
    CRITICAL FIX: Check if gamma rules would produce new instances before selecting them.
    """
    target_fmla = None
    best_priority = 100
    
    current_constants = get_constants(branch)
    
    for fmla in branch:
        if is_literal(fmla):
            continue
        
        current_priority = 100
        
        # Double negation - highest priority
        if fmla.startswith('~~'):
            current_priority = 0
        
        # Negated quantifiers
        elif fmla.startswith('~A') or fmla.startswith('~E'):
            if len(fmla) > 2 and fmla[2] in ['x', 'y', 'z', 'w']:
                current_priority = 1
        
        # Alpha rules (don't branch)
        elif fmla.startswith('~('):
            inner = fmla[1:]
            inner_connective = con(inner) if inner.startswith('(') else ''
            if inner_connective in ['->', '\\/']:
                current_priority = 2
        else:
            p = parse(fmla)
            if p in [5, 8]:
                inner_connective = con(fmla)
                if inner_connective == '&':
                    current_priority = 2
        
        # Beta rules (branch)
        if current_priority == 100:
            if fmla.startswith('~('):
                inner = fmla[1:]
                inner_connective = con(inner) if inner.startswith('(') else ''
                if inner_connective == '&':
                    current_priority = 10
            else:
                p = parse(fmla)
                if p in [5, 8]:
                    inner_connective = con(fmla)
                    if inner_connective in ['->', '\\/']:
                        current_priority = 10
        
        # Delta rules (existential)
        if current_priority == 100:
            if parse(fmla) == 4:
                current_priority = 20
        
        # Gamma rules (universal) - CRITICAL FIX
        # Only select if it would produce NEW instances
        if current_priority == 100:
            if parse(fmla) == 3:
                var = fmla[1]
                sub = fmla[2:]
                # Check what instances would be produced
                constants = current_constants if current_constants else {'a'}
                instances = [substitute(sub, var, c) for c in constants]
                new_instances = [inst for inst in instances if inst not in branch]
                
                if new_instances:
                    current_priority = 30
                else:
                    # This gamma won't produce anything new - SKIP IT
                    continue
        
        if current_priority < best_priority:
            best_priority = current_priority
            target_fmla = fmla
    
    return target_fmla

def expand(branch: list[str], initial_constants: set = None) -> list[list[str]]:
    """Expand one formula in the branch using tableau rules"""
    if initial_constants is None:
        initial_constants = set()
    
    # Find the best formula to expand
    target_fmla = select_target_formula(branch)
    
    if target_fmla is None:
        return [branch]
    
    p = parse(target_fmla)
    
    def remove_target():
        new_branch = branch.copy()
        new_branch.remove(target_fmla)
        return new_branch
    
    inner = target_fmla[1:] if target_fmla.startswith('~') else target_fmla
    inner_connective = con(inner) if inner.startswith('(') and inner.endswith(')') else ''
    
    # Double negation
    if target_fmla.startswith('~~'):
        subfmla = target_fmla[2:]
        b = remove_target()
        return [[*b, subfmla]]
    
    # Negated quantifiers
    if target_fmla.startswith('~A') and len(target_fmla) > 2 and target_fmla[2] in ['x','y','z','w']:
        var = target_fmla[2]
        sub = target_fmla[3:]
        b = remove_target()
        new_fmla = f"E{var}~{sub}"
        return [[*b, new_fmla]]
    
    if target_fmla.startswith('~E') and len(target_fmla) > 2 and target_fmla[2] in ['x','y','z','w']:
        var = target_fmla[2]
        sub = target_fmla[3:]
        b = remove_target()
        new_fmla = f"A{var}~{sub}"
        return [[*b, new_fmla]]
    
    # Alpha expansions
    if target_fmla.startswith('~(') and inner_connective == '->':
        A = lhs(inner)
        B = rhs(inner)
        b = remove_target()
        return [[*b, A, "~"+B]]

    if target_fmla.startswith('~(') and inner_connective == '\\/':
        A = lhs(inner)
        B = rhs(inner)
        b = remove_target()
        return [[*b, "~"+A, "~"+B]]

    if p in [5, 8] and inner_connective == '&':
        A = lhs(inner)
        B = rhs(inner)
        b = remove_target()
        return [[*b, A, B]]

    # Beta expansions
    if target_fmla.startswith("~(") and inner_connective == '&':
        A = lhs(inner)
        B = rhs(inner)
        b = remove_target()
        return [[*b, "~"+A], [*b, "~"+B]]

    if p in [5, 8] and inner_connective == '->':
        A = lhs(inner)
        B = rhs(inner)
        b = remove_target()
        return [[*b, "~"+A], [*b, B]]

    if p in [5, 8] and inner_connective == '\\/':
        A = lhs(inner)
        B = rhs(inner)
        b = remove_target()
        return [[*b, A], [*b, B]]

    # Delta expansion
    if p == 4:
        var = target_fmla[1]
        sub = target_fmla[2:]
        base = remove_target()
        used = get_constants(base)
        
        new_const = None
        for c in "abcdefghijklmnopqrstuvwxyz":
            if c not in used:
                new_const = c
                break
        
        if new_const is None:
            new_const = 'a'
        instance = substitute(sub, var, new_const)
        return [[*base, instance]]

    # Gamma expansion - CRITICAL FIX
    if p == 3:
        var = target_fmla[1]
        sub = target_fmla[2:]
        base = branch.copy()  # Keep universal formula in branch
        
        constants = get_constants(base)
        
        if not constants:
            constants = {'a'}
        
        instances = [substitute(sub, var, c) for c in constants]
        new_instances = [inst for inst in instances if inst not in base]
        
        if new_instances:
            # FIXED: Return new_instances, not instances
            return [[*base, *new_instances]]
        else:
            # No new instances - return unchanged branch
            return [branch]

    return [branch]

# You may choose to represent a theory as a set or a list
def theory(fmla: str) -> list[str]:
    return [fmla]

def is_branch_complete(branch: list[str]) -> bool:
    """
    Check if a branch is complete (fully expanded).
    A branch is complete if there are NO formulas that can be expanded further.
    
    This means:
    - All literals: complete
    - Only universal quantifiers remain that have been fully instantiated: complete
    - Any other non-literal formula: not complete (needs expansion)
    """
    # Try to find a formula to expand
    target = select_target_formula(branch)
    
    # If no formula can be selected for expansion, the branch is complete
    return target is None

def sat(tableau) -> int:
    """
    Check for satisfiability using tableau method.
    CRITICAL FIXES:
    1. Added loop detection to prevent infinite loops
    2. Added progress tracking to detect when stuck
    3. Better handling of undetermined cases
    4. Proper completion check for branches with universal quantifiers
    """
    # Handle empty tableau
    if not tableau:
        return 0  # Empty tableau is unsatisfiable
    
    initial_constants = set()
    for branch in tableau:
        initial_constants.update(get_constants(branch))
    
    max_iterations = 10000
    iterations = 0
    seen_states = set()  # Track seen branch states
    
    while tableau and iterations < max_iterations:
        iterations += 1
        new_tableau = []
        
        for branch in tableau:
            # Check if branch is closed (has contradiction)
            if branch_contradiction(branch):
                continue  # Discard this branch
            
            # Check if we've exceeded the constant limit
            new_const_count = count_new_constants(branch, initial_constants)
            if new_const_count > MAX_CONSTANTS:
                return 2  # Undetermined
            
            # CRITICAL FIX: Check if branch is complete (not just all literals)
            if is_branch_complete(branch):
                # Found an open, complete branch = satisfiable
                return 1
            
            # Detect if we've seen this exact branch before
            branch_state = tuple(sorted(branch))
            if branch_state in seen_states:
                # We've seen this branch before - check if it's complete
                if is_branch_complete(branch):
                    return 1
                # Otherwise, we need more constants or it's undetermined
                return 2
            seen_states.add(branch_state)
            
            # Expand this branch
            expanded = expand(branch, initial_constants)
            
            # Check if expansion made progress
            if len(expanded) == 1 and expanded[0] == branch:
                # No progress - expansion returned same branch
                if is_branch_complete(branch):
                    return 1  # Complete and satisfiable
                else:
                    # Has non-complete formulas but can't expand - undetermined
                    return 2
            
            new_tableau.extend(expanded)
        
        # Update tableau
        tableau = new_tableau
        
        # If all branches closed
        if not tableau:
            return 0  # Not satisfiable
    
    # Hit iteration limit
    # Check if any remaining branch is complete and satisfiable
    for branch in tableau:
        if not branch_contradiction(branch) and is_branch_complete(branch):
            return 1
    
    return 2  # Undetermined

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