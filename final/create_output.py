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
