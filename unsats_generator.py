from Nonogram_solver import efficiency_counter
import pandas as pd
import matplotlib.pyplot as plt

for i in range(4, 12):
    f = open("tests/unsat_tests/unsat_test_"+str(i)+".txt", "w")
    f.write(str(i)+' '+str(i+1)+'\n')
    for j in range(i*2+1):
        f.write('1\n')
    f.close()


existing_file = 'Unsats_efficiency_comparison.xlsx'
tests = ['unsat_tests/unsat_test_4', 'unsat_tests/unsat_test_5', 'unsat_tests/unsat_test_6',
         'unsat_tests/unsat_test_7', 'unsat_tests/unsat_test_8', 'unsat_tests/unsat_test_9',
         'unsat_tests/unsat_test_10', 'unsat_tests/unsat_test_11']
final_tests = []
times, sizes= [], []
for test in tests:
    final_tests.append(test.split('/')[1]+'.txt')
    efficiency_1 = efficiency_counter(test)
    times.append(efficiency_1[0])
    sizes.append(efficiency_1[1])

new_data = {'Test': final_tests,
            'Size': sizes,
            'My program': times}
df_new = pd.DataFrame(new_data)
df_existing = pd.read_excel(existing_file)
df_combined = pd.concat([df_new], ignore_index=True)
df_combined.to_excel(existing_file, index=False)

file = 'Unsats_efficiency_comparison.xlsx'

xl = pd.ExcelFile(file)

df1 = xl.parse('Sheet1')

df1.plot(x="Size", y="My program", kind="line")

plt.show()