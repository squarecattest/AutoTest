from slowmain import main, rotations, TextIO
from string import ascii_uppercase as Alphas
from random import randint, random, choice

def trigger(p: float):
    return random() < p

## change here ##
code = "3"
numberfrom = 1
samples = 10
string_length = 100
max_pattern_length = 100
max_length_is_length = True
p1 = 1 ## p for generate a pattern / rotation
p2 = 1 ## p for choosing some rotations when generating, otherwise the original pattern
p3 = 0 ## p for continuing pattern to rotation
#################

for i in range(samples):
    pattern_length = max_pattern_length if max_length_is_length else randint(1, max_pattern_length)
    pattern = "".join(choice(Alphas) for i in range(pattern_length))
    patterns = rotations(pattern)

    string = ""
    s = 0
    j = None
    while s < string_length:
        if not j is None:
            if trigger(p3):
                string += pattern[j % pattern_length]
                s += 1
                j += 1
                continue
        if trigger(p1):
            if trigger(p2):
                j = choice(range(pattern_length))
                string += patterns[j]
                s += pattern_length
            else:
                string += pattern
                s += pattern_length
                j = 0
        else:
            string += choice(Alphas)
            s += 1
            j = None
    string = string[:string_length]
        

    fileinname = f".\\testcase\\sin\\{code}-{i + numberfrom:02d}.txt"
    fileoutname = f".\\testcase\\sout\\{code}-{i + numberfrom:02d}.txt"
    with open(fileinname, "w") as filein:
        filein.write(f"{string_length} {pattern_length}\n")
        filein.write(f"{string}\n")
        filein.write(f"{pattern}\n")
    with open(fileinname, "r") as filein:
        with open(fileoutname, "w") as fileout:
            main(filein, fileout)
