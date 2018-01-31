"""
Purposes: - check Meep's integration routine
          - check implementation of Laguerre-Gauss beam fields
          - check transition from cartesian to spherical coordinates
"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

from scipy.integrate import dblquad

def complex_dblquad(func, a, b, gfun, hfun, **kwargs):
    """Integrates the real and imaginary part of the given function."""
    def real_func(x, y):
        return sp.real(func(x, y))
    def imag_func(x, y):
        return sp.imag(func(x, y))
    
    def real_integral():
        return dblquad(real_func, a, b, gfun, hfun, **kwargs)
    def imag_integral():
        return dblquad(imag_func, a, b, gfun, hfun, **kwargs)
    
    return (real_integral()[0] + 1j * imag_integral()[0], real_integral()[1:], imag_integral()[1:])


## test paramters (free space propagation, i.e. n1=n2=n_ref=1)
kw_0     = 8.0
m_charge = 0.0
n1      = 1.0

## meep specific
freq = 4.0

## derived values
k_vac = 2.0 * np.pi * freq
k1    = n1 * k_vac
w_0   = kw_0 / k_vac

def f_Gauss_cartesian(W_y, k_y, k_z): 
    """
    """
    return sp.exp(-(W_y ** 2.0) * (k_y ** 2.0 + k_z ** 2.0) / 4.0)
    
def f_Laguerre_Gauss_cartesian(W_y, m_charge, k_x, k_y, k_z):
    """
    """
    phi   = np.arctan2(k_y / k1, -k_z / k1)
    theta = np.arccos(k_x / k1)
    
    return f_Gauss_cartesian(W_y, k_y, k_z) * (theta ** np.abs(m_charge)) * sp.exp(1.0j * m_charge * phi)

def integrand_cartesian(x, y, z, k_y, k_z):
    """
    """
    ## first variant (taking the real part of the suqare root)
    #return f_Gauss_cartesian(w_0, k_y, k_z) * sp.exp(1.0j * (x * (sp.sqrt(k**2 - k_y**2 - k_z**2).real) + 
    #                                                         y * k_y + 
    #                                                         z * k_z))
    
    ## second variant (leave square root as is, but perform second integration with non-constant bounds)
    return f_Gauss_cartesian(w_0, k_y, k_z) * sp.exp(1.0j * (x * sp.sqrt(k1**2 - k_y**2 - k_z**2) + 
                                                             y * k_y + 
                                                             z * k_z))

def psi_cartesian(x, y, z):
    """
    """
    integrand_ = lambda k_y, k_z: integrand_cartesian(x, y, z, k_y, k_z)
    
    ## constant integration bounds (appropriate for first variant)
    #return complex_dblquad(integrand_, -k1, k1, lambda x: -k1, lambda x1: k)[0]
    
    ## non-constant integration bounds (appropriate for second variant)
    return complex_dblquad(integrand_, -k1, k1, lambda x: -np.sqrt(k1**2 - x**2), lambda x: np.sqrt(k1**2 - x**2))[0]
    
    
x_shift = -2.0
print "Gauss spectrum (cartesian): ", f_Gauss_cartesian(w_0, 1.0, 5.2)
print "L-G spectrum   (cartesian): ", f_Laguerre_Gauss_cartesian(w_0, 1.0, 0.1, 1.0, 5.2)
print "integrand      (cartesian): ", integrand_cartesian(x_shift, 0.3, 0.5, 4, 0)
print "psi            (cartesian): ", psi_cartesian(x_shift, 0.3, 0.1)

K_y = np.linspace(-k1, k1, 100)

#INTEGRAND = integrand_cartesian(x_shift, 0.0, 0.0, K_y, 0.0)
#plt.plot(K_y, INTEGRAND.real)
#plt.plot(K_y, INTEGRAND.imag)
#plt.show()