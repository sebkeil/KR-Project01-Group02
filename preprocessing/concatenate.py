import glob

# read in all txt files
files = glob.glob('*.txt')

# find the index of the sudoku rules
rules_index = files.index('sudoku-rules.txt')

# create new sudoku_test (rules + puzzle) for each puzzle
for index_file, this_file in enumerate(files):
    with open("sudoku_test{}.txt".format(index_file+1), "wb") as outfile:
        with open(files[rules_index], "rb") as rules:
            outfile.write(rules.read())
        with open(this_file, "rb") as infile: 
            outfile.write(infile.read())

