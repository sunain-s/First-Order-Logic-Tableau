
MAX_CONSTANTS = 10

#------------------------------------------------------------------------------------------------------------------------------:
# Helper Functions

def main_connective(fmla) -> tuple[int, str]:
    depth = 0
    i = 0
    while i < len(fmla):
        char = fmla[i]
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1

        # checking at highest level for the main connective
        elif depth == 1:
            if char == "&":
                return i, "&"
            elif char == "\\" and i + 1 < len(fmla) and fmla[i + 1] == "/":
                return i, "\\/"
            elif char == "-" and i + 1 < len(fmla) and fmla[i + 1] == ">":
                return i, "->"
        i += 1
    return None, None



#------------------------------------------------------------------------------------------------------------------------------:
# Testing Functions

def test_main_connective():
    assert main_connective('(P&Q)') == (2, '&')
    assert main_connective('((P\\/Q)->R)') == (7, '->')
    assert main_connective('(P->(Q&R))') == (2, '->')
    assert main_connective('(P)') == (None, None)
    assert main_connective('((P&Q)\\/ (R->S))') == (6, '\\/')
    print("All tests passed.")

test_main_connective()
print("================================\n\n\n")

#------------------------------------------------------------------------------------------------------------------------------:
# Main Tableau Functions

# Parse a formula, consult parseOutputs for return values.
def parse(fmla) -> int:
    return 0

# Return the LHS of a binary connective formula
def lhs(fmla) -> str:
    return ''

# Return the connective symbol of a binary connective formula
def con(fmla) -> str:
    return ''

# Return the RHS symbol of a binary connective formula
def rhs(fmla) -> str:
    return ''

# You may choose to represent a theory as a set or a list
def theory(fmla) -> list[str]:  # initialise a theory with a single formula in it
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