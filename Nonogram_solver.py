from Nonogram_project import NonogramSolver
import time


def efficiency_counter(test):
    solver = NonogramSolver()
    start_time = time.time()
    solver.load_from_file('tests/test' + str(test) + '.txt')
    solver.solve()
    solver.draw()
    end_time = time.time()
    return [end_time - start_time, str(solver.rows)+'*'+str(solver.columns)]