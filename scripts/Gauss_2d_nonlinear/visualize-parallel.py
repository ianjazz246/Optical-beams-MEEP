#!/bin/env python3
import multiprocessing
import subprocess
import os
import re

OUTPUT_H5_FILENAME = "Gauss2d-ez-000011088.h5"

def rreplace(s: str, old: str, new: str, occurrence: int) -> str:
    """
    Replace last occurance of old in string s with new
    """
    li = s.rsplit(old, maxsplit=occurrence)
    return new.join(li)

def visualize_gauss(mainDataFile: str):
    """
    Runs ../make-visualization.sh script to turn h5 to png.
    mainDataFile must be an absolute path
    Also renames output png to the name of the directory it's in
    """
    subprocess.run(["../make-visualization.sh", mainDataFile])
    output_png_path = rreplace(mainDataFile, ".h5", ".png", 1)
    containing_dir_name = os.path.basename(os.path.dirname(mainDataFile))
    os.rename(output_png_path, os.path.dirname(output_png_path) + "/" + containing_dir_name + ".png")

def get_dirs_to_visualize() -> filter:
    """
    Get iterator containg directory names that match pattern "amp=* logk=*"
    Only directories in current directory, names relative to current directory
    """
    regex_pattern = "^amp=[0-9\.]+ logk=[+-]?[0-9\.]+ detailed$"
    regex = re.compile(regex_pattern)
    dirs = os.listdir(".")
    matching_dirs = filter(lambda dir: regex.search(dir), dirs)
    return matching_dirs

if __name__ == "__main__":
    print("Note. Run this file in directory containing Gauss2d.py and output directories")
    files_to_visualize = map(lambda dir: os.path.abspath(dir + "/" + OUTPUT_H5_FILENAME), get_dirs_to_visualize())
    with multiprocessing.Pool() as pool:
        pool.map(visualize_gauss, files_to_visualize)