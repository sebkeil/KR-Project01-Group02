import glob

files = glob.glob('*.txt')
print(files)

# make sure first the sudoku rules are read in, then the given sudoku
if files[1] == 'sudoku-rules.txt':
    order = [1, 0]
    files = [files[i] for i in order]
print(files)

# create new file including both the the sudoku rules and the given sudoku
with open("sudoku_inputfile.txt", "wb") as outfile:
    for f in files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())

