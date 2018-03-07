"""
file:   plot_2d_matplotlib.py
brief:  Python script to visualise transverse intensity profiles of vortex beams. 
        The program extracts 2d slices (for any given section) of an HDF5 file generated by the FDTD solver Meep.
author: Daniel Kotik
date:   18.01.2018
"""
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import h5py

#---------------------------------------------------------------------------------------------------
# set parameters
#---------------------------------------------------------------------------------------------------
n       = 1.54 / 1.0           # relative index of refraction
chi_deg = 45.0                 # angle of incidence in degrees
inc_deg = 90 - chi_deg         # inclination of the interface with respect to the x-axis
cutoff  = 30                   # cut off borders of data (remove PML layer up to and including line source placement)

#---------------------------------------------------------------------------------------------------
# import data from HDF file(s)
#---------------------------------------------------------------------------------------------------
path = "simulations/DK_meep-01.03.2018 11_08_44/LaguerreGauss3d_C-out/"
filename_real = path + "e_real2_s-000001540.h5"
filename_imag = path + "e_imag2_s-000001540.h5"

with h5py.File(filename_real, 'r') as hf:
    #print("keys: %s" % hf.keys())
    data_real = hf['e_real2_s'][:]

with h5py.File(filename_imag, 'r') as hf:
    #print("keys: %s" % hf.keys())
    data_imag = hf['e_imag2_s'][:]

data = data_real + data_imag
del data_imag                                       # free memory early

orig_shape = np.shape(data)

print "file size in MB: ", np.round(data.nbytes / 1024 / 1024, 2)
print "data (max, min): ", (np.round(data.max(), 2), np.round(data.min(), 2))
print "original shape:  ", orig_shape

data = data[cutoff:-cutoff, cutoff:-cutoff, cutoff:-cutoff] / data.max()
new_shape = np.shape(data)
print "cutted shape:    ", new_shape

## calculate center of 3d array data in pixel coordinates
center = (int((new_shape[0] - 1)/2), int((new_shape[1] - 1)/2), int(np.rint((data.shape[2] - 1)/2)))

#------------------------------------------------------------------------------------------------------------------
# calculating propagation directions of the secondary beams according to geometric optics
#------------------------------------------------------------------------------------------------------------------
eta_rad = np.arcsin((1.0/n) * np.sin(np.deg2rad(chi_deg)))   # angle of refraction in radians

## properties of the k-vectors
vec_length = 150

## (x, y)-components of the central k-vectors (in pixel coordinates)
center_x_y = (int((new_shape[0] - 1)/2), int((new_shape[1] - 1)/2))

vec_inc = (center[0] - vec_length, center[1])
vec_ref = (center[0] + int(np.rint(vec_length * np.sin(np.deg2rad(chi_deg - inc_deg)))),
           center[1] + int(np.rint(vec_length * np.cos(np.deg2rad(chi_deg - inc_deg)))))
vec_tra = (center[0] + int(np.rint(vec_length * np.sin(eta_rad + np.deg2rad(inc_deg)))),
           center[1] - int(np.rint(vec_length * np.cos(eta_rad + np.deg2rad(inc_deg)))))

components = [vec_inc, vec_ref, vec_tra]


#------------------------------------------------------------------------------------------------------------------
# obtaining cut-plane data position
#------------------------------------------------------------------------------------------------------------------
delta_deg = 20           # opening angle

## degree to radians conversion
delta_rad = np.deg2rad(delta_deg)
chi_rad   = np.deg2rad(chi_deg)
inc_rad   = np.deg2rad(inc_deg)

## calculate margins of the cut-plane for the respective beams in pixel coordinates
cut_inc = (center[0] - vec_length, center[1] - int(np.rint(vec_length * np.tan(delta_rad))),
           center[0] - vec_length, center[1] + int(np.rint(vec_length * np.tan(delta_rad))))
cut_ref = (center[0] + int(np.rint((vec_length / np.cos(delta_rad)) * np.sin(chi_rad - delta_rad - inc_rad))),
           center[1] + int(np.rint((vec_length / np.cos(delta_rad)) * np.cos(chi_rad - delta_rad - inc_rad))),
           center[0] + int(np.rint((vec_length / np.cos(delta_rad)) * np.sin(chi_rad + delta_rad - inc_rad))),
           center[1] + int(np.rint((vec_length / np.cos(delta_rad)) * np.cos(chi_rad + delta_rad - inc_rad))))
cut_tra = (center[0] + int(np.rint((vec_length / np.cos(delta_rad)) * np.sin(eta_rad - delta_rad + inc_rad))),
           center[1] - int(np.rint((vec_length / np.cos(delta_rad)) * np.cos(eta_rad - delta_rad + inc_rad))),
           center[0] + int(np.rint((vec_length / np.cos(delta_rad)) * np.sin(eta_rad + delta_rad + inc_rad))),
           center[1] - int(np.rint((vec_length / np.cos(delta_rad)) * np.cos(eta_rad + delta_rad + inc_rad))))

x0, y0, x1, y1 = cut_tra
width  = int(np.hypot(x1 - x0, y1 - y0))            # width of the cut-plane (determined by vec_length and delta_deg)
x, y   = np.linspace(x0, x1, width, dtype=np.int), np.linspace(y0, y1, width, dtype=np.int)

data_cut = data[x, y, :]  # TODO: Slice outside boundary possible? Fill with NaN?

#------------------------------------------------------------------------------------------------------------------
# visualising 
#------------------------------------------------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))

## visualise intensity dirstribution within the plane of incidence
data_poi = data[:,:,center[2]]                   # slice within the plane of incidence
ax1.imshow(np.transpose(data_poi), origin="lower", cmap=plt.cm.hot, interpolation='None')

## visualise k-vectors wihtin the plane of incidence
for i in [0,1,2]:
    ax1.plot([center[0], components[i][0]],
             [center[1], components[i][1]], '--', color="white")

## visualise cut line
ax1.plot([x0, x1], [y0, y1], 'ro-')

## subfigure properties
ax1.set_title("plane of incidence")
ax1.set_xlabel('x')                                 # labels are according to Meep
ax1.set_ylabel('y')


## visualise transverse intensity distribution with respect to the axis of the central wave vector
ax2.imshow(np.transpose(data_cut), origin="lower", cmap=plt.cm.gist_stern_r, interpolation='None')

## visualise geometric center point
ax2.axhline(center[2], color='w', lw=0.5)
ax2.axvline(int(np.rint((data_cut.shape[0] - 1)/2)), color='w', lw=0.5)

## subfigure properties
ax2.set_title("cut-plane")
ax2.set_xlabel('x')                                 # labels are according to Bliokh&Aiello's beam coordinate system
ax2.set_ylabel('z')


plt.tight_layout()
plt.show()

## free memory
try:
    del data, data_poi, data_real
except:
    pass
