def create_output(assignments, sudoku_name):
    filename = '{}_out.txt'.format(sudoku_name)
    with open(filename, 'w') as f:
        for assignment in assignments:
            f.write('{} 0\n'.format(assignment))
