import matplotlib.pyplot as plt
import mplcursors # module for cursors 
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.patches as mpatches


def rfPolarPlotFromDataFrame(dataFrameList, plotUnitaryCircle=False):
    if not isinstance(dataFrameList, list):
        raise Exception("The argument is not a list") 



    # Some Definitions
    #Labelfont = 22
    #TickLabelfont = 20
    LineWd = 2


    # Create the plot

    Lines  = []

    fig, ax = plt.subplots(1,figsize=(7, 7))



    for item in dataFrameList:
        if 'f' not in item.columns:
            raise Exception("The data frame does not have the column f") 
        if 'cplx' not in item.columns:
            raise Exception("The data frame does not have the column cplx") 

        xReal = np.real(item['cplx'].to_numpy())   
        yImag = np.imag(item['cplx'].to_numpy()) 
        line0, = ax.plot(xReal, yImag,'.')
        
        Lines.append(id(line0))

    if (plotUnitaryCircle):
        p = mpatches.Circle((0, 0), 1, alpha=0.1, edgecolor='k', facecolor='g', linestyle='--')
        ax.add_patch(p)

    # Configure the data cursor  
    c2 = mplcursors.cursor(multiple=True) # enabling the cursor
    @c2.connect("add")
    def _(sel):
        xi, yi = sel.target
        Mag = np.sqrt(xi**2 + yi**2)
        Phi = np.arctan2(yi, xi) * 180 / np.pi

        # This is a workaround to retrieve the frequency of the point
        # It should work if, and only if, the cursor does not point to interpoled values
        # Since I'm ploting the curve with '.', instead of '-' and '--', the cursor will only point to values in the input arrays 
        element = Lines.index(id(sel.artist))

        df = dataFrameList[element]

        xReal2 = np.real(df['cplx'].to_numpy())
        yImag2 = np.imag(df['cplx'].to_numpy())  

        positionX = np.where(xReal2 == xi)
        positionY = np.where(yImag2 == yi)

        # A small test to see if everything is working proplerly
        # Chances are, it will have conditions not covered by this test
        # It is a good idei to check this part in the future 
        if(positionX[0][0] == positionY[0][0]):
            f = df['f'].to_numpy()[positionX[0][0]]
        else:
            f = -1 # only a flag in case something go wrong


        if(yi>0):
            sel.annotation.set_text(f"Freq: {f:.2f}Hz\nMag: {Mag:.2f}\n Phi: {Phi:.2f}deg\nValue: {xi:.2f}+j{yi:.2f}")
        else:
            sel.annotation.set_text(f"Freq: {f:.2f}Hz\nMag: {Mag:.2f}\n Phi: {Phi:.2f}deg\nValue: {xi:.2f}-j{np.abs(yi):.2f}")
            


    plt.show()

    return fig, ax