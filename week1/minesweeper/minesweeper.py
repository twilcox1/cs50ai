import itertools
import random
from collections import deque



class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        return self.cells if len(self.cells) == self.count else set()


    def known_safes(self):
        return self.cells if self.count == 0 else set()
    

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1


    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)



class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        if cell in self.mines:
            return
        self.mines.add(cell)
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.mark_mine(cell)

    def mark_safe(self, cell):
        if cell in self.safes:
            return
        self.safes.add(cell)
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        print("curren safes:", self.safes)
        print("current mines:", self.mines)
        self.moves_made.add(cell)
        self.mark_safe(cell)
        sentence = self.build_sentence(cell, count)
        if sentence and sentence not in self.knowledge:
            self.knowledge.append(sentence)
        self.clear_empty()
        self.check_knowledge()
        return
    

    def build_sentence(self, cell, count):
        grid = {
            (i, j)
            for i in range(cell[0] - 1, cell[0] + 2)
            for j in range(cell[1] - 1, cell[1] + 2)
            if (i, j) != cell and 0 <= i < self.height and 0 <= j < self.width
            if (i, j) not in self.safes
        }
        mines = grid & self.mines
        new_count = count - len(mines)
        grid -= mines
        if grid:
            return Sentence(grid, new_count)
        else:
            return None
    
    def check_knowledge(self):
        queue = deque(self.knowledge)
        for q in queue:
            print(q)
        while queue:
            current_sentence = queue.popleft()
            if current_sentence.count == 0:
                for cell in list(current_sentence.cells):
                    self.mark_safe(cell)
                    continue
            if len(current_sentence.cells) == current_sentence.count:
                for cell in list(current_sentence.cells):
                    self.mark_mine(cell)
                    continue
            for known_sentence in list(self.knowledge):
                if (known_sentence == current_sentence):
                    continue
                new_sentence = self.subset_check(current_sentence, known_sentence)
                if not new_sentence:
                        print("nonetype")
                        continue
                elif len(new_sentence.cells) == 0:
                    continue
                if new_sentence in self.knowledge:
                    continue
                print(new_sentence)
                self.knowledge.append(new_sentence)
                if len(new_sentence.cells) == new_sentence.count:
                    for cell in list(new_sentence.cells):
                        self.mark_mine(cell)
                if new_sentence.count == 0:
                    for cell in list(new_sentence.cells):
                        self.mark_safe(cell)
                self.clear_empty()
                queue.append(new_sentence)
        return

        
    def subset_check(self, setone, settwo):
        print("setone:",setone.cells, "settwo:", settwo.cells)
        if setone.cells.issubset(settwo.cells):
            print("setone is subset of settwo")
            setone, settwo = settwo, setone
        if settwo.cells.issubset(setone.cells) and setone.cells != settwo.cells:
            print("settwo is a subset of setone")
            new_cells = setone.cells - settwo.cells
            new_count = setone.count - settwo.count
            if new_cells and new_count >= 0:
                new_sentence = Sentence(new_cells, new_count)
                print("newsent created")
                return new_sentence
        else:
            return None
        
    def clear_empty(self):
            self.knowledge = [sentence for sentence in self.knowledge if len(sentence.cells) > 0 and len(sentence.cells) >= sentence.count >= 0]

    def make_safe_move(self):
        for move in self.safes:
            if move not in self.moves_made and move not in self.mines:
                return move
        return None


    def make_random_move(self):
        random_moves = [(i, j) for i in range(self.height) for j in range(self.width) if (i, j) not in self.moves_made and (i, j) not in self.mines]
        if not random_moves:
            return None
        move = random.choice(random_moves)
        return move

