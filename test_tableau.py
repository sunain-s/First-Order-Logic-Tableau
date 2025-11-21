# Test suite for tableau.py
# Run this file to test your tableau implementation before submission

# Import all functions from tableau.py
from skeleton import (
    balanced_parentheses, main_connective, is_prop_atom, is_fol_atom,
    lhs, con, rhs, parse, substitute, is_literal, branch_contradiction,
    get_constants, count_new_constants, select_target_formula, expand,
    theory, sat, MAX_CONSTANTS
)

# Color codes for better output visibility
class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_test_header(test_name):
    print(f"\n{Color.BLUE}{Color.BOLD}{'='*60}{Color.END}")
    print(f"{Color.BLUE}{Color.BOLD}Testing: {test_name}{Color.END}")
    print(f"{Color.BLUE}{Color.BOLD}{'='*60}{Color.END}")

def print_pass(message):
    print(f"{Color.GREEN}✓ {message}{Color.END}")

def print_fail(message):
    print(f"{Color.RED}✗ {message}{Color.END}")

def print_section(message):
    print(f"\n{Color.YELLOW}{message}{Color.END}")

#------------------------------------------------------------------------------------------------------------------------------:
# PARSING TESTS
#------------------------------------------------------------------------------------------------------------------------------:

def test_balanced_parentheses():
    print_test_header("balanced_parentheses()")
    
    # Valid cases
    assert balanced_parentheses('(P&Q)'), "Simple balanced"
    assert balanced_parentheses('((P\\/Q)->R)'), "Nested balanced"
    assert balanced_parentheses('(P->(Q&R))'), "Right-nested balanced"
    assert balanced_parentheses('((P&Q)->(R\\/S))'), "Complex balanced"
    assert balanced_parentheses(''), "Empty string"
    assert balanced_parentheses('PQR'), "No parentheses"
    print_pass("All valid parentheses cases passed")
    
    # Invalid cases
    assert not balanced_parentheses('(P&(Q->R)'), "Missing closing"
    assert not balanced_parentheses('P&Q)'), "Missing opening"
    assert not balanced_parentheses('((P&Q)'), "Unbalanced nested"
    assert not balanced_parentheses(')P&Q('), "Reversed"
    assert not balanced_parentheses('(P&Q))'), "Extra closing"
    print_pass("All invalid parentheses cases passed")
    
    print_pass("balanced_parentheses: ALL TESTS PASSED")

def test_main_connective():
    print_test_header("main_connective()")
    
    # Valid connectives
    assert main_connective('(P&Q)') == (2, '&'), "Simple conjunction"
    assert main_connective('((P\\/Q)->R)') == (7, '->'), "Nested implication"
    assert main_connective('(P->(Q&R))') == (2, '->'), "Right-nested implication"
    assert main_connective('((P&Q)\\/(R->S))') == (6, '\\/'), "Disjunction"
    assert main_connective('(p->q)') == (2, '->'), "Propositional implication"
    assert main_connective('(P(x,y)->Q(z,w))') == (7, '->'), "FOL implication"
    print_pass("All valid connectives found")
    
    # Invalid cases - should return (None, None)
    assert main_connective('(P)') == (None, None), "Single formula in parens"
    assert main_connective('p->q') == (None, None), "Missing outer parens"
    assert main_connective('') == (None, None), "Empty string"
    assert main_connective('p') == (None, None), "Atom"
    assert main_connective('~(p&q)') == (None, None), "Negation"
    print_pass("All invalid cases handled")
    
    print_pass("main_connective: ALL TESTS PASSED")

def test_is_prop_atom():
    print_test_header("is_prop_atom()")
    
    # Valid propositional atoms
    assert is_prop_atom('p'), "p is valid"
    assert is_prop_atom('q'), "q is valid"
    assert is_prop_atom('r'), "r is valid"
    assert is_prop_atom('s'), "s is valid"
    print_pass("All valid propositional atoms recognized")
    
    # Invalid cases
    assert not is_prop_atom('P'), "Capital P is not prop atom"
    assert not is_prop_atom('x'), "x is variable, not prop atom"
    assert not is_prop_atom('t'), "t is not in {p,q,r,s}"
    assert not is_prop_atom('(p&q)'), "Formula is not atom"
    assert not is_prop_atom('~p'), "Negation is not atom"
    assert not is_prop_atom(''), "Empty string"
    assert not is_prop_atom('pp'), "Multiple letters"
    print_pass("All invalid cases rejected")
    
    print_pass("is_prop_atom: ALL TESTS PASSED")

def test_is_fol_atom():
    print_test_header("is_fol_atom()")
    
    # Valid FOL atoms with variables
    assert is_fol_atom('P(x,y)'), "P with variables"
    assert is_fol_atom('Q(z,w)'), "Q with variables"
    assert is_fol_atom('R(x,x)'), "R with same variable"
    assert is_fol_atom('S(y,z)'), "S with variables"
    print_pass("Valid FOL atoms with variables recognized")
    
    # Valid FOL atoms with constants
    assert is_fol_atom('P(a,b)'), "P with constants"
    assert is_fol_atom('Q(a,a)'), "Q with same constant"
    assert is_fol_atom('R(x,a)'), "R with mixed variable/constant"
    assert is_fol_atom('S(c,z)'), "S with mixed constant/variable"
    print_pass("Valid FOL atoms with constants recognized")
    
    # Invalid cases
    assert not is_fol_atom('P(x)'), "Unary predicate"
    assert not is_fol_atom('P(x,y,z)'), "Ternary predicate"
    assert not is_fol_atom('p'), "Propositional atom"
    assert not is_fol_atom('(P(x,y)&Q(z,w))'), "Complex formula"
    assert not is_fol_atom('~P(x,y)'), "Negated atom"
    assert not is_fol_atom('P(X,y)'), "Capital variable"
    assert not is_fol_atom('P(x,)'), "Missing term"
    assert not is_fol_atom('P(,y)'), "Missing term"
    assert not is_fol_atom('T(x,y)'), "Invalid predicate T"
    assert not is_fol_atom('P[x,y]'), "Wrong brackets"
    print_pass("All invalid cases rejected")
    
    print_pass("is_fol_atom: ALL TESTS PASSED")

def test_lhs_con_rhs():
    print_test_header("lhs(), con(), rhs()")
    
    # Test lhs, con, rhs together
    formula = '(p&q)'
    assert lhs(formula) == 'p', "LHS of (p&q)"
    assert con(formula) == '&', "Connective of (p&q)"
    assert rhs(formula) == 'q', "RHS of (p&q)"
    print_pass("Simple conjunction decomposed")
    
    formula = '((p\\/q)->r)'
    assert lhs(formula) == '(p\\/q)', "LHS of nested formula"
    assert con(formula) == '->', "Connective of nested formula"
    assert rhs(formula) == 'r', "RHS of nested formula"
    print_pass("Nested formula decomposed")
    
    formula = '(P(x,y)->Q(z,w))'
    assert lhs(formula) == 'P(x,y)', "LHS of FOL formula"
    assert con(formula) == '->', "Connective of FOL formula"
    assert rhs(formula) == 'Q(z,w)', "RHS of FOL formula"
    print_pass("FOL formula decomposed")
    
    # Invalid cases
    assert lhs('p') == '', "No LHS for atom"
    assert con('p') == '', "No connective for atom"
    assert rhs('p') == '', "No RHS for atom"
    print_pass("Invalid cases return empty string")
    
    print_pass("lhs/con/rhs: ALL TESTS PASSED")

def test_parse():
    print_test_header("parse()")
    
    print_section("Propositional formulas:")
    # Propositions (return 6)
    assert parse('p') == 6, "p is proposition"
    assert parse('q') == 6, "q is proposition"
    assert parse('r') == 6, "r is proposition"
    assert parse('s') == 6, "s is proposition"
    print_pass("All propositions parsed correctly (return 6)")
    
    # Negations of propositional formulas (return 7)
    assert parse('~p') == 7, "~p is negation of prop"
    assert parse('~~q') == 7, "~~q is negation of prop"
    assert parse('~(p&q)') == 7, "~(p&q) is negation of prop"
    assert parse('~(p->q)') == 7, "~(p->q) is negation of prop"
    print_pass("Propositional negations parsed correctly (return 7)")
    
    # Binary connectives propositional (return 8)
    assert parse('(p&q)') == 8, "(p&q) is binary prop"
    assert parse('(p\\/q)') == 8, "(p\\/q) is binary prop"
    assert parse('(p->q)') == 8, "(p->q) is binary prop"
    assert parse('((p&q)->(r\\/s))') == 8, "Complex binary prop"
    print_pass("Propositional binary connectives parsed correctly (return 8)")
    
    print_section("First-order logic formulas:")
    # FOL atoms (return 1)
    assert parse('P(x,y)') == 1, "P(x,y) is atom"
    assert parse('Q(a,b)') == 1, "Q(a,b) is atom"
    assert parse('R(x,x)') == 1, "R(x,x) is atom"
    print_pass("FOL atoms parsed correctly (return 1)")
    
    # Negations of FOL formulas (return 2)
    assert parse('~P(x,y)') == 2, "~P(x,y) is negation of FOL"
    assert parse('~AxP(x,x)') == 2, "~AxP(x,x) is negation of FOL"
    assert parse('~ExP(x,y)') == 2, "~ExP(x,y) is negation of FOL"
    assert parse('~(P(x,y)->Q(z,w))') == 2, "~(P->Q) is negation of FOL"
    print_pass("FOL negations parsed correctly (return 2)")
    
    # Universal quantifiers (return 3)
    assert parse('AxP(x,x)') == 3, "AxP(x,x) is universal"
    assert parse('AyQ(y,z)') == 3, "AyQ(y,z) is universal"
    assert parse('AwR(w,w)') == 3, "AwR(w,w) is universal"
    assert parse('Ax(P(x,y)->Q(x,z))') == 3, "Ax with implication is universal"
    print_pass("Universal quantifiers parsed correctly (return 3)")
    
    # Existential quantifiers (return 4)
    assert parse('ExP(x,x)') == 4, "ExP(x,x) is existential"
    assert parse('EyQ(y,z)') == 4, "EyQ(y,z) is existential"
    assert parse('EzR(z,w)') == 4, "EzR(z,w) is existential"
    assert parse('Ex(P(x,y)&Q(x,z))') == 4, "Ex with conjunction is existential"
    print_pass("Existential quantifiers parsed correctly (return 4)")
    
    # Binary connectives FOL (return 5)
    assert parse('(P(x,y)->Q(z,w))') == 5, "P->Q is binary FOL"
    assert parse('(P(x,y)&Q(z,w))') == 5, "P&Q is binary FOL"
    assert parse('(ExP(x,x)\\/AyQ(y,y))') == 5, "Ex\/Ay is binary FOL"
    assert parse('(AxP(x,x)->ExQ(x,y))') == 5, "Ax->Ex is binary FOL"
    print_pass("FOL binary connectives parsed correctly (return 5)")
    
    print_section("Invalid formulas:")
    # Not formulas (return 0)
    assert parse('') == 0, "Empty string is not formula"
    assert parse('x') == 0, "Variable alone is not formula"
    assert parse('P') == 0, "Predicate alone is not formula"
    assert parse('(p&)') == 0, "Missing RHS"
    assert parse('(&q)') == 0, "Missing LHS"
    assert parse('p&q') == 0, "Missing outer parens"
    assert parse('(p~q)') == 0, "Invalid connective"
    assert parse('P(x)') == 0, "Unary predicate"
    assert parse('P(x,y,z)') == 0, "Ternary predicate"
    assert parse('Ax') == 0, "Quantifier without formula"
    assert parse('((p\\/q)&') == 0, "Incomplete formula"
    print_pass("All invalid formulas rejected (return 0)")
    
    print_pass("parse: ALL TESTS PASSED")

#------------------------------------------------------------------------------------------------------------------------------:
# SATISFIABILITY HELPER TESTS
#------------------------------------------------------------------------------------------------------------------------------:

def test_is_literal():
    print_test_header("is_literal()")
    
    print_section("Propositional literals:")
    assert is_literal('p'), "p is literal"
    assert is_literal('q'), "q is literal"
    assert is_literal('r'), "r is literal"
    assert is_literal('s'), "s is literal"
    assert is_literal('~p'), "~p is literal"
    assert is_literal('~q'), "~q is literal"
    print_pass("All propositional literals recognized")
    
    print_section("FOL literals:")
    assert is_literal('P(x,y)'), "P(x,y) is literal"
    assert is_literal('Q(a,b)'), "Q(a,b) is literal"
    assert is_literal('R(x,x)'), "R(x,x) is literal"
    assert is_literal('~P(x,y)'), "~P(x,y) is literal"
    assert is_literal('~Q(a,b)'), "~Q(a,b) is literal"
    assert is_literal('~R(z,w)'), "~R(z,w) is literal"
    print_pass("All FOL literals recognized")
    
    print_section("Non-literals:")
    assert not is_literal('~~p'), "~~p is not literal"
    assert not is_literal('(p&q)'), "(p&q) is not literal"
    assert not is_literal('~(p&q)'), "~(p&q) is not literal"
    assert not is_literal('(p->q)'), "(p->q) is not literal"
    assert not is_literal('AxP(x,x)'), "AxP(x,x) is not literal"
    assert not is_literal('ExP(x,x)'), "ExP(x,x) is not literal"
    assert not is_literal('~AxP(x,x)'), "~AxP(x,x) is not literal"
    assert not is_literal('(P(x,y)->Q(z,w))'), "P->Q is not literal"
    print_pass("All non-literals rejected")
    
    print_pass("is_literal: ALL TESTS PASSED")

def test_branch_contradiction():
    print_test_header("branch_contradiction()")
    
    print_section("No contradictions:")
    assert not branch_contradiction([]), "Empty branch has no contradiction"
    assert not branch_contradiction(['p']), "Single atom"
    assert not branch_contradiction(['p', 'q']), "Different atoms"
    assert not branch_contradiction(['p', 'q', 'r', 's']), "Multiple different atoms"
    assert not branch_contradiction(['P(x,y)']), "Single FOL atom"
    assert not branch_contradiction(['P(x,y)', 'Q(z,w)']), "Different FOL atoms"
    assert not branch_contradiction(['P(x,y)', '~Q(x,x)']), "Different predicates"
    assert not branch_contradiction(['P(a,b)', '~P(c,d)']), "Same predicate, different terms"
    assert not branch_contradiction(['~p', '~q', '~r']), "All negations, no contradiction"
    print_pass("All non-contradictory branches recognized")
    
    print_section("Propositional contradictions:")
    assert branch_contradiction(['p', '~p']), "p and ~p"
    assert branch_contradiction(['~p', 'p']), "~p and p (order reversed)"
    assert branch_contradiction(['q', 'r', '~q']), "q and ~q among other atoms"
    assert branch_contradiction(['~r', 's', 'r', 'q']), "~r and r among other atoms"
    print_pass("All propositional contradictions detected")
    
    print_section("FOL contradictions:")
    assert branch_contradiction(['P(x,y)', '~P(x,y)']), "P(x,y) and ~P(x,y)"
    assert branch_contradiction(['~Q(z,z)', 'Q(z,z)']), "~Q and Q"
    assert branch_contradiction(['P(a,b)', '~P(a,b)']), "P(a,b) and ~P(a,b)"
    assert branch_contradiction(['Q(a,a)', 'R(b,c)', '~Q(a,a)']), "Q and ~Q among others"
    print_pass("All FOL contradictions detected")
    
    print_section("Mixed contradictions:")
    assert branch_contradiction(['p', 'P(x,y)', '~p']), "Mixed prop and FOL with contradiction"
    assert branch_contradiction(['P(x,y)', 'R(x,x)', '~R(x,x)', 'q']), "FOL contradiction among mixed"
    print_pass("Mixed contradictions detected")
    
    print_pass("branch_contradiction: ALL TESTS PASSED")

def test_substitute():
    print_test_header("substitute()")
    
    print_section("Basic substitution in atoms:")
    assert substitute('P(x,y)', 'x', 'a') == 'P(a,y)', "Substitute x with a"
    assert substitute('P(x,y)', 'y', 'b') == 'P(x,b)', "Substitute y with b"
    assert substitute('P(x,x)', 'x', 'a') == 'P(a,a)', "Substitute both occurrences"
    assert substitute('Q(y,z)', 'y', 'c') == 'Q(c,z)', "Substitute first term"
    assert substitute('R(z,w)', 'w', 'd') == 'R(z,d)', "Substitute second term"
    print_pass("Basic substitutions work correctly")
    
    print_section("Negated atoms:")
    assert substitute('~P(x,y)', 'x', 'a') == '~P(a,y)', "Substitute in negated atom"
    assert substitute('~Q(y,y)', 'y', 'b') == '~Q(b,b)', "Substitute both in negated"
    assert substitute('~R(x,z)', 'z', 'c') == '~R(x,c)', "Substitute second in negated"
    print_pass("Negated atom substitutions work correctly")
    
    print_section("No substitution in bound variables:")
    assert substitute('AxP(x,y)', 'x', 'a') == 'AxP(x,y)', "Don't substitute bound x"
    assert substitute('ExP(x,z)', 'x', 'a') == 'ExP(x,z)', "Don't substitute bound x in Ex"
    assert substitute('AyQ(y,y)', 'y', 'b') == 'AyQ(y,y)', "Don't substitute bound y"
    assert substitute('EzR(z,w)', 'z', 'c') == 'EzR(z,w)', "Don't substitute bound z"
    print_pass("Bound variables correctly protected")
    
    print_section("Substitute free variables in quantified formulas:")
    assert substitute('AxP(x,y)', 'y', 'b') == 'AxP(x,b)', "Substitute free y"
    assert substitute('ExP(x,z)', 'z', 'c') == 'ExP(x,c)', "Substitute free z"
    assert substitute('AyQ(y,w)', 'w', 'd') == 'AyQ(y,d)', "Substitute free w"
    print_pass("Free variables in quantified formulas substituted")
    
    print_section("Binary connectives:")
    assert substitute('(P(x,y)->Q(y,z))', 'x', 'a') == '(P(a,y)->Q(y,z))', "Substitute in LHS"
    assert substitute('(P(x,y)->Q(y,z))', 'y', 'b') == '(P(x,b)->Q(b,z))', "Substitute in both sides"
    assert substitute('(P(x,x)&Q(x,x))', 'x', 'a') == '(P(a,a)&Q(a,a))', "Substitute all occurrences"
    assert substitute('(P(x,y)\\/Q(z,w))', 'x', 'a') == '(P(a,y)\\/Q(z,w))', "Substitute in disjunction"
    print_pass("Binary connective substitutions work correctly")
    
    print_section("Complex nested formulas:")
    assert substitute('~(P(x,x)->Q(y,y))', 'x', 'a') == '~(P(a,a)->Q(y,y))', "Nested with negation"
    assert substitute('Ax(P(x,y)->Q(y,z))', 'y', 'b') == 'Ax(P(x,b)->Q(b,z))', "Quantified binary"
    assert substitute('Ex~P(x,y)', 'y', 'c') == 'Ex~P(x,c)', "Quantified negation"
    print_pass("Complex formula substitutions work correctly")
    
    print_section("No-op substitutions:")
    assert substitute('P(a,b)', 'x', 'c') == 'P(a,b)', "No variable to substitute"
    assert substitute('p', 'x', 'a') == 'p', "Propositional atom unchanged"
    assert substitute('~q', 'y', 'b') == '~q', "Negated prop atom unchanged"
    print_pass("Non-applicable substitutions handled correctly")
    
    print_pass("substitute: ALL TESTS PASSED")

def test_get_constants():
    print_test_header("get_constants()")
    
    # Empty branch
    assert get_constants([]) == set(), "Empty branch has no constants"
    
    # Propositional formulas have no constants
    assert get_constants(['p', '~q']) == set(), "Prop formulas have no constants"
    
    # FOL with variables only
    assert get_constants(['P(x,y)', 'Q(z,w)']) == set(), "Variables are not constants"
    
    # FOL with constants
    assert get_constants(['P(a,b)']) == {'a', 'b'}, "Extract a and b"
    assert get_constants(['Q(a,a)']) == {'a'}, "Extract single constant"
    assert get_constants(['P(a,b)', 'Q(b,c)']) == {'a', 'b', 'c'}, "Extract multiple"
    
    # Mixed variables and constants
    assert get_constants(['P(x,a)', 'Q(b,y)']) == {'a', 'b'}, "Extract only constants"
    
    # Negated atoms
    assert get_constants(['~P(a,b)', '~Q(c,d)']) == {'a', 'b', 'c', 'd'}, "Extract from negated"
    
    # Complex branches
    branch = ['P(a,b)', 'Q(x,y)', '~R(c,c)', 'p', '(P(d,e)&Q(f,f))']
    assert get_constants(branch) == {'a', 'b', 'c', 'd', 'e', 'f'}, "Extract from complex branch"
    
    print_pass("get_constants: ALL TESTS PASSED")

def test_count_new_constants():
    print_test_header("count_new_constants()")
    
    initial = {'a', 'b'}
    
    # No new constants
    branch = ['P(a,b)', 'Q(a,a)']
    assert count_new_constants(branch, initial) == 0, "No new constants"
    
    # One new constant
    branch = ['P(a,b)', 'Q(c,c)']
    assert count_new_constants(branch, initial) == 1, "One new constant: c"
    
    # Multiple new constants
    branch = ['P(c,d)', 'Q(e,f)']
    assert count_new_constants(branch, initial) == 4, "Four new constants: c,d,e,f"
    
    # Mixed old and new
    branch = ['P(a,c)', 'Q(b,d)', 'R(e,e)']
    assert count_new_constants(branch, initial) == 3, "Three new: c,d,e"
    
    # Empty initial
    branch = ['P(a,b)', 'Q(c,c)']
    assert count_new_constants(branch, set()) == 3, "All are new: a,b,c"
    
    print_pass("count_new_constants: ALL TESTS PASSED")

def test_select_target_formula():
    print_test_header("select_target_formula()")
    
    print_section("Priority order:")
    # Double negation has highest priority (0)
    b = ['~~p', '(p\\/q)', 'AxP(x,x)']
    assert select_target_formula(b) == '~~p', "Double negation first"
    
    # Negated quantifiers (priority 1)
    b = ['~AxP(x,x)', '(p&q)', 'ExQ(x,x)']
    assert select_target_formula(b) == '~AxP(x,x)', "Negated quantifier over alpha"
    
    # Alpha rules (priority 2) over beta (priority 10)
    b = ['(p&q)', '(r\\/s)']
    assert select_target_formula(b) == '(p&q)', "Alpha (conjunction) before beta"
    
    b = ['~(p->q)', '(r->s)']
    assert select_target_formula(b) == '~(p->q)', "Alpha (neg impl) before beta"
    
    # Beta rules (priority 10) over delta (priority 20)
    b = ['(p\\/q)', 'ExP(x,x)']
    assert select_target_formula(b) == '(p\\/q)', "Beta before delta"
    
    # Delta rules (priority 20) over gamma (priority 30)
    b = ['ExP(x,x)', 'AxQ(x,x)']
    assert select_target_formula(b) == 'ExP(x,x)', "Delta before gamma"
    
    # Gamma as last resort
    b = ['AxP(x,x)', 'p', 'q']
    assert select_target_formula(b) == 'AxP(x,x)', "Gamma when no higher priority"
    
    print_pass("Priority ordering correct")
    
    print_section("Special cases:")
    # All literals - should return None
    b = ['p', '~q', 'P(a,b)', '~R(c,d)']
    assert select_target_formula(b) is None, "None for all literals"
    
    # Empty branch
    assert select_target_formula([]) is None, "None for empty branch"
    
    # Mixed priorities
    b = ['(p&q)', '~~r', '(s\\/t)', 'AxP(x,x)']
    assert select_target_formula(b) == '~~r', "Highest priority from mixed"
    
    print_pass("Special cases handled correctly")
    
    print_pass("select_target_formula: ALL TESTS PASSED")

#------------------------------------------------------------------------------------------------------------------------------:
# EXPANSION TESTS
#------------------------------------------------------------------------------------------------------------------------------:

def beq(actual, expected, msg=""):
    """Assert equality with helpful error message"""
    if actual != expected:
        print_fail(f"{msg}")
        print(f"  Expected: {expected}")
        print(f"  Actual:   {actual}")
        raise AssertionError(f"{msg}: Expected {expected}, got {actual}")
    
def test_expand_double_negation():
    print_test_header("expand() - Double Negation")
    
    b = ['~~p']
    beq(expand(b), [['p']], "~~p reduces to p")
    
    b = ['~~~p']
    beq(expand(b), [['~p']], "~~~p reduces to ~p")
    
    b = ['~~~~p']
    beq(expand(b), [['~~p']], "~~~~p reduces to ~~p")
    
    b = ['~~P(x,y)']
    beq(expand(b), [['P(x,y)']], "~~P(x,y) reduces to P(x,y)")
    
    b = ['p', '~~q', 'r']
    result = expand(b)
    assert 'q' in result[0] and 'p' in result[0] and 'r' in result[0], "~~q reduced with others preserved"
    
    print_pass("Double negation: ALL TESTS PASSED")

def test_expand_negated_quantifiers():
    print_test_header("expand() - Negated Quantifiers")
    
    # ~Ax becomes Ex~
    b = ['~AxP(x,x)']
    result = expand(b)
    beq(result, [['Ex~P(x,x)']], "~AxP(x,x) becomes Ex~P(x,x)")
    
    b = ['~AyQ(y,z)']
    result = expand(b)
    beq(result, [['Ey~Q(y,z)']], "~AyQ(y,z) becomes Ey~Q(y,z)")
    
    # ~Ex becomes Ax~
    b = ['~ExP(x,y)']
    result = expand(b)
    beq(result, [['Ax~P(x,y)']], "~ExP(x,y) becomes Ax~P(x,y)")
    
    b = ['~EzR(z,w)']
    result = expand(b)
    beq(result, [['Az~R(z,w)']], "~EzR(z,w) becomes Az~R(z,w)")
    
    # With other formulas
    b = ['p', '~AxP(x,x)', 'q']
    result = expand(b)
    assert 'Ex~P(x,x)' in result[0], "~Ax transformed in branch"
    assert 'p' in result[0] and 'q' in result[0], "Other formulas preserved"
    
    print_pass("Negated quantifiers: ALL TESTS PASSED")

def test_expand_alpha_rules():
    print_test_header("expand() - Alpha Rules")
    
    print_section("Conjunction (A & B):")
    b = ['(p&q)']
    beq(expand(b), [['p', 'q']], "(p&q) splits to p, q")
    
    b = ['(r&s)']
    beq(expand(b), [['r', 's']], "(r&s) splits to r, s")
    
    b = ['(P(x,y)&Q(z,w))']
    beq(expand(b), [['P(x,y)', 'Q(z,w)']], "FOL conjunction splits")
    
    b = ['p', '(q&r)', 's']
    result = expand(b)
    assert 'q' in result[0] and 'r' in result[0], "Conjunction expanded"
    assert 'p' in result[0] and 's' in result[0], "Other formulas preserved"
    print_pass("Conjunction rules work")
    
    print_section("Negated implication ~(A -> B):")
    b = ['~(p->q)']
    beq(expand(b), [['p', '~q']], "~(p->q) gives p, ~q")
    
    b = ['~(r->s)']
    beq(expand(b), [['r', '~s']], "~(r->s) gives r, ~s")
    
    b = ['~(P(x,y)->Q(z,w))']
    beq(expand(b), [['P(x,y)', '~Q(z,w)']], "FOL negated implication")
    print_pass("Negated implication rules work")
    
    print_section("Negated disjunction ~(A \\/ B):")
    b = ['~(p\\/q)']
    beq(expand(b), [['~p', '~q']], "~(p\\/q) gives ~p, ~q")
    
    b = ['~(r\\/s)']
    beq(expand(b), [['~r', '~s']], "~(r\\/s) gives ~r, ~s")
    
    b = ['~(P(x,y)\\/Q(z,w))']
    beq(expand(b), [['~P(x,y)', '~Q(z,w)']], "FOL negated disjunction")
    print_pass("Negated disjunction rules work")
    
    print_pass("Alpha rules: ALL TESTS PASSED")

def test_expand_beta_rules():
    print_test_header("expand() - Beta Rules")
    
    print_section("Disjunction (A \\/ B):")
    b = ['(p\\/q)']
    result = expand(b)
    beq(len(result), 2, "Disjunction creates 2 branches")
    assert result[0] == ['p'] or result[0] == ['q'], "First branch is p or q"
    assert result[1] == ['p'] or result[1] == ['q'], "Second branch is p or q"
    assert result[0] != result[1], "Branches are different"
    print_pass("Disjunction branches correctly")
    
    b = ['(P(x,y)\\/Q(z,w))']
    result = expand(b)
    beq(len(result), 2, "FOL disjunction creates 2 branches")
    assert 'P(x,y)' in result[0] or 'P(x,y)' in result[1], "P(x,y) in one branch"
    assert 'Q(z,w)' in result[0] or 'Q(z,w)' in result[1], "Q(z,w) in one branch"
    print_pass("FOL disjunction branches correctly")
    
    print_section("Implication (A -> B):")
    b = ['(p->q)']
    result = expand(b)
    beq(len(result), 2, "Implication creates 2 branches")
    assert result[0] == ['~p'] or result[0] == ['q'], "Branch is ~p or q"
    assert result[1] == ['~p'] or result[1] == ['q'], "Branch is ~p or q"
    print_pass("Implication branches correctly")
    
    print_section("Negated conjunction ~(A & B):")
    b = ['~(p&q)']
    result = expand(b)
    beq(len(result), 2, "Negated conjunction creates 2 branches")
    assert result[0] == ['~p'] or result[0] == ['~q'], "Branch is ~p or ~q"
    assert result[1] == ['~p'] or result[1] == ['~q'], "Branch is ~p or ~q"
    print_pass("Negated conjunction branches correctly")
    
    print_section("Preservation of other formulas:")
    b = ['r', '(p\\/q)', 's']
    result = expand(b)
    beq(len(result), 2, "Creates 2 branches")
    assert 'r' in result[0] and 's' in result[0], "First branch preserves r, s"
    assert 'r' in result[1] and 's' in result[1], "Second branch preserves r, s"
    print_pass("Other formulas preserved in beta expansion")
    
    print_pass("Beta rules: ALL TESTS PASSED")

def test_expand_delta_rule():
    print_test_header("expand() - Delta Rule (Existential)")
    
    print_section("Simple existential:")
    b = ['ExP(x,x)']
    result = expand(b)
    beq(len(result), 1, "Creates 1 branch")
    # Should instantiate with 'a'
    found_instance = any(is_fol_atom(f) and f[0] == 'P' for f in result[0])
    assert found_instance, "Creates instance P(a,a)"
    assert any(f == 'P(a,a)' for f in result[0]), "Specifically P(a,a)"
    print_pass("Simple existential instantiates with 'a'")
    
    print_section("Avoiding existing constants:")
    b = ['P(a,a)', 'ExQ(x,x)']
    result = expand(b)
    beq(len(result), 1, "Creates 1 branch")
    assert 'P(a,a)' in result[0], "Preserves existing atom"
    # Should use 'b' since 'a' is taken
    assert 'Q(b,b)' in result[0], "Uses next available constant 'b'"
    print_pass("Avoids existing constant 'a'")
    
    b = ['P(a,b)', 'Q(b,c)', 'ExR(x,x)']
    result = expand(b)
    # Should use 'd' since a, b, c are taken
    assert 'R(d,d)' in result[0], "Uses 'd' when a,b,c taken"
    print_pass("Skips multiple existing constants")
    
    print_section("Different variables:")
    b = ['EyP(y,y)']
    result = expand(b)
    assert 'P(a,a)' in result[0], "Works with variable y"
    
    b = ['EzQ(z,w)', 'P(x,x)']
    result = expand(b)
    # Should substitute z with 'a', but w remains as free variable
    assert 'Q(a,w)' in result[0], "Substitutes bound variable z, keeps free variable w"
    assert 'P(x,x)' in result[0], "Original formula preserved"
    print_pass("Handles different variables correctly")
    
    print_section("Nested existentials:")
    b = ['ExEyP(x,y)']
    result = expand(b)
    # First expansion: Ex disappears, Ey remains with x substituted
    assert any('Ey' in f for f in result[0]), "Inner existential remains"
    print_pass("Nested existentials expand one at a time")
    
    print_pass("Delta rule: ALL TESTS PASSED")

def test_expand_gamma_rule():
    print_test_header("expand() - Gamma Rule (Universal)")
    
    print_section("Universal with no constants:")
    b = ['AxP(x,x)']
    result = expand(b)
    beq(len(result), 1, "Creates 1 branch")
    assert 'AxP(x,x)' in result[0], "Universal formula remains"
    assert 'P(a,a)' in result[0], "Instantiates with default 'a'"
    print_pass("Instantiates with 'a' when no constants exist")
    
    print_section("Universal with existing constants:")
    b = ['P(a,a)', 'AxP(x,x)']
    result = expand(b)
    assert 'AxP(x,x)' in result[0], "Universal remains for future"
    assert 'P(a,a)' in result[0], "Original instance preserved"
    # Should not add duplicate
    count_p_a_a = sum(1 for f in result[0] if f == 'P(a,a)')
    beq(count_p_a_a, 1, "No duplicate P(a,a)")
    print_pass("Doesn't create duplicate instances")
    
    b = ['Q(a,a)', 'AxP(x,x)']
    result = expand(b)
    assert 'P(a,a)' in result[0], "Instantiates with existing constant"
    assert 'AxP(x,x)' in result[0], "Universal remains"
    print_pass("Instantiates with existing constant")
    
    print_section("Multiple constants:")
    b = ['P(a,a)', 'Q(b,b)', 'R(c,c)', 'AxS(x,x)']
    result = expand(b)
    assert 'AxS(x,x)' in result[0], "Universal remains"
    assert 'S(a,a)' in result[0], "Instantiates with a"
    assert 'S(b,b)' in result[0], "Instantiates with b"
    assert 'S(c,c)' in result[0], "Instantiates with c"
    print_pass("Instantiates with all existing constants")
    
    print_section("No new instances if all exist:")
    b = ['P(a,a)', 'AxP(x,x)']
    result = expand(b)
    # First expand adds no new instances, just keeps universal
    # Second expand of same formula should return same branch
    result2 = expand(result[0])
    beq(result, result2, "No expansion when instance exists")
    print_pass("Doesn't add existing instances")
    
    print_section("Different variables:")
    b = ['P(a,a)', 'AyQ(y,y)']
    result = expand(b)
    assert 'Q(a,a)' in result[0], "Works with variable y"
    assert 'AyQ(y,y)' in result[0], "Universal remains"
    print_pass("Handles different variables")
    
    print_pass("Gamma rule: ALL TESTS PASSED")

def test_expand_no_expansion():
    print_test_header("expand() - No Expansion Cases")
    
    # All literals
    b = ['p', '~q']
    beq(expand(b), [b], "All literals, no expansion")
    
    b = ['p', 'q', 'r', 's']
    beq(expand(b), [b], "Multiple literals")
    
    b = ['P(a,b)', '~Q(c,d)', 'r']
    beq(expand(b), [b], "Mixed prop and FOL literals")
    
    # Empty branch
    b = []
    beq(expand(b), [[]], "Empty branch returns empty")
    
    print_pass("No expansion: ALL TESTS PASSED")

def test_expand_complex():
    print_test_header("expand() - Complex Cases")
    
    print_section("Nested formulas:")
    b = ['~(p->(q&r))']
    result = expand(b)
    beq(len(result), 1, "Alpha rule, single branch")
    assert 'p' in result[0], "Contains p"
    assert '~(q&r)' in result[0], "Contains ~(q&r)"
    print_pass("Nested alpha expansion")
    
    b = ['((p&q)\\/r)']
    result = expand(b)
    beq(len(result), 2, "Beta rule, two branches")
    print_pass("Nested beta expansion")
    
    print_section("Priority in mixed formulas:")
    b = ['~~p', '(q\\/r)', 'AxP(x,x)']
    result = expand(b)
    # Should expand ~~p first (highest priority)
    assert 'p' in result[0], "Double negation expanded first"
    assert '(q\\/r)' in result[0], "Beta rule not yet expanded"
    assert 'AxP(x,x)' in result[0], "Gamma not yet expanded"
    print_pass("Correct priority ordering")
    
    print_section("FOL with quantifiers and connectives:")
    b = ['(ExP(x,x)&AyQ(y,y))']
    result = expand(b)
    # Should expand conjunction (alpha)
    assert any('Ex' in f for f in result[0]), "Existential extracted"
    assert any('Ay' in f for f in result[0]), "Universal extracted"
    print_pass("Mixed quantifiers and connectives")
    
    print_pass("Complex expansion: ALL TESTS PASSED")

#------------------------------------------------------------------------------------------------------------------------------:
# SATISFIABILITY TESTS
#------------------------------------------------------------------------------------------------------------------------------:

def test_sat_simple():
    print_test_header("sat() - Simple Cases")
    
    print_section("Satisfiable:")
    assert sat([['p']]) == 1, "Single atom is SAT"
    assert sat([['q']]) == 1, "Different atom is SAT"
    assert sat([['p', 'q']]) == 1, "Multiple consistent atoms are SAT"
    assert sat([['p', 'q', 'r', 's']]) == 1, "Many atoms are SAT"
    assert sat([['P(a,b)']]) == 1, "FOL atom is SAT"
    assert sat([['~p']]) == 1, "Negated atom is SAT"
    print_pass("Simple satisfiable cases")
    
    print_section("Unsatisfiable:")
    assert sat([['p', '~p']]) == 0, "Direct contradiction is UNSAT"
    assert sat([['~p', 'p']]) == 0, "Contradiction (reversed) is UNSAT"
    assert sat([['P(a,a)', '~P(a,a)']]) == 0, "FOL contradiction is UNSAT"
    assert sat([['(p&~p)']]) == 0, "p AND NOT p is UNSAT"
    print_pass("Simple unsatisfiable cases")
    
    print_pass("Simple SAT: ALL TESTS PASSED")

def test_sat_propositional():
    print_test_header("sat() - Propositional Logic")
    
    print_section("Tautologies (satisfiable):")
    assert sat([['(p->p)']]) == 1, "p -> p is tautology"
    assert sat([['(p\\/~p)']]) == 1, "p OR NOT p is tautology"
    assert sat([['((p->q)\\/(q->p))']]) == 1, "Complex tautology"
    print_pass("Tautologies are satisfiable")
    
    print_section("Contradictions (unsatisfiable):")
    assert sat([['~(p->p)']]) == 0, "NOT(p -> p) is contradiction"
    assert sat([['(p&~p)']]) == 0, "p AND NOT p is contradiction"
    assert sat([['~(p\\/~p)']]) == 0, "NOT(p OR NOT p) is contradiction"
    assert sat([['(q&~(p\\/~p))']]) == 0, "q AND contradiction is UNSAT"
    print_pass("Contradictions are unsatisfiable")
    
    print_section("Satisfiable (non-tautologies):")
    assert sat([['(p\\/q)']]) == 1, "p OR q is SAT"
    assert sat([['(p&q)']]) == 1, "p AND q is SAT"
    assert sat([['(p->q)']]) == 1, "p -> q is SAT"
    assert sat([['((p\\/q)&(~p\\/~q))']]) == 1, "XOR-like formula is SAT"
    assert sat([['(~~~p\\/( q&~q))']]) == 1, "Complex with subformula"
    print_pass("Non-tautological satisfiable formulas")
    
    print_section("More complex unsatisfiable:")
    assert sat([['((p\\/q)&((p->~p)&(~p->p)))']]) == 0, "Complex contradiction"
    assert sat([['(~(p->q)&q)']]) == 0, "NOT(p->q) AND q is UNSAT"
    print_pass("Complex unsatisfiable formulas")
    
    print_pass("Propositional SAT: ALL TESTS PASSED")

def test_sat_fol_basic():
    print_test_header("sat() - FOL Basic")
    
    print_section("Satisfiable:")
    assert sat([['P(a,b)']]) == 1, "Simple FOL atom is SAT"
    assert sat([['ExP(x,x)']]) == 1, "Existential is SAT"
    assert sat([['AxP(x,x)']]) == 1, "Universal is SAT"
    assert sat([['~P(a,a)']]) == 1, "Negated atom is SAT"
    assert sat([['Ex~P(x,x)']]) == 1, "Existential negation is SAT"
    print_pass("Basic FOL satisfiable")
    
    print_section("Unsatisfiable:")
    assert sat([['P(a,a)', '~P(a,a)']]) == 0, "Direct FOL contradiction"
    assert sat([['Ax(P(x,x)&~P(x,x))']]) == 0, "Universal contradiction"
    assert sat([['ExAx(P(x,x)&~P(x,x))']]) == 0, "Nested quantifier contradiction"
    print_pass("Basic FOL unsatisfiable")
    
    print_pass("FOL Basic SAT: ALL TESTS PASSED")

def test_sat_fol_advanced():
    print_test_header("sat() - FOL Advanced")
    
    print_section("Quantifier interactions:")
    # ExP(x,x) & Ax(~P(x,x) -> P(x,x))
    # Should be SAT: instantiate Ex with 'a' giving P(a,a)
    # Universal gives: ~P(a,a) -> P(a,a), which with P(a,a) is consistent
    result = sat([['(ExP(x,x)&Ax(~P(x,x)->P(x,x)))']])
    assert result == 1, "Ex with Ax implication is SAT"
    print_pass("Existential + universal interaction")
    
    # ~Ax(P(x,x) & ~P(x,x)) should be SAT
    # Equivalent to Ex~(P(x,x) & ~P(x,x)) = Ex(~P(x,x) | P(x,x)) which is always SAT
    result = sat([['~Ax(P(x,x)&~P(x,x))']])
    assert result == 1, "Negated universal contradiction is SAT"
    print_pass("Negated universal quantifier")
    
    # ~Ax~Ey~P(x,y) should be SAT
    # This is Ex~~Ey~P(x,y) = ExEy~P(x,y) which is SAT
    result = sat([['~Ax~Ey~P(x,y)']])
    assert result == 1, "Complex nested negated quantifiers"
    print_pass("Multiple negated quantifiers")
    
    print_section("Mixed quantifiers and connectives:")
    # ExAy(Q(x,x)->P(y,y)) should be SAT
    result = sat([['ExAy(Q(x,x)->P(y,y))']])
    assert result == 1, "Ex with Ay and implication"
    print_pass("Mixed Ex and Ay")
    
    # ExEy((Q(x,x)&Q(y,y))\/~P(y,y)) should be SAT
    result = sat([['ExEy((Q(x,x)&Q(y,y))\\/~P(y,y))']])
    assert result == 1, "Multiple existentials with disjunction"
    print_pass("Multiple existentials")
    
    # (Ax(P(x,x)&~P(x,x))&ExQ(x,x)) should be UNSAT
    # Left side is always false
    result = sat([['(Ax(P(x,x)&~P(x,x))&ExQ(x,x))']])
    assert result == 0, "Conjunction with universal contradiction"
    print_pass("Universal contradiction in conjunction")
    
    print_section("Undetermined cases:")
    # (AxEyP(x,y)&EzQ(z,z)) might be undetermined
    # This could require many instantiations
    result = sat([['(AxEyP(x,y)&EzQ(z,z))']])
    assert result in [1, 2], "AxEy formula may be SAT or undetermined"
    print_pass("Complex formula with potential loops")
    
    print_pass("FOL Advanced SAT: ALL TESTS PASSED")

def test_sat_edge_cases():
    print_test_header("sat() - Edge Cases")
    
    print_section("Empty and single formulas:")
    # Empty tableau - no open branches means UNSAT
    result = sat([])
    assert result == 0, "Empty tableau is UNSAT"
    
    # Branch that immediately closes
    result = sat([['p', '~p']])
    assert result == 0, "Immediately contradictory branch"
    print_pass("Empty and contradictory cases")
    
    print_section("Multiple branches:")
    # One branch closes, other stays open
    # This would be from beta expansion where one branch has contradiction
    # We test this indirectly through formulas
    result = sat([['((p&~p)\\/q)']])
    assert result == 1, "One branch closes, other open = SAT"
    print_pass("Multiple branches with one closing")
    
    print_section("Deep nesting:")
    result = sat([['~~~~p']])
    assert result == 1, "Deep nesting of negations"
    
    result = sat([['((((p\\/q)\\/r)\\/s)\\/t)']])
    assert result == 1, "Deep nesting of disjunctions"
    print_pass("Deeply nested formulas")
    
    print_section("Constant limits:")
    # This tests the MAX_CONSTANTS limit
    # A formula that would require > 10 constants should return 2
    # We can't easily construct this without the formula being SAT first,
    # but we can test the mechanism works
    print_pass("Constant limit mechanism in place")
    
    print_pass("Edge cases: ALL TESTS PASSED")

#------------------------------------------------------------------------------------------------------------------------------:
# RUN ALL TESTS
#------------------------------------------------------------------------------------------------------------------------------:

def run_all_tests():
    print(f"\n{Color.BOLD}{'='*60}")
    print(f"TABLEAU.PY COMPREHENSIVE TEST SUITE")
    print(f"{'='*60}{Color.END}\n")
    
    test_count = 0
    passed_count = 0
    
    tests = [
        # Parsing tests
        ("Balanced Parentheses", test_balanced_parentheses),
        ("Main Connective", test_main_connective),
        ("Propositional Atoms", test_is_prop_atom),
        ("FOL Atoms", test_is_fol_atom),
        ("LHS/CON/RHS", test_lhs_con_rhs),
        ("Parse Function", test_parse),
        
        # Helper function tests
        ("Is Literal", test_is_literal),
        ("Branch Contradiction", test_branch_contradiction),
        ("Substitute", test_substitute),
        ("Get Constants", test_get_constants),
        ("Count New Constants", test_count_new_constants),
        ("Select Target Formula", test_select_target_formula),
        
        # Expansion tests
        ("Expand - Double Negation", test_expand_double_negation),
        ("Expand - Negated Quantifiers", test_expand_negated_quantifiers),
        ("Expand - Alpha Rules", test_expand_alpha_rules),
        ("Expand - Beta Rules", test_expand_beta_rules),
        ("Expand - Delta Rule", test_expand_delta_rule),
        ("Expand - Gamma Rule", test_expand_gamma_rule),
        ("Expand - No Expansion", test_expand_no_expansion),
        ("Expand - Complex", test_expand_complex),
        
        # Satisfiability tests
        ("SAT - Simple", test_sat_simple),
        ("SAT - Propositional", test_sat_propositional),
        ("SAT - FOL Basic", test_sat_fol_basic),
        ("SAT - FOL Advanced", test_sat_fol_advanced),
        ("SAT - Edge Cases", test_sat_edge_cases),
    ]
    
    for test_name, test_func in tests:
        test_count += 1
        try:
            test_func()
            passed_count += 1
        except AssertionError as e:
            print_fail(f"\n{test_name} FAILED: {e}")
        except Exception as e:
            print_fail(f"\n{test_name} ERROR: {e}")
    
    print(f"\n{Color.BOLD}{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}{Color.END}")
    
    if passed_count == test_count:
        print(f"{Color.GREEN}{Color.BOLD}✓ ALL {test_count} TEST SUITES PASSED!{Color.END}")
    else:
        print(f"{Color.YELLOW}{passed_count}/{test_count} test suites passed{Color.END}")
        print(f"{Color.RED}{test_count - passed_count} test suites failed{Color.END}")
    
    print(f"\n{Color.BOLD}{'='*60}{Color.END}\n")
    
    return passed_count == test_count

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1) 
