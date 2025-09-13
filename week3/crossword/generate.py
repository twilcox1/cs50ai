import sys

from crossword import *
from itertools import permutations, combinations
from collections import deque


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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        for key, value in self.domains.items():
            length = key.length
            junk = {item for item in value if len(item) != length}
            self.domains[key] -= junk

    def revise(self, x, y):
        overlap_check = self.crossword.overlaps[x, y]
        if not overlap_check:
            return False
        xi, yi = overlap_check
        junk = set()
        print("domain values for", x)
        for xword in self.domains[x]:
            print(type(xword), xword)
            print(xword)
            if not any(xword[xi] == yword[yi] for yword in self.domains[y]):
                junk.add(xword)
        if junk:
            self.domains[x] -= junk
            return True
        else:
            return False


    def ac3(self, arcs=None):
        if arcs == []:
            return True
        if arcs is None:
            variables = self.crossword.variables
            arcs = list(permutations(variables, 2))
        queue = deque(arcs)
        while queue:
            current = queue.popleft()
            x, y = current
            check = self.revise(x, y)
            if self.domains[x] == set():
                return False
            neighbors = self.crossword.neighbors(x)
            if not check or not neighbors:
                continue
            queue.extend(((var, x) for var in neighbors if var != y))
        return True



    def assignment_complete(self, assignment):
        return set(assignment.keys()) == set(self.crossword.variables)



    def consistent(self, assignment):
        unique = True if len(set(assignment.values())) == len(assignment) else False
        if not unique:
            return False
        length_check = all(var.length == len(word) for var, word in assignment.items())
        if not length_check:
            return False
        neighbors = [
            ((x, y), overlap)
            for x, y in combinations(assignment.keys(), 2)
            if (overlap := self.crossword.overlaps[x, y]) is not None
        ]
        for (x, y), (i, j) in neighbors:
            x_value = assignment[x][i]
            y_value = assignment[y][j]
            if x_value != y_value:
                return False
        return True

    def order_domain_values(self, var, assignment):
        for k in self.domains.keys():
            print(type(k), k)
        print(self.domains[var])
        unordered = [x for x in self.domains[var]]
        score = dict.fromkeys(unordered, 0)
        neighbors = {x for x in self.crossword.neighbors(var) if x not in assignment}
        if not neighbors:
            return unordered
        n = {i: self.domains[i] for i in neighbors}
        print("!~", n, "~!")
        for variable in unordered:
            for key, value in n.items():
                overlap = self.crossword.overlaps[var, key]
                if overlap is None:
                    continue
                og, ng = overlap
                for string in value:  # string is a word from neighbor's domain
                    if string[ng] != variable[og]:
                        score[variable] += 1
                else:
                    continue
        return sorted(unordered, key=lambda w: score[w])
    




    def select_unassigned_variable(self, assignment):
        print(self.crossword.variables)
        print(assignment)
        unassigned = [x for x in self.crossword.variables if x not in assignment.keys()]
        print("~~~",unassigned,"~~~")
        score = {}
        for i in unassigned:
            score[i] = len(self.domains[i])
        print("unassigned",unassigned)
        print("score",score)
        return min(unassigned, key=lambda w: score[w])


    def backtrack(self, assignment):
        if self.assignment_complete(assignment):
            return assignment
        
        variable = self.select_unassigned_variable(assignment)
        for i in self.order_domain_values(variable, assignment):
            if self.consistent(assignment):
                assignment[variable] = i
                result = self.backtrack(assignment)
                if result: 
                    return result
            assignment.pop(var)
        return None
        



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
