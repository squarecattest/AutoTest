from subprocess import run, TimeoutExpired
from os.path import isdir, isfile, join
from os import listdir, makedirs, remove
from argparse import ArgumentParser
from time import time
from random import randint

linesep = "-" * 40

class AutoFormatIO:
    def __init__(self, file):
        self.__file = file

    def __align(self, __s):
        if __s == linesep:
            return f"[-{__s:40s}-]\n"
        return f"[ {__s:40s} ]\n"

    def write(self, __s):
        self.__file.write(self.__align(__s))

class Timer:
    @classmethod
    def start(cls):
        cls.time = time()

    @classmethod
    def read(cls):
        return int((time() - cls.time) * 1000)
    
    @classmethod
    def settimeout(cls, timeout):
        cls.timeout = timeout
        cls.insecond = timeout / 1000

    @staticmethod
    def string_format(runtime):
        if runtime < 1000:
            return f"{runtime}ms"
        return f"{runtime // 1000}.{runtime % 1000:03d}s"
    
class Checker:
    class EOL:
        pass
    def __init__(self, sout, out, runtime):
        self.runtime = runtime
        sout.seek(0)
        out.seek(0)
        lineno = 1
        while True:
            sline = sout.readline()
            line = out.readline()
            if not sline and not line:
                self.AC = True
                return
            if not sline and line:
                while True:
                    if line := line.strip(""):
                        self.AC = False
                        self.lineno = lineno
                        self.expected = Checker.EOL()
                        self.found = line.strip()
                        return
                    lineno += 1
                    line = out.readline()
                    if not line:
                        self.AC = True
                        return
            if sline and not line:
                self.AC = False
                self.lineno = lineno
                self.expected = sline.strip("")
                self.found = Checker.EOL()
                return
            sline = sline.strip()
            line = line.strip()
            if sline != line:
                self.AC = False
                self.lineno = lineno
                self.expected = sline
                self.found = line
                return
            lineno += 1

    def EOL_check(self, string):
        if isinstance(string, Checker.EOL):
            return "EOL"
        return f"'{string}'"

    def string_format(self):
        if self.AC:
            return ("AC", ("Result: AC", f"Runtime: {Timer.string_format(self.runtime)}"))
        return ("WA", ("Result: WA", f"Runtime: {Timer.string_format(self.runtime)}",
                f" - <At line {self.lineno}>", 
                f" - Expected: {self.EOL_check(self.expected)}",
                f" - Found: {self.EOL_check(self.found)}"))

def Execute(exe: str, sinfile, soutfile, output, output_i, counter):
    with open(output_i, "w+") as outputfile:
        output.write(linesep)
        output.write(f"Testcase #{counter}: {sinfile.name}")
        if soutfile is None:
            output.write("<sample output not found>")
        output.write("")
        TLE = False
        Timer.start()
        try:
            exitcode = run([exe], stdin=sinfile, stdout=outputfile, timeout=Timer.insecond).returncode
            runtime = Timer.read()
            TLE = False
        except TimeoutExpired:
            exitcode = 1
            runtime = Timer.timeout
            TLE = True
        
        result, log = LogProcess(exitcode, runtime, TLE, soutfile, outputfile)
        for line in log:
            output.write(line)
        return result

def LogProcess(exitcode: int, runtime: int, IsTLE: bool, sout, out):
    if IsTLE:
        return ("TLE", ("Result: TLE", f"Runtime: >{Timer.string_format(runtime)}"))
    if exitcode != 0:
        return ("RE", ("Result: RE", f"Runtime: {Timer.string_format(runtime)}"))
    if sout is None:
        return ("AC/WA", ("Result: <AC or WA>", f"Runtime: {Timer.string_format(runtime)}"))
    return Checker.string_format(Checker(sout, out, runtime))


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-f", dest="file", default=".\\a.exe",
                        help="Executable file location")
    parser.add_argument("-sin", default=".\\sin",
                        help="Sample input directory location")
    parser.add_argument("-sout", default=".\\sout",
                        help="Sample output directory location")
    parser.add_argument("-l", dest="log", default=".\\log.txt",
                        help="Main output log location")
    parser.add_argument("-o", dest="outs", default=".\\outputs",
                        help="Individual output directory location")
    parser.add_argument("-t", dest="timeout", type=int, default="2000",
                        help="Set the timeout in unit ms")
    args = parser.parse_args()

    if not isfile(args.file):
        raise FileNotFoundError(f"Invalid executable file: \"{args.file}\"")
    if not isdir(args.sin):
        raise FileNotFoundError(f"Invalid sample input directory: \"{args.sin}\"")
    if not isdir(args.sout):
        print("<Warning: Sample output directory not found>")
        souts = []
    else:
        souts = listdir(args.sout)
    if not isdir(args.outs):
        makedirs(args.outs)

    exe_file = args.file
    tmpoutputfile = f".\\tmp{randint(100000000, 999999999)}"
    results: dict[str, list[str]] = {"AC": [], "WA": [], "AC/WA": [], "TLE": [], "RE": []}
    Timer.settimeout(args.timeout)
    try:
        with open(tmpoutputfile, "w") as tmpoutput:
            tmpoutputAF = AutoFormatIO(tmpoutput)
            sins = listdir(args.sin)
            if not len(sins):
                raise FileNotFoundError("No sample input found")
            counter = 1

            for sin in sins:
                filename_sin = join(args.sin, sin)
                filename_sout = join(args.sout, sin)
                filename_out = join(args.outs, sin)
                print(f"Testing '{filename_sin}'")
                with open(filename_sin) as sinfile:
                    if sin in souts:
                        with open(filename_sout) as soutfile:
                            results.get(
                                Execute(
                                    exe_file, sinfile, soutfile, tmpoutputAF, filename_out, counter
                                )
                            ).append(sin)
                    else:
                        results.get(
                            Execute(exe_file, sinfile, None, tmpoutputAF, filename_out, counter)
                        ).append(sin)
                counter += 1

            tmpoutputAF.write(linesep)
        counter -= 1
        with open(tmpoutputfile, "r") as tmpoutput:
            with open(args.log, "w") as output:
                output.write("Results:\n")
                for key, value in results.items():
                    output.write(f">>\t{key}: {len(value)}/{counter}\n")
                    if key == "AC":
                        continue
                    for filename in value:
                        output.write(f">>\t\t{filename}\n")
                while text := tmpoutput.readline():
                    output.write(text)
        remove(tmpoutputfile)
        print("Tests end.")
    except:
        remove(tmpoutputfile)
        raise