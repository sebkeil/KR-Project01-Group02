import os

def create_output(assignments, sudoku_name, difficulty_level):  # pass difficulty_level as string
    current_path = os.getcwd()
    directory = "sudoku_" + difficulty_level
    os.makedirs(directory)
    path = os.path.join(current_path, directory) 
    os.chdir(path)
    filename = '{}_out.txt'.format(sudoku_name)
    with open(filename, 'w') as f:
        for assignment in assignments:
            f.write('{} 0\n'.format(assignment))

            
def collect_test_results(assignments, sudoku_name, difficulty_level, initial_assignments, backtrack_counter, units, now_time):
    filename = 'test_results_file.txt'
    with open(filename, 'w') as f:
        f.write('-----------------------------------------------------------')
        f.write('Difficulty: '.format(difficulty_level))
        f.write('{}\n'.format(sudoku_name))
        f.write('Number of initial assignments: {}'.format(len(initial_assignments)))
        f.write('Number of assignments: {}'.format(len(assignments)))
        f.write('Number of backtracks: {}'.format(len(backtrack_counter)))
        f.write('Number of unit literals: {}'.format(len(units)))
        f.write("--- %s seconds ---\n" % now_time)
