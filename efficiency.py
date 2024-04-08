from Nonogram_solver import efficiency_counter
from backtracking_naive import efficiency_naive
from enumerative_backtracking_solver import efficiency_enumerative
import pandas as pd

existing_file = 'Efficiency_comparison.xlsx'
tests = [70419, 70402, 70399, 70472, 70449, 70446, 70474, 70470, 70468, 70442, 70281, 70260, 70289, 70070, 69690]
final_tests = []
for test in tests:
    final_tests.append('test'+str(test)+'.txt')
new_data = {'Tests': final_tests,
            'My project': efficiency_counter(),
            'enumerative_backtracking_solver.py': efficiency_enumerative()}
df_new = pd.DataFrame(new_data)
df_existing = pd.read_excel(existing_file)
df_combined = pd.concat([df_new], ignore_index=True)
df_combined.to_excel(existing_file, index=False)