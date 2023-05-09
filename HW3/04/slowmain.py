from typing import TextIO
from sys import stdin, stdout

Alphas = "ABCDEFGHIJKLMNOP"

def rotations(pattern: str):
    return tuple(pattern[i:] + pattern[:i] for i in range(len(pattern)))

def isrotation(string: str, patterns: tuple[str], m: int, s: int):
    return string[s:s + m] in patterns

def main(filein: TextIO = stdin, fileout: TextIO = stdout):
    if filein == stdin:
        n, m = map(int, input().strip().split())
        string = input()
        pattern = input()
    else:
        n, m = map(int, filein.readline().strip().split())
        string = filein.readline().strip()
        pattern = filein.readline().strip()
    patterns = rotations(pattern)
    print(sum(isrotation(string, patterns, m, i) for i in range(n - m + 1)), file=fileout)

if __name__ == "__main__":
    main()