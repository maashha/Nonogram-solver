import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pysat.solvers import Solver
import itertools

class NonogramSolver:
    def __init__(self):
        self.rows = 0
        self.columns = 0
        self.row_blocks = []
        self.column_blocks = []
        self.solved_status = []
        self.solver = Solver()

    def load_from_file(self, file_name):
        line_number = 0
        self.rows, self.columns = 0, 0
        self.row_blocks, self.column_blocks = [], []  # an array of all blocks of filled cells in ROWS/COLUMNS
        if os.path.isfile(file_name):
            with open(file_name, "r") as file:
                for line in file:
                    line_number += 1
                    if line_number == 1:
                        self.rows = int(line.split(" ")[0])
                        self.columns = int(line.split(" ")[1])
                    elif line_number <= 1 + self.rows:
                        self.row_blocks.append(list(map(int, line.split())))
                    else:
                        self.column_blocks.append(list(map(int, line.split())))

    @staticmethod
    def __existence(block_sizes, length, sizes, number):
        all_positions, non_empty_positions, uniqueness_clauses = [], [], []
        max_position, min_position = 0, -1
        left_boundary, right_boundary = 0, 0
        for group_size in range(len(block_sizes)):
            starting_positions = []
            if group_size == 0:
                left_boundary = 0
                right_boundary = length + 1 - sum(block_sizes[0:]) - len(block_sizes)
            else:
                # move borders on the length of the previous block
                left_boundary += block_sizes[group_size - 1] + 1
                right_boundary += block_sizes[group_size - 1] + 1
            for possible in range(left_boundary, right_boundary + 1):
                position = (possible + 1) + sizes + length * (number + group_size)
                # add all possible positions of the first cell of the block to one array
                starting_positions.append(position)
                non_empty_positions.append(position)
                if max_position < position:
                    max_position = position
                if min_position > position or min_position == -1:
                    min_position = position
                for can in range(possible + 1, right_boundary + 1):
                    # exclude situations where one block has two starting cells
                    uniqueness_clauses.append([-position, -((can + 1) + sizes + length * (number + group_size))])
            all_positions.append(starting_positions)  # all of such starting_positions for one row or column
        return [all_positions, uniqueness_clauses, max_position, min_position, non_empty_positions]

    @staticmethod
    def __intersections(position_sets, block_lengths, amount):
        intersecting_clauses = []
        sections_set = itertools.combinations(range(len(position_sets)), 2)
        for section in sections_set:
            for first_position in range(len(position_sets[section[0]])):
                # add elements of the first array in pairs with elements of the second, excluding their intersection
                for second_position in range(len(position_sets[section[1]])):
                    if abs((position_sets[section[0]][first_position]) - (position_sets[section[1]][second_position])) % amount < sum(
                            block_lengths[section[0]:section[1]]) + (section[1] - section[0]) and abs(
                        (position_sets[section[0]][first_position]) - (position_sets[section[1]][second_position])) >= amount:
                        intersecting_clauses.append([-(position_sets[section[0]][first_position]), -(position_sets[section[1]][second_position])])
                        if first_position >= 3:
                            intersecting_clauses.append([-(position_sets[section[0]][first_position]), -(position_sets[section[1]][first_position - 3])])
        return intersecting_clauses

    @staticmethod
    def __match_row_cells(max_position, length, start, min_position, occupied_positions_rows, row_blocks, total_length):
        all_cells, unoccupied_positions, empty_cells, single_cells, row_mapping = [], [], [], [], {}
        for i in range(start + 1, start + length + 1):
            cells_in_row = [-i]
            if i % length != 0:
                for j in range(min_position + i % length - 1, max_position + 1, length):
                    if j not in unoccupied_positions and j not in occupied_positions_rows:
                        unoccupied_positions.append([-j])
                    else:
                        cells_in_row.append(j)
                        for n in range(i, i + row_blocks[(j - total_length) // length]):
                            single_cells.append([-j, n])
                            if n in row_mapping:
                                row_mapping[n].append(j)
                            else:
                                row_mapping[n] = [-n, j]
                        empty_cells.append([i, -j])
            else:
                for j in range(min_position + length - 1, max_position + 1, length):
                    if j not in unoccupied_positions and j not in occupied_positions_rows:
                        unoccupied_positions.append([-j])
                    else:
                        cells_in_row.append(j)
                        for n in range(i, i + row_blocks[(j - total_length) // length - 1]):
                            single_cells.append([-j, n])
                            if n in row_mapping:
                                row_mapping[n].append(j)
                            else:
                                row_mapping[n] = [-n, j]
                        empty_cells.append([i, -j])
            all_cells.append(cells_in_row)
            all_cells = []
        return [single_cells, empty_cells, unoccupied_positions, row_mapping]

    @staticmethod
    def __match_column_cells(max_position, length, start, min_position, occupied_positions_columns, total_columns, column_blocks, total_length):
        all_cells, unoccupied_positions, empty_cells, single_cells, column_mapping = [], [], [], [], {}
        for i in range(start + 1, start + length + 1):
            column_mapping[((i - 1) % length) * total_columns + (i - 1) // length + 1] = [-(((i - 1) % length) * total_columns + (i - 1) // length + 1)]
        for i in range(start + 1, start + length + 1):
            cells_in_column = [-(((i - 1) % length) * total_columns + (i - 1) // length + 1)]
            boundary, remainder = (0, i % length) if i % length != 0 else (-1, length)
            for j in range(min_position + remainder - 1, max_position + 1, length):
                if j not in unoccupied_positions and j not in occupied_positions_columns:
                    unoccupied_positions.append([-j])
                else:
                    cells_in_column.append(j)
                    for n in range(i, i + column_blocks[(j - total_length) // length + boundary]):
                        single_cells.append([-j, ((n - 1) % length) * total_columns + (n - 1) // length + 1])
                        column_mapping[((n - 1) % length) * total_columns + (n - 1) // length + 1].append(j)
                    empty_cells.append([((i - 1) % length) * total_columns + (i - 1) // length + 1, -j])
            all_cells.append(cells_in_column)
        return [single_cells, empty_cells, unoccupied_positions, column_mapping]

    def __add_to_solution_clauses(self, cells_info):
        colored_cells, empty_cells, unoccupied_cells, mapping = cells_info
        for clause in itertools.chain(empty_cells, colored_cells, unoccupied_cells, mapping.values()) :
            self.solver.add_clause(clause)

    def solve(self):
        previous_start_row = 0
        max_position = self.rows*self.columns
        for i in range(self.rows):
            blocks = self.row_blocks[i]  # all filled in cells in the ith row
            if max_position % self.columns == 0:
                max_row_position = max_position
            else:
                max_row_position = max_position + (self.columns-max_position % self.columns)
            if blocks == [0]:  # case of the empty row
                for empty in range(i*self.columns+1, (i+1)*self.columns+1):
                    self.solver.add_clause([-empty])
                continue
            all_starts = self.__existence(blocks, self.columns, self.rows*self.columns, previous_start_row)
            exist, unique_start, max_position, min_num = all_starts[0], all_starts[1], all_starts[2], all_starts[3]
            color = all_starts[4]
            for clause in exist:
                self.solver.add_clause(clause)
            for clause in unique_start:
                self.solver.add_clause(clause)
            for clause in self.__intersections(exist, blocks, self.columns):
                self.solver.add_clause(clause)
            row_cells_info = self.__match_row_cells(max_position, self.columns, i * self.columns, min_num, color, blocks, max_row_position)
            self.__add_to_solution_clauses(row_cells_info)
            previous_start_row += len(blocks)

        previous_start_column = 0
        for column in range(self.columns):
            blocks = self.column_blocks[column]
            got_info = self.__existence(blocks, self.rows, self.rows*self.columns, previous_start_column)
            if column == 0:
                if max_position % self.columns == 0:
                    max_column_position = max_position
                else:
                    max_column_position = max_position + (self.columns-max_position % self.columns)
                row_column_difference = max_column_position-self.columns*self.rows
            if (max_position-row_column_difference) % self.rows == 0:
                max_column_position = max_position
            else:
                max_column_position = max_position + (self.rows-(max_position-row_column_difference) % self.rows)
            if blocks == [0]:
                for h in range(column*self.rows+1, column*self.rows+self.rows+1):
                    self.solver.add_clause([-(((h-1) % self.rows)*self.columns+(h-1)//self.rows+1)])
                continue
            sol_1, sol_2 = [], []
            solution_1, solution_2 = got_info[0], got_info[1]
            for i in solution_1:
                solution_1_1 = []
                for j in i:
                    solution_1_1.append(j+row_column_difference)
                sol_1.append(solution_1_1)
            for i in solution_2:
                solution_2_1 = []
                for j in i:
                    solution_2_1.append(-(j*(-1)+row_column_difference))
                sol_2.append(solution_2_1)
            solution_1, solution_2 = sol_1.copy(), sol_2.copy()
            max_position, min_num, color = got_info[2]+row_column_difference, got_info[3]+row_column_difference, got_info[4]
            adjusted_color_indices = []
            for i in color:
                adjusted_color_indices.append(i+row_column_difference)
            color = adjusted_color_indices.copy()
            self.solver.append_formula(solution_1)
            self.solver.append_formula(solution_2)
            self.solver.append_formula(self.__intersections(solution_1, blocks, self.rows))
            row_cells_info = self.__match_column_cells(max_position, self.rows, column * self.rows, min_num, color, self.columns, blocks, max_column_position)
            self.__add_to_solution_clauses(row_cells_info)
            previous_start_column += len(blocks)

        self.solver.solve()
        self.solved_status = self.solver.get_model()

    def draw(self):
        fig, ax = plt.subplots()
        ax.plot()
        if self.solved_status != None:
            for i in range(self.rows*self.columns):
                if i % self.columns == (self.columns-1):
                    if self.solved_status[i] >= 0:
                        ax.add_patch(Rectangle((i % self.columns, self.rows-i//self.columns), 1, 1))
                else:
                    if self.solved_status[i] >= 0:
                        ax.add_patch(Rectangle((i % self.columns, self.rows-i//self.columns), 1, 1))
            plt.show()
        else:
            return 'No solution'
