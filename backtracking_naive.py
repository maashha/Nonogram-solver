import re
from random import sample
from typing import List, Tuple, Dict
import os
import time

solution_list: List[List[int]] = []


def valid(s: List[int], r: List[Tuple], c: List[Tuple]):
    s_all: List[int] = s.copy() + [-1]*(len(r)*len(c) - len(s))
    grid: Dict[int, List] = {}
    row: int = 0
    for i in range(0, len(s_all), len(c)):
        grid[row] = s_all[i:(i + len(c))]
        row += 1
    
    # Check row and column constraints
    for row in grid.keys():
        # Ensure row sum is not exceeded
        row_sum_max = sum(r[row])
        row_sum_now = sum([1 if r == 1 else 0 for r in grid[row]])
        if row_sum_now > row_sum_max:
            return False
        
        # If row sum is not exceeded, can they still be obtained from the blank cells?
        sum_from_blank = sum([1 if r == -1 else 0 for r in grid[row]])
        if row_sum_now + sum_from_blank < row_sum_max:
            return False
        
        # Are grouping requirements met?
        if sum_from_blank != 0:
            # Blank cells exist. Assume True.
            continue
        else:
            str_ = "".join([str(a) for a in grid[row]])
            groups = re.split('0+', str_)
            groups = [g for g in groups if g != '']
            group_sums = tuple([len(g) for g in groups])
            if group_sums != r[row]:
                return False
    
    for col in range(len(c)):
        col_values = []
        for row in grid.keys():
            col_values.append(grid[row][col])
        
        # Ensure column sum is not exceeded
        col_sum_max = sum(c[col])
        col_sum_now = sum([1 if c == 1 else 0 for c in col_values])
        if col_sum_now > col_sum_max:
            return False
        
        # If col sum is not exceeded, can they still be obtained from the blank cells?
        sum_from_blank = sum([1 if r == -1 else 0 for r in col_values])
        if col_sum_now + sum_from_blank < col_sum_max:
            return False

        # Are grouping requirements met?
        if sum_from_blank != 0:
            # Blank cells exist. Assume True.
            continue
        else:
            str_ = "".join([str(a) for a in col_values])
            groups = re.split('0+', str_)
            groups = [g for g in groups if g != '']
            group_sums = tuple([len(g) for g in groups])
            if group_sums != c[col]:
                return False
    
    # Both row and column checks passed
    return True


def extend(row_args: List[Tuple], col_args: List[Tuple], partial_solution: List[int]):
    global solution_list
    if len(partial_solution) == len(row_args) * len(col_args):
        solution_list.append(partial_solution.copy())
        return
    
    # Define move list based on how sparse the row/column sum is
    # move_row, move_col = len(partial_solution) % len(row_args), int(len(partial_solution)/len(row_args)) % len(col_args)
    for move in sample([0, 1], k=2):
        partial_solution.append(move)
        if not valid(partial_solution, row_args, col_args):
            # Backtrack
            partial_solution.pop()
            continue
        extend(row_args, col_args, partial_solution)
        partial_solution.pop()
    return
def load_from_file(file_name):
    line_number = 0
    rows = 0
    columns = 0
    all_rows = []  # the array of all blocks of filled cells in ROWS
    all_columns = []  # the array of all blocks of filled cells in COLUMNS
    if os.path.isfile(file_name):
        with open(file_name, "r") as file:
            for line in file:
                line_number += 1
                if line_number == 1:
                    rows = int(line.split(" ")[0])
                    columns = int(line.split(" ")[1])
                elif line_number <= 1 + rows:
                    all_rows.append(list(map(int, line.split())))
                else:
                    all_columns.append(list(map(int, line.split())))
    return [all_rows, all_columns]

def efficiency_naive():
    times = []
    tests = [70419, 70402, 70399, 70472, 70449, 70446, 70474, 70470, 70468, 70442, 70281, 70260, 70289, 70070, 69690]
    for test in tests:
        start_time = time.time()
        ro = load_from_file('tests/test'+str(test)+'.txt')[0]
        co = load_from_file('tests/test'+str(test)+'.txt')[1]
        row_args = []
        col_args = []
        for i in ro:
            row_args.append(tuple(i))
        for i in co:
            col_args.append(tuple(i))
        extend(row_args, col_args, [])
        end_time = time.time()
        times.append(end_time-start_time)
    return times