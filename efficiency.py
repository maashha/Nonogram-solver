from Nonogram_solver import efficiency_counter
from programs_to_compare.enumerative_backtracking_solver import efficiency_enumerative
from programs_to_compare.New_solver import efficiency_nonogram
import pandas as pd


existing_file = 'Efficiency_comparison.xlsx'
tests = ['small_tests/small_test_1', 'small_tests/small_test_2', 'small_tests/small_test_3',
         'medium_tests/medium_test_1', 'medium_tests/medium_test_2', 'medium_tests/medium_test_3',
         'large_tests/large_test_1', 'large_tests/large_test_2', 'large_tests/large_test_3',
         'x-large_tests/x-large_test_1', 'x-large_tests/x-large_test_2', 'x-large_tests/x-large_test_3'
         'xx-large_tests/xx-large_test_1', 'xx-large_tests/xx-large_test_2', 'xx-large_tests/xx-large_test_3',
         'unsat_tests/unsat_test_1', 'unsat_tests/unsat_test_2', 'unsat_tests/unsat_test_3']
final_tests = []
times_1, sizes_1, times_2, times_3 = [], [], [], []
for test in tests:
    final_tests.append(test.split('/')[1]+'.txt')
    efficiency_1 = efficiency_counter(test)
    times_1.append(efficiency_1[0])
    sizes_1.append(efficiency_1[1])
    efficiency_2 = efficiency_enumerative(test)
    times_2.append(efficiency_2)
    efficiency_3 = efficiency_nonogram(test)
    times_3.append(efficiency_3)
new_data = {'Test': final_tests,
            'Size': sizes_1,
            'My project': times_1,
            'enumerative_backtracking_solver.py': times_2,
            'New_solver.py': times_3}
df_new = pd.DataFrame(new_data)
df_existing = pd.read_excel(existing_file)
df_combined = pd.concat([df_new], ignore_index=True)
df_combined.to_excel(existing_file, index=False)