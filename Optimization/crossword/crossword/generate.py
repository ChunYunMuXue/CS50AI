import sys

from math import inf
from crossword import *
from copy import deepcopy

BACKTRACK_COUNTER = 0
WORDS_TESTED = 0

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self, interleaving):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        if not interleaving:
            print('Solving Crossword with single arc consistency enforcement...')
            return self.backtrack(dict())
        else:
            print('Solving Crossword with interleaved backtracking and arc consistency enforcement...')
            return self.backtrack_ac3(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # Iterate through all variables in the crossword
        for var in self.domains:
            var_len = var.length
            to_remove = set()

            # Iterate through all values in the variable's domain
            for val in self.domains[var]:
                # If value length does not match variable length, add to values to remove
                if len(val) != var_len:
                    to_remove.add(val)

            # Remove all invalide vals from variable domain
            self.domains[var] = self.domains[var] - to_remove

    def overlap_satisfied(self, x, y, val_x, val_y):
            """
            Helper function that returns true if val_x and val_y
            satisfy any overlap arc consistency requirement for
            variables x and y.

            Returns True if consistency is satisfied, False otherwise.
            """

            # If no overlap, no arc consistency to satisfy
            if not self.crossword.overlaps[x, y]:
                return True

            # Otherwise check that letters match at overlapping indices
            else:
                x_index, y_index = self.crossword.overlaps[x,y]

                if val_x[x_index] == val_y[y_index]:
                    return True
                else:
                    return False

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        revision = False
        to_remove = set()

        # Iterate over domain of x and y, track any inconsistent x:
        for val_x in self.domains[x]:
            consistent = False
            for val_y in self.domains[y]:
                if val_x != val_y and self.overlap_satisfied(x, y, val_x, val_y):
                    consistent = True
                    break

            if not consistent:
                to_remove.add(val_x)
                revision = True

        # Remove any domain variables that aren't arc consistent:
        self.domains[x] = self.domains[x] - to_remove
        return revision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # If no arcs, start with queue of all arcs:
        if not arcs:
            arcs = []
            for var_1 in self.domains:
                for var_2 in self.domains:
                    if var_1 != var_2:
                        arcs.append((var_1, var_2))

        # Continue until no arcs left (arc consistency enforced):
        while arcs:
            var_x, var_y = arcs.pop()
            # Revise x domain wrt y:
            if self.revise(var_x, var_y):
                # If x domain is empty after revision, no solution:
                if not self.domains[var_x]:
                    return False
                # If revised, add to arcs all x neighbors
                for var_z in self.crossword.neighbors(var_x) - {var_y}:
                    arcs.append((var_z, var_x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        for var in self.domains:
            if var not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        used_variables = []

        for var_x in assignment:
            val_x = assignment[var_x]

            # If the assigned word is already used, not consistent:
            if val_x in used_variables:
                return False
            used_variables.append(val_x)

            # Check if variable is assigned its length is correct
            if len(val_x) != var_x.length:
                return False

            # Check if there are conflicts between neighboring variables:
            for var_y in self.crossword.neighbors(var_x):
                if var_y in assignment:
                    val_y = assignment[var_y]

                    # Check if neighbor variable is assigned and satisfies constraints
                    if not self.overlap_satisfied(var_x, var_y, val_x, val_y):
                        return False

        # Otherwise all assignments are consistent
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        vals_ruleout = {val: 0 for val in self.domains[var]}

        # Iterate through all possible values of var:
        for val in self.domains[var]:

            # Iterate through neighboring variables and values:
            for other_var in self.crossword.neighbors(var):
                for other_val in self.domains[other_var]:

                    # If val rules out other val, add to ruled_out count
                    if not self.overlap_satisfied(var, other_var, val, other_val):
                        vals_ruleout[val] += 1

        # Return list of vals sorted from fewest to most other_vals ruled out:
        return sorted([x for x in vals_ruleout], key = lambda x: vals_ruleout[x])


        # SIMPLE, INEFFICIENT - RETURN IN ANY ORDER:
        #return [x for x in self.domains[var]]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # Get set of unassigned variables
        unassigned = set(self.domains.keys()) - set(assignment.keys())

        # Create list of variables, sorted by MRV and highest degree
        result = [var for var in unassigned]
        result.sort(key = lambda x: (len(self.domains[x]), -len(self.crossword.neighbors(x))))

        return result[0]


        # SIMPLE, INEFFICIENT - RETURN ANY VARIABLE:
        #return [var for var in unassigned][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        global BACKTRACK_COUNTER
        global WORDS_TESTED
        BACKTRACK_COUNTER += 1

        # If all variables are assigned, return assignment:
        if self.assignment_complete(assignment):
            return assignment

        # Otherwise select an unassigned variable:
        var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(var, assignment):
            assignment[var] = val
            WORDS_TESTED += 1
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            del assignment[var]
        return None

    def backtrack_ac3(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        Interleaves backtracking search with inference using ac3, to reduce
        the domains of each variable as assignments are made.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        global BACKTRACK_COUNTER
        global WORDS_TESTED
        BACKTRACK_COUNTER += 1

        # If all variables are assigned, return assignment:
        if self.assignment_complete(assignment):
            return assignment

        # Otherwise select an unassigned variable:
        var = self.select_unassigned_variable(assignment)
        pre_assignment_domains = deepcopy(self.domains)
        for val in self.order_domain_values(var, assignment):
            assignment[var] = val
            WORDS_TESTED += 1
            if self.consistent(assignment):
                # Update variable domain to be assigned value
                self.domains[var] = {val}
                # Use ac3 to remove inconcistent values from neighbouring variables
                self.ac3([(other_var, var) for other_var in self.crossword.neighbors(var)])
                result = self.backtrack_ac3(assignment)
                if result:
                    return result
            # If assignment does not produce solution, remove assignment and reset domains
            del assignment[var]
            self.domains = pre_assignment_domains
        return None

def main():

    # Check usage
    if len(sys.argv) not in [4, 5]:
        sys.exit("Usage: python generate.py structure words interleaving [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    interleaving = sys.argv[3] == 'True'
    output = sys.argv[4] if len(sys.argv) == 5 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve(interleaving)

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        print("Calls to backtrack function: ", BACKTRACK_COUNTER)
        print("Words tested to find solution: ", WORDS_TESTED)
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()