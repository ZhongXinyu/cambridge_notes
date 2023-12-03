## Solution to Problem Sheet 3 Question 1
## once again more optimal solutions will be available
import numpy as np np.random.seed (210187)
from scipy.optimize import brute, minimize from scipy.integrate import quad from scipy.stats import moment import matplotlib.pyplot as plt plt.style.use('code/mphil.mplstyle') from jacobi import propagate from iminuit import cost, Minuit import sys sys.path.append (' $PWD/code')
from accept_reject import accept_reject_id, check_ok_plot from tabulate import tabulate
if __name__==".
    _main_
xrange = [-0.95,0.95]
alpha = 0.5
beta = 0.5
def dk (k):
return (xrange [1]**k - xrange [0]**k) / k
N = 1/ ( dk (1) + alpha×dk (2) + beta*dk (3) )
func = lambda x: N* (1 + alpha*x + beta*x**2)
# run the accept-reject
dset = accept_reject_1d ( func, range=xrange, size=2000 )
check_ok_plot ( func, range, dset, bins=40, save=f'figs /mom_gen.
pdf ' )
dset = np.asarray (dset)
np. save (' ../s1_principles_of_data_science/datasets/mom_data.py' , dset)
# MoM estimate
m1_hat = moment (dset,
moment=1, center=0)
m2_hat = moment (dset,
moment=2, center=0)
def alpha (mi, m2):
numerator = (m1*dk (3) - dk (4)) * (m2*dk (1) -dk (3)) - (m1*dk (1) -
dk (2) ) * (m2* dk (3) - dk (5) )
denominator = (m1*dk (2) - dk (3))* (m2*dk (3) -dk (5)) - (m1*dk (3
)-dk (4)) * (m2*dk (2) -dk (4) )
return numerator / denominator
def beta (m1, m2):
numerator = (m1*dk (1) - dk (2)) * (m2*dk (2) -dk (4)) - (m1*dk (2) -
dk (3)) * (m2*dk (1) -dk (3) )
denominator = (mi*dk (2) - dk (3))* (m2*dk (3) -dk (5)) - (mi*dk (3