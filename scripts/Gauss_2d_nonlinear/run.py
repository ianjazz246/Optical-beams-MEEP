#!/bin/env python3

import multiprocessing
import subprocess

AMP_AND_LOGK_PAIRS=[(1.0, -2), (5.0, -2), (10.0, -2), (1.0, -3), (1.0, -1)]
# Max number of simulation processes to run at a time. Default (value of None) is the number of available cpus. See https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool
PROCESS_COUNT = None

# Path to simulation Python file
SIM_SCRIPT = "Gauss2d.py"
SIM_N1 = 1.0
SIM_N2 = 1.54

def run_sim(amp: float, logk: float):
    """
    Run simulation with specified amp and logk values.
    Output directory set to "amp={amp} logk={logk}".
    Writes stdout to file
    """
    out_dir = f"amp={amp} logk={logk} test"
    # Write to log file so each MEEP process's output can be clearly read
    with open(out_dir + ".log", "w") as out_file:
        subprocess.run(["python3", SIM_SCRIPT,
                        "-n1", str(SIM_N1), "-n2", str(SIM_N2),
                        "-amp", str(amp), "-logk", str(logk), "-outdir", out_dir],
                        stdout=out_file)
    print(f"MEEP process \"{out_dir}\" completed successfully")

if __name__ == "__main__":
    with multiprocessing.Pool(processes=PROCESS_COUNT) as pool:    
        pool.starmap(run_sim, AMP_AND_LOGK_PAIRS)
    