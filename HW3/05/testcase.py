from slowmain import slowmain
from random import randint, choice

def writefile(fileinname, N, M, H, A, attacks):
    with open(fileinname, "w") as filein:
        filein.write(f"{N} {M}\n")
        for h in H[:-1]:
            filein.write(f"{h} ")
        filein.write(f"{H[-1]}\n")
        for a in A[:-1]:
            filein.write(f"{a} ")
        filein.write(f"{A[-1]}\n")
        for Ka, Ks in attacks:
            filein.write(f"{Ka} {Ks}\n")

def testfile(fileinname, fileoutname):
    with open(fileinname, "r") as filein:
        with open(fileoutname, "w") as fileout:
            slowmain(filein=filein, fileout=fileout)

"--------------------- change here ---------------------"
## {classno}-{startno} ~ {classno}-{endno}
## endno - startno + 1 = number of testcases
classno = 1
startno = 1
endno = 10

## number of knights
n = 10
## number of attacks
m = 10
## max health point
h_max = 40
## max attack point
a_max = 40
"-------------------------------------------------------"

if __name__ == "__main__":
    for fileno in range(startno, endno + 1):
        healths = []
        ATKs = []
        attacks = []
        Nrange = range(1, n + 1)
        Nrangeminus1 = range(1, n)
        for i in range(n):
            healths.append(randint(1, h_max))
        for i in range(n):
            ATKs.append(randint(1, a_max))
        for i in range(m):
            j = choice(Nrange)
            k = choice(Nrangeminus1)
            if k >= j: k += 1
            attacks.append((j, k))

        fileinname = f".\\sin\\{classno}-{fileno:02d}.txt"
        fileoutname = f".\\sout\\{classno}-{fileno:02d}.txt"
        writefile(fileinname, n, m, healths, ATKs, attacks)
        testfile(fileinname, fileoutname)