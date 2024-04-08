from Nonogram_project import NonogramSolver
import time


def efficiency_counter():
    tests = [70419, 70402, 70399, 70472, 70449, 70446, 70474, 70470, 70468, 70442, 70281, 70260, 70289, 70070, 69690]
    times = []
    for test in tests:
        solver = NonogramSolver(0, 0, [], [], [], [])
        start_time = time.time()
        solver.load_from_file('tests/test' + str(test) + '.txt')
        solver.solve()
        solver.draw()
        end_time = time.time()
        times.append(end_time - start_time)
    return times