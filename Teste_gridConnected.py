#import sympy as sp
import control as ctrl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# My modules 
from MMC import MMC
from LINEARCTRL import LINEARCTRL
from MMC_CTRL_NRF_I import MMC_CTRL_NRF_I
from bodeFromDataFrame import bodeFromDataFrame


import mplcursors
from DataFrameFromRF import DataFrameFromRF
from bodeFromDataFrame import bodeFromDataFrame
from rfPolarPlotFromDataFrame import rfPolarPlotFromDataFrame


# Rated paramenters of the system
Sr = 100e6
Vll = 69e3
Zbase = Vll**2/Sr
fbase = 60
wbase = 2*np.pi*fbase

# Definition of the Laplace-domain frequency
s = ctrl.tf('s')

# Grid impendance: different cases
# 1, 2, 3 represent three different modules
# a, b, c represent three differen X/R ratio
Zpu_module = np.array([0.02, 0.05, 0.1])
XoR_ratio = np.array([3, 5, 10])

Zg_list = [[Zbase*(Z/np.sqrt(1+XoR**2))*(1+(s*XoR/wbase)) for Z in Zpu_module] for XoR in XoR_ratio]
#print(Zg_list[1][1])


# Definition of the MMC with the same parameters considered in the Thesis
mmc_0 = MMC(s = s)

# Definition of the current cotroller used in the thesis
Ci_0 = LINEARCTRL(type='PR',kp=0.0005, kr=10,d=0,w0=2*np.pi*60,s=s)

# MMC model without considering the PLL (used in the thesis)
mmc_ctrl_i_0 = MMC_CTRL_NRF_I(Ci = Ci_0, s = s, Converter=mmc_0)


# Loop functions: To verify stability
Loop_list = [[Z*mmc_ctrl_i_0.Yac for Z in Zline] for Zline in Zg_list]


# Dataframes with the frequency responses
DT_Loop = [[DataFrameFromRF(G =Loop, s = s) for Loop in Loop_line] for Loop_line in Loop_list]


# Bode plots: Admitance
fig4,ax4 = bodeFromDataFrame([DataFrameFromRF(G=mmc_ctrl_i_0.Yac,s=s)])

# Polar plots
fig1,ax1 = rfPolarPlotFromDataFrame(DT_Loop[0], plotUnitaryCircle=True, plotAxis=True)
fig2,ax2 = rfPolarPlotFromDataFrame(DT_Loop[1], plotUnitaryCircle=True, plotAxis=True)
fig3,ax3 = rfPolarPlotFromDataFrame(DT_Loop[2], plotUnitaryCircle=True, plotAxis=True)


# Bode plots: loop
fig5,ax5 = bodeFromDataFrame(DT_Loop[0])
fig6,ax6 = bodeFromDataFrame(DT_Loop[1])
fig7,ax7 = bodeFromDataFrame(DT_Loop[2])
