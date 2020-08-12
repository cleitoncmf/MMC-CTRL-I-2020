# Function for computing the frequency response of a system and returning a dataframe with the result
import pandas as pd
import numpy as np

def DataFrameFromRF(G, s, freqList):


    if 'minreal' in dir(G):
        return 1
    elif 'simplify' in dir(G):
        return 2
    else:
        print('\33[33m' +  'Warning: G might not be neither an transfer-fucntion nor a symbolic-math object' + '\33[0m')
        return 3
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #return np.array([1,2,3,4,5])