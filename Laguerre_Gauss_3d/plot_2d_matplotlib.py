"""
file:   plot_2d_matplotlib.py
brief:  Python script to visualise transverse intensity profiles of vortex beams. 
        The program extracts 2d slices (for any given section) of an HDF5 file generated by the FDTD solver Meep.
author: Daniel Kotik
date:   18.01.2018

invocation: python plot_2d_matplotlib.py LaguerreGauss3d-out/e2_s-000010.00.h5
"""

import matplotlib.pyplot as plt
import numpy as np
import h5py
import sys

filename = sys.argv[1]
#filename = "LaguerreGauss3d-out/e2_s-000010.00.h5"

cutoff = 30   # cut-off borders of data (removing PML layer and line source placment is desired)

with h5py.File(filename, 'r') as hf:
    print("Keys: %s" % hf.keys())
    #data = hf['e2_s'][:]
    data = hf[hf.keys()[0]][:] # first data set

print(np.shape(data))
center_index = np.int(data.shape[2]/2)

data_optimised = np.transpose(data[cutoff:-cutoff, cutoff:-cutoff, center_index])

plt.imshow(data_optimised, origin='lower', cmap=plt.cm.hot, interpolation='None')
plt.show()


# List all groups
#print("Keys: %s" % hf.keys())


# Get the data (first variant)
#a_group_key = list(hf.keys())[0]
#data = list(f[a_group_key])

# Get the data (second variant)
#n1 = hf.get('dataset_1')
#n1 = np.array(n1)
#n1.shape
