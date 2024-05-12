import pandas as pd
import matplotlib.pyplot as plt

file = 'Efficiency_comparison.xlsx'

xl = pd.ExcelFile(file)

df1 = xl.parse('Sheet1')

df1.plot(x="Size", y="My program", kind="line")

plt.show()
for i in range(len(df1['enumerative_backtracking_solver.py'])):
    if df1['enumerative_backtracking_solver.py'][i] == '*':
         df1['enumerative_backtracking_solver.py'][i] = float(600)
df1['enumerative_backtracking_solver.py']=df1['enumerative_backtracking_solver.py'].astype(float)

df1.plot(x="Size", y="enumerative_backtracking_solver.py", kind="line")

plt.show()
for i in range(len(df1['New_solver.py'])):
    if df1['New_solver.py'][i] == '*':
         df1['New_solver.py'][i] = float(600)
df1['New_solver.py']=df1['New_solver.py'].astype(float)

df1.plot(x="Size", y="New_solver.py", kind="line")

plt.show()

df1.plot(kind="line")
plt.show()