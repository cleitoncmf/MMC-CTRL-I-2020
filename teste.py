import sympy as sp
import control as ctrl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# My modules 
from MMC import MMC
from LINEARCTRL import LINEARCTRL
from MMC_CTRL_NRF_I import MMC_CTRL_NRF_I
from bodeFromDataFrame import bodeFromDataFrame





# Definition of the Laplace-domain frequency
s = ctrl.tf('s')
#s = sp.Symbol('s')

# Definition of the MMC with the same parameters considered in the Thesis
mmc_0 = MMC(s = s)

# Definition of the current cotroller used in the thesis
Ci_0 = LINEARCTRL(type='PR',kp=0.0001, kr=0.01,d=0,w0=2*np.pi*60,s=s)

# MMC model without considering the PLL (used in the thesis)
mmc_ctrl_i_0 = MMC_CTRL_NRF_I(Ci = Ci_0, s = s, Converter=mmc_0)



# different controllers 

Ci_10 = LINEARCTRL(type='PR',kp=0.001, kr=0.01,d=0,w0=2*np.pi*60,s=s)
Ci_20 = LINEARCTRL(type='PR',kp=0.01, kr=0.01,d=0,w0=2*np.pi*60,s=s)


# Models for the different control settings
mmc_ctrl_i_10 = MMC_CTRL_NRF_I(Ci = Ci_10, s = s, Converter=mmc_0)
mmc_ctrl_i_20 = MMC_CTRL_NRF_I(Ci = Ci_20, s = s, Converter=mmc_0)


import mplcursors
from DataFrameFromRF import DataFrameFromRF
from bodeFromDataFrame import bodeFromDataFrame

teste = DataFrameFromRF(G =mmc_ctrl_i_0.Yac, s = s)
teste2 = DataFrameFromRF(G =-2*mmc_ctrl_i_0.Yac, s = s)
#teste.head()

bodeFromDataFrame([teste,teste2])