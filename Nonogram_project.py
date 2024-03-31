import pycosat
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class NonogramSolver:
    def __init__(self, rows, columns, row_blocks, column_blocks, solved_status, solution_clauses):
        self.rows = rows
        self.columns = columns
        self.row_blocks = row_blocks
        self.column_blocks = column_blocks
        self.solved_status = solved_status
        self.solution_clauses = solution_clauses

    def load_from_file(self, file_name):
        line_number = 0
        self.rows = 0
        self.columns = 0
        self.row_blocks = []  # the array of all blocks of filled cells in ROWS
        self.column_blocks = []  # the array of all blocks of filled cells in COLUMNS
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
    def calculate_positions(block_sizes, length, base_position, series_number):
        all_positions, non_empty_positions, uniqueness_clauses = [], [], []
        max_position = 0
        min_position = -1
        left_boundary = 0
        right_boundary = 0
        for group_size in range(len(block_sizes)):
            starting_positions = []
            if group_size == 0:
                left_boundary = 0
                right_boundary = length + 1 - sum(block_sizes[0:]) - len(block_sizes)
            else:
                # Move boundaries by the length of the previous block
                left_boundary += block_sizes[group_size - 1] + 1
                right_boundary += block_sizes[group_size - 1] + 1
            for possible_start in range(left_boundary, right_boundary + 1):
                position = (possible_start + 1) + length * (series_number + group_size) + base_position
                # Add all possible positions of the first cell of the block to one array
                starting_positions.append(position)
                non_empty_positions.append(position)
                if max_position < position:
                    max_position = position
                if min_position > position or min_position == -1:
                    min_position = position
                for next_possible in range(possible_start + 1, right_boundary + 1):
                    # Exclude situations where one block has two starting cells
                    uniqueness_clauses.append([-position, -((next_possible + 1) + length * (series_number + group_size))])
            all_positions.append(starting_positions)  # all of such starting_positions for one row or column
        return [all_positions, uniqueness_clauses, max_position, min_position, non_empty_positions]

    @staticmethod
    def calculate_intersections(position_sets, block_lengths, total_length):
        intersecting_clauses = []
        for section_1 in range(len(position_sets)):
            for section_2 in range(section_1 + 1, len(position_sets)):  # choose two sets of starting positions of the blocks
                for first_position in range(len(position_sets[section_1])):
                    # add elements of the first array in pairs with elements of the second, excluding their intersection
                    for second_position in range(len(position_sets[section_2])):
                        if abs((position_sets[section_1][first_position]) - (position_sets[section_2][second_position])) % total_length < sum(
                                block_lengths[section_1:section_2]) + (section_2 - section_1) and abs(
                                (position_sets[section_1][first_position]) - (position_sets[section_2][second_position])) >= total_length:
                            intersecting_clauses.append([-(position_sets[section_1][first_position]), -(position_sets[section_2][second_position])])
                            if first_position >= 3:
                                intersecting_clauses.append([-(position_sets[section_1][first_position]), -(position_sets[section_2][first_position - 3])])
        return intersecting_clauses

    @staticmethod
    def calculate_row_cells(max_position, length, start, min_position, occupied_positions, row_blocks, total_length):
        all_cells, unoccupied_positions, empty_cells, single_cells, row_mapping = [], [], [], [], {}
        for i in range(start + 1, start + length + 1):
            cells_in_row = [-i]
            if i % length != 0:
                for j in range(min_position + i % length - 1, max_position + 1, length):
                    if j not in unoccupied_positions and j not in occupied_positions:
                        unoccupied_positions.append([-j])
                    else:
                        cells_in_row.append(j)
                        for n in range(i, i + row_blocks[(j - total_length) // length]):
                            single_cells.append([-j, n])
                            if n in row_mapping.keys():
                                row_mapping[n].append(j)
                            else:
                                row_mapping[n] = [-n, j]
                        empty_cells.append([i, -j])
            else:
                for j in range(min_position + length - 1, max_position + 1, length):
                    if j not in unoccupied_positions and j not in occupied_positions:
                        unoccupied_positions.append([-j])
                    else:
                        cells_in_row.append(j)
                        for n in range(i, i + row_blocks[(j - total_length) // length - 1]):
                            single_cells.append([-j, n])
                            if n in row_mapping.keys():
                                row_mapping[n].append(j)
                            else:
                                row_mapping[n] = [-n, j]
                        empty_cells.append([i, -j])
            all_cells.append(cells_in_row)
            all_cells = []
        return [single_cells, empty_cells, unoccupied_positions, row_mapping]

    @staticmethod
    def calculate_column_cells(max_position, length, start, min_position, occupied_positions, total_columns, row_length, column_blocks, total_length):
        all_cells, unoccupied_positions, empty_cells, single_cells, column_mapping = [], [], [], [], {}
        for i in range(start + 1, start + length + 1):
            column_mapping[((i - 1) % length) * total_columns + (i - 1) // length + 1] = [-(((i - 1) % length) * total_columns + (i - 1) // length + 1)]
        for i in range(start + 1, start + length + 1):
            cells_in_column = [-(((i - 1) % length) * total_columns + (i - 1) // length + 1)]
            if i % length != 0:
                until_boundary = 0
                remainder = i % length
            else:
                until_boundary = -1
                remainder = length
            for j in range(min_position + remainder - 1, max_position + 1, length):
                if j not in unoccupied_positions and j not in occupied_positions:
                    unoccupied_positions.append([-j])
                else:
                    cells_in_column.append(j)
                    for n in range(i, i + column_blocks[(j - total_length) // length + until_boundary]):
                        single_cells.append([-j, ((n - 1) % length) * total_columns + (n - 1) // length + 1])
                        column_mapping[((n - 1) % length) * total_columns + (n - 1) // length + 1].append(j)
                    empty_cells.append([((i - 1) % length) * total_columns + (i - 1) // length + 1, -j])
            all_cells.append(cells_in_column)
        return [single_cells, empty_cells, unoccupied_positions, column_mapping]

    def add_cells_to_solutions(self, cells_info):
        colored_cells, empty_cells, unoccupied_cells, mapping = cells_info
        for cell in empty_cells:
            self.solution_clauses.append(cell)
        for cell in colored_cells:
            self.solution_clauses.append(cell)
        for cell in unoccupied_cells:
            self.solution_clauses.append(cell)
        for cell in mapping:
            self.solution_clauses.append(mapping[cell])

    def solve(self):
        previous = 0
        max_position = self.rows * self.columns
        for i in range(self.rows):
            blocks = self.row_blocks[i]  # all filled in cells in the ith row
            if max_position % self.columns == 0:
                max_position_adjusted = max_position
            else:
                max_position_adjusted = max_position + (self.columns - max_position % self.columns)
            if blocks == [0]:  # case of the empty row
                for empty_position in range(i * self.columns + 1, (i + 1) * self.columns + 1):
                    self.solution_clauses.append([-empty_position])
                continue
            all_positions_info = self.calculate_positions(blocks, self.columns, self.rows * self.columns, previous)
            positions, unique_positions, max_position, min_position = all_positions_info[0], all_positions_info[1], all_positions_info[2], all_positions_info[3]
            color_positions = all_positions_info[4]
            for position in positions:
                self.solution_clauses.append(position)
            for unique_position in unique_positions:
                self.solution_clauses.append(unique_position)
            for clause in self.calculate_intersections(positions, blocks, self.columns):
                self.solution_clauses.append(clause)
            cells_info = self.calculate_row_cells(max_position, self.columns, i * self.columns, min_position, color_positions, blocks, max_position_adjusted)
            self.add_cells_to_solutions(cells_info)
            previous += len(blocks)
        previous = 0
        for column in range(self.columns):
            blocks = self.column_blocks[column]
            position_info = self.calculate_positions(blocks, self.rows, self.rows * self.columns, previous)
            if column == 0:
                if max_position % self.columns == 0:
                    max_position_adjusted = max_position
                else:
                    max_position_adjusted = max_position + (self.columns - max_position % self.columns)
                adjust = max_position_adjusted - self.columns * self.rows
            if (max_position - adjust) % self.rows == 0:
                max_position_adjusted = max_position
            else:
                max_position_adjusted = max_position + (self.rows - (max_position - adjust) % self.rows)
            if blocks == [0]:
                for h in range(column * self.rows + 1, column * self.rows + self.rows + 1):
                    self.solution_clauses.append([-(((h - 1) % self.rows) * self.columns + (h - 1) // self.rows + 1)])
                continue
            row_solutions, row_solutions_negated = [], []
            row_positions_1, row_positions_2 = position_info[0], position_info[1]
            for position_set_1 in row_positions_1:
                row_positions_1_1 = []
                for position_1 in position_set_1:
                    row_positions_1_1.append(position_1 + adjust)
                row_solutions.append(row_positions_1_1)
            for position_set_2 in row_positions_2:
                row_positions_2_1 = []
                for position_2 in position_set_2:
                    row_positions_2_1.append(-(position_2 * (-1) + adjust))
                row_solutions_negated.append(row_positions_2_1)
            row_positions_1, row_positions_2 = row_solutions.copy(), row_solutions_negated.copy()
            max_position_adjusted, min_position_adjusted, color_positions = position_info[2] + adjust, position_info[3] + adjust, position_info[4]
            color_positions_adjusted = []
            for color_position in color_positions:
                color_positions_adjusted.append(color_position + adjust)
            color_positions = color_positions_adjusted.copy()
            for position_set_1 in row_positions_1:
                self.solution_clauses.append(position_set_1)
            for position_set_2 in row_positions_2:
                self.solution_clauses.append(position_set_2)
            for clause in self.calculate_intersections(row_positions_1, blocks, self.rows):
                self.solution_clauses.append(clause)
            cells_info = self.calculate_column_cells(max_position_adjusted, self.rows, column * self.rows, min_position_adjusted, color_positions, self.columns, self.rows, blocks, max_position_adjusted)
            self.add_cells_to_solutions(cells_info)
            previous += len(blocks)
        self.solved_status = pycosat.solve(self.solution_clauses)

    def draw(self):
        fig, ax = plt.subplots()
        ax.plot()
        if self.solved_status != 'UNSAT':
            for i in range(self.rows * self.columns):
                if i % self.columns == (self.columns - 1):
                    if self.solved_status[i] >= 0:
                        ax.add_patch(Rectangle((i % self.columns, self.rows - i // self.columns), 1, 1))
                else:
                    if self.solved_status[i] >= 0:
                        ax.add_patch(Rectangle((i % self.columns, self.rows - i // self.columns), 1, 1))
        plt.show()
