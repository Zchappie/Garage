import time
import glob
from fabric import * 
from subprocess import Popen, PIPE
import os
from threading import Timer
import numpy as np


faster = 0
slower = 0
tests = 0
mistakes = 0

UNSAT_times = []
SAT_times = []
TIMEOUT = 60*10 #seconds
TIMEOUT_times = []

def run(cmd, timeout_sec):
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    timer = Timer(timeout_sec, proc.kill)
    try:
        timer.start()
        stdout, stderr = proc.communicate()
        return stdout.decode()
    finally:
        timer.cancel()

with open("benchmarks/benchmark_details.txt", "w+") as bm:
    for file in list(reversed(sorted(glob.glob('./Examples/*.txt'), key=os.path.basename)))[:]:
        filename = file.replace("./Examples/", "")

        f = Fabric()
        w, h, shapes, connections, b = f.parse_input(file)
        cnf_name = "cnfs/"+filename+".cnf"
        X, cnf = f.fabric(w, h, shapes, connections, output=False, into_file=cnf_name)

        s = time.time()
        solution = run(['picosat', cnf_name], TIMEOUT)
        dur = time.time()-s

        theirs = file.replace("./Examples/", "")
        theirs = theirs.replace("_UNSAT.txt", "")
        theirs = theirs.replace("_SAT.txt", "")
        theirs = float(theirs)
        

        their_solution = "UNSAT" if "UNSAT" in file else "SAT"


        if dur <= theirs:
            speed = "faster" 
            faster += 1
        else:
            speed = "slower" 
            slower += 1
        
        if solution == "":
            print("{:40} {:10} {:10} {:10}".format(file, speed, "TIMEOUT", dur))
            bm.write("{:40} {:10} {:10} {:10}\n".format(file, speed, "TIMEOUT", dur))
            TIMEOUT_times.append(dur)

        elif "UNSATISFIABLE" in solution  and  their_solution == "UNSAT":
            print("{:40} {:10} {:10} {:10}".format(file, speed, "UNSAT", dur))
            bm.write("{:40} {:10} {:10} {:10}\n".format(file, speed, "UNSAT", dur))
            UNSAT_times.append(dur)
        elif "UNSATISFIABLE" not in solution and "SATISFIABLE" in solution and their_solution == "SAT":
            speed = "faster" if dur < theirs else "slower"
            print("{:40} {:10} {:10} {:10}".format(file, speed, "SAT", dur))
            bm.write("{:40} {:10} {:10} {:10}\n".format(file, speed, "SAT", dur))
            SAT_times.append(dur)
        else:
            print(solution)
            print("{:40} {:10}".format(file, "MISTAKE?"))
            bm.write("{:40} {:10}\n".format(file, "MISTAKE?"))
            mistakes += 1

        tests +=1

with open("benchmarks/benchmark.txt", "w+") as file:
    file.write("Tests:          {}\n".format(tests))
    file.write("Faster:         {}\n".format(faster))
    file.write("Slower:         {}\n".format(slower))
    file.write("Mistakes:       {}\n".format(mistakes))
    file.write("Timeouts:       {} with {}s timeout\n".format(len(TIMEOUT_times), TIMEOUT))
    if UNSAT_times: 
        file.write("Average UNSAT:  {:.3f} of {} \n".format(sum(UNSAT_times)/len(UNSAT_times), len(UNSAT_times)))
        file.write("Median UNSAT:   {:.3f} of {} \n".format(np.median(UNSAT_times), len(UNSAT_times)))
    if SAT_times: 
        file.write("Average SAT:    {:.3f} of {} \n".format(sum(SAT_times)/len(SAT_times), len(SAT_times)))
        file.write("Median SAT:     {:.3f} of {} \n".format(np.median(SAT_times), len(SAT_times)))

