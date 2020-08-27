# Function for computing the frequency response of a system and returning a dataframe with the result
import pandas as pd
import numpy as np
import control as ctrl
import sympy as sp


# wBounds - list with the minimum and maximum frequencies in rad/s (It is predefined)
def DataFrameFromRF(G, s, wBounds = (2*np.pi,1000*2*np.pi)):


    def CreateFrameRF(Gs):
        fr =  pd.DataFrame(columns=['f', 'w', 'cplx', 'Mag', 'Mag_dB', 'phi'])
        fr['Mag'], fr['phi'], fr['w'] = ctrl.bode(Gs,omega_limits=wBounds, Plot=False)
        fr['f'] = fr['w'].values/(2*np.pi)
        fr['Mag_dB'] = 20*np.log10(fr['Mag'].values)
        fr['cplx'] = fr['Mag'].values * np.exp(1j*fr['phi'].values)
        fr['phi'] = np.rad2deg(fr['phi'].values)
        return fr
    
    # Convert symbolic expression in trasnfer function
    def SympytoNumpyFrac(Gs):
        num,den = sp.fraction(Gs.together()) 
        #
        num = sp.Poly(num.expand(),s)
        den = sp.Poly(den.expand(),s)
        #
        c_num = np.array(num.all_coeffs()).astype(np.float64)
        c_den = np.array(den.all_coeffs()).astype(np.float64)
        #
        return ctrl.tf(c_num,c_den)

    # Compute frequency response for an control object 
    if 'minreal' in dir(G):
        return CreateFrameRF(G)

    # Compute frequency response for an sympy object    
    elif 'simplify' in dir(G):
        return CreateFrameRF(SympytoNumpyFrac(G))

    else:
        print('\33[33m' +  'Warning: G might not be neither an transfer-fucntion nor a symbolic-math object' + '\33[0m')
        return G
    
    
    
    
    
    
    