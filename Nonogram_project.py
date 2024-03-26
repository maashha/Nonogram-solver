import pycosat
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class NonogramSolver:
    def __init__(self, rows, columns, all_rows, all_columns, solved, solutions):
        self.rows = rows
        self.columns = columns
        self.all_rows = all_rows
        self.all_columns = all_columns
        self.solved = solved
        self.solutions = solutions

    def load_from_file(self, file_name):
        line_number = 0
        self.rows = 0
        self.columns = 0
        self.all_rows = []  # the array of all blocks of filled cells in ROWS
        self.all_columns = []  # the array of all blocks of filled cells in COLUMNS
        if os.path.isfile(file_name):
            with open(file_name, "r") as file:
                for line in file:
                    line_number += 1
                    if line_number == 1:
                        self.rows = int(line.split(" ")[0])
                        self.columns = int(line.split(" ")[1])
                    elif line_number <= 1 + self.rows:
                        self.all_rows.append(list(map(int, line.split())))
                    else:
                        self.all_columns.append(list(map(int, line.split())))

    @staticmethod
    def existence(series, length, sizes, number):
        final, non_empty, uniqueness = [], [], []
        maximum = 0
        minimum = -1
        left = 0
        right = 0
        for group in range(len(series)):
            starting_positions = []
            if group == 0:
                left = 0
                right = length + 1 - sum(series[0:]) - len(series)
            else:
                # move borders on the length of the previous block
                left += series[group - 1] + 1
                right += series[group - 1] + 1
            for possible in range(left, right + 1):
                position = (possible + 1) + sizes + length * (number + group)
                # add all possible positions of the first cell of the block to one array
                starting_positions.append(position)
                non_empty.append(position)
                if maximum < position:
                    maximum = position
                if minimum > position or minimum == -1:
                    minimum = position
                for can in range(possible + 1, right + 1):
                    # exclude situations where one block has two starting cells
                    uniqueness.append([-position, -((can + 1) + sizes + length * (number + group))])
            final.append(starting_positions)  # all of such starting_positions for one row or column
        return [final, uniqueness, maximum, minimum, non_empty]

    @staticmethod
    def intersection(sets, lengths, amount):
        intersect = []
        for section_1 in range(len(sets)):
            for section_2 in range(section_1 + 1, len(sets)):  # choose two sets of starting positions of the blocks
                for first in range(len(sets[section_1])):
                    # add elements of the first array in pairs with elements of the second, excluding their intersection
                    for second in range(len(sets[section_2])):
                        if abs((sets[section_1][first]) - (sets[section_2][second])) % amount < sum(
                                lengths[section_1:section_2]) + (section_2 - section_1) and abs(
                                (sets[section_1][first]) - (sets[section_2][second])) >= amount:
                            intersect.append([-(sets[section_1][first]), -(sets[section_2][second])])
                            if first >= 3:
                                intersect.append([-(sets[section_1][first]), -(sets[section_2][first - 3])])
        return intersect

    @staticmethod
    def cell_rows(mx, lenn, start, mn, something, liine, pr):
        all_cells, no, empty, se, y = [], [], [], [], {}
        for i in range(start + 1, start + lenn + 1):
            cells = [-i]
            if i % lenn != 0:
                for j in range(mn + i % lenn - 1, mx + 1, lenn):
                    if j not in no and j not in something:
                        no.append([-j])
                    else:
                        cells.append(j)
                        for n in range(i, i + liine[(j - pr) // lenn]):
                            se.append([-j, n])
                            if n in y.keys():
                                y[n].append(j)
                            else:
                                y[n] = [-n, j]
                        empty.append([i, -j])
            else:
                for j in range(mn + lenn - 1, mx + 1, lenn):
                    if j not in no and j not in something:
                        no.append([-j])
                    else:
                        cells.append(j)
                        for n in range(i, i + liine[(j - pr) // lenn - 1]):
                            se.append([-j, n])
                            if n in y.keys():
                                y[n].append(j)
                            else:
                                y[n] = [-n, j]
                        empty.append([i, -j])
            all_cells.append(cells)
            all_cells = []
        return [se, empty, no, y]

    @staticmethod
    def cell_columns(mx, lenn, start, mn, something, amoun, liine, pr):
        all_cells, no, empty, se, yw = [], [], [], [], {}
        for i in range(start + 1, start + lenn + 1):
            yw[((i - 1) % lenn) * amoun + (i - 1) // lenn + 1] = [-(((i - 1) % lenn) * amoun + (i - 1) // lenn + 1)]
        for i in range(start + 1, start + lenn + 1):
            cells = [-(((i - 1) % lenn) * amoun + (i - 1) // lenn + 1)]
            if i % lenn != 0:
                until = 0
                remainder = i % lenn
            else:
                until = -1
                remainder = lenn
            for j in range(mn + remainder - 1, mx + 1, lenn):
                if j not in no and j not in something:
                    no.append([-j])
                else:
                    cells.append(j)
                    for n in range(i, i + liine[(j - pr) // lenn + until]):
                        se.append([-j, ((n - 1) % lenn) * amoun + (n - 1) // lenn + 1])
                        yw[((n - 1) % lenn) * amoun + (n - 1) // lenn + 1].append(j)
                    empty.append([((i - 1) % lenn) * amoun + (i - 1) // lenn + 1, -j])
            all_cells.append(cells)
        return [se, empty, no, yw]

    def adding(self, get):
        colored, emptys, nothing, d = get[0], get[1], get[2], get[3]
        for j in emptys:
            self.solutions.append(j)
        for j in colored:
            self.solutions.append(j)
        for j in nothing:
            self.solutions.append(j)
        for j in d:
            self.solutions.append(d[j])

    @staticmethod
    def adding_1(solution, att):
        transformed_solution = []
        for sublist in solution:
            transformed_sublist = []
            for elem in sublist:
                transformed_sublist.append(elem + att)
            transformed_solution.append(transformed_sublist)
        return transformed_solution

    def solve(self):
        previous = 0
        max_num = self.rows*self.columns
        for i in range(self.rows):
            blocks = self.all_rows[i]  # all filled in cells in the ith row
            if max_num % self.columns == 0:
                ma = max_num
            else:
                ma = max_num + (self.columns-max_num % self.columns)
            if blocks == [0]:  # case of the empty row
                for empty in range(i*self.columns+1, (i+1)*self.columns+1):
                    self.solutions.append([-empty])
                continue
            all_starts = self.existence(blocks, self.columns, self.rows*self.columns, previous)
            exist, unique_start, max_num, min_num = all_starts[0], all_starts[1], all_starts[2], all_starts[3]
            color = all_starts[4]
            for j in exist:
                self.solutions.append(j)
            for j in unique_start:
                self.solutions.append(j)
            for j in self.intersection(exist, blocks, self.columns):
                self.solutions.append(j)
            get = self.cell_rows(max_num, self.columns, i*self.columns, min_num, color, blocks, ma)
            self.adding(get)
            previous += len(blocks)
        previous = 0
        for column in range(self.columns):
            blocks = self.all_columns[column]
            got = self.existence(blocks, self.rows, self.rows*self.columns, previous)
            if column == 0:
                if max_num % self.columns == 0:
                    mm = max_num
                else:
                    mm = max_num + (self.columns-max_num % self.columns)
                att = mm-self.columns*self.rows
            if (max_num-att) % self.rows == 0:
                mm = max_num
            else:
                mm = max_num + (self.rows-(max_num-att) % self.rows)
            if blocks == [0]:
                for h in range(column*self.rows+1, column*self.rows+self.rows+1):
                    self.solutions.append([-(((h-1) % self.rows)*self.columns+(h-1)//self.rows+1)])
                continue
            solution_1, solution_2 = got[0], got[1]
            sol_1 = self.adding_1(solution_1, att)
            sol_2 = self.adding_1(solution_2, att)
            for i in solution_2:
                solution_2_1 = []
                for j in i:
                    solution_2_1.append(-(j*(-1)+att))
                sol_2.append(solution_2_1)
            solution_1, solution_2 = sol_1.copy(), sol_2.copy()
            max_num, min_num, color = got[2]+att, got[3]+att, got[4]
            colll = []
            for i in color:
                colll.append(i+att)
            color = colll.copy()
            for j in solution_1:
                self.solutions.append(j)
            for j in solution_2:
                self.solutions.append(j)
            for j in self.intersection(solution_1, blocks, self.rows):
                self.solutions.append(j)
            get = self.cell_columns(max_num, self.rows, column*self.rows, min_num, color, self.columns, blocks, mm)
            self.adding(get)
            previous += len(blocks)
        self.solved = pycosat.solve(self.solutions)

    def draw(self):
        fig, ax = plt.subplots()
        ax.plot()
        if self.solved != 'UNSAT':
            for i in range(self.rows*self.columns):
                if i % self.columns == (self.columns-1):
                    if self.solved[i] >= 0:
                        ax.add_patch(Rectangle((i % self.columns, self.rows-i//self.columns), 1, 1))
                else:
                    if self.solved[i] >= 0:
                        ax.add_patch(Rectangle((i % self.columns, self.rows-i//self.columns), 1, 1))
        plt.show()
