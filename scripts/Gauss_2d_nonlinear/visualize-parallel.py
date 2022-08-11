#!/bin/env python3
import multiprocessing
import subprocess
import os
import re

OUTPUT_H5_FILENAME = "/Gauss2d-ez-000003696.h5"

"""
Replace last occurance of old in string s with new
"""
def rreplace(s: str, old: str, new: str, occurrence: int) -> str:
    li = s.rsplit(old, occurrence)
    return new.join(li)

"""
Runs ../make-visualization.sh script to turn h5 to png.
Also renames output png to the name of the directory it's in
"""
def visualize_gauss(mainDataFile: str):
    subprocess.run(["../make-visualization.sh", mainDataFile])
    # chdir so we don't need to use absolute path when renaming output image
    os.chdir(os.path.dirname(os.path.abspath(mainDataFile)))
    containing_dir_name = os.path.basename(os.path.dirname(os.path.abspath(mainDataFile)))
    os.rename(rreplace(os.path.abspath(mainDataFile), ".h5", ".png", 1),
              containing_dir_name + ".png")

"""
Get iterator containg directory names that match pattern "amp=* logk=*"
Only directories in current directory, names relative to current directory
"""
def get_dirs_to_visualize() -> filter:
    regex_pattern = "^amp=[0-9\.]+ logk=[+-]?[0-9\.]+$"
    regex = re.compile(regex_pattern)
    dirs = os.listdir(".")
    matching_dirs = filter(lambda dir: regex.search(dir), dirs)
    return matching_dirs

if __name__ == "__main__":
    print("Note. Run this file in directory containing Gauss2d.py and output directories")
    dirs_to_visualize = map(lambda dir: dir + OUTPUT_H5_FILENAME, get_dirs_to_visualize())
    with multiprocessing.Pool() as pool:
        pool.map(visualize_gauss, dirs_to_visualize)