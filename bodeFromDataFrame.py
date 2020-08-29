import matplotlib.pyplot as plt
import mplcursors # module for cursors 
import numpy as np
from scipy.interpolate import interp1d

# The argument must be a list of frames
def bodeFromDataFrame(dataFrameList):
    if not isinstance(dataFrameList, list):
        raise Exception("The argument is not a list") 

    # Some Definitions
    Labelfont = 22
    TickLabelfont = 20
    LineWd = 2

    # Create the plot   
    UpperLines = []
    bottomLines  = []

    fig, ax = plt.subplots(2,figsize=(15, 7))

    for item in dataFrameList:
        if 'f' not in item.columns:
            raise Exception("The data frame does not have the column f") 
        if 'Mag_dB' not in item.columns:
            raise Exception("The data frame does not have the column Mag_dB") 
        if 'phi' not in item.columns:
            raise Exception("The data frame does not have the column phi") 
        line0, = ax[0].plot(item['f'].to_numpy(), item['Mag_dB'].to_numpy(), linewidth=LineWd)
        line1, = ax[1].plot(item['f'].to_numpy(), item['phi'].to_numpy(), linewidth=LineWd)
        UpperLines.append(id(line0)) # list of object indentifier
        bottomLines.append(id(line1)) # list of object indentifier

    # Configure the aesthetic pattern the plot 
    ax[0].autoscale(enable=True, axis='x', tight=True)    
    ax[1].autoscale(enable=True, axis='x', tight=True)  

    ax[0].set_xscale('log')
    ax[1].set_xscale('log')

    ax[1].set_xlabel('Frequency - Hz',fontsize=Labelfont, fontname='serif')
    ax[0].set_ylabel('Magnitude - dB',fontsize=Labelfont, fontname='serif')
    ax[1].set_ylabel('Phase - deg',fontsize=Labelfont, fontname='serif')

    ax[0].tick_params(axis='both', which='major', labelsize=TickLabelfont)
    ax[1].tick_params(axis='both', which='major', labelsize=TickLabelfont)

    # Set the font name for axis tick labels to be serif
    for tick in ax[1].get_xticklabels():
        tick.set_fontname('serif')
    for tick in ax[1].get_yticklabels():
        tick.set_fontname('serif')
    for tick in ax[0].get_yticklabels():
        tick.set_fontname('serif')

    #ax[0].grid(color='k', linestyle='-', linewidth=0.5, alpha=0.7,dash_capstyle='butt')
    #ax[1].grid(color='k', linestyle='-', linewidth=0.5, alpha=0.7,dash_capstyle='butt')
    ax[0].grid(color='k', linestyle='-', linewidth=1, dash_capstyle='butt', alpha=0.20)
    ax[1].grid(color='k', linestyle='-', linewidth=1, dash_capstyle='butt', alpha=0.20)

    #ax[0].grid(which='minor',color='k', linestyle='--', linewidth=0.5, alpha=0.7,dash_capstyle='butt',dashes=(5, 5))
    #ax[1].grid(which='minor',color='k', linestyle='--', linewidth=0.5, alpha=0.7,dash_capstyle='butt',dashes=(5, 5))
    ax[0].grid(which='minor',color='k', linestyle='--', linewidth=1, alpha=0.20, dash_capstyle='butt', dashes=(5, 5))
    ax[1].grid(which='minor',color='k', linestyle='--', linewidth=1, alpha=0.20, dash_capstyle='butt', dashes=(5, 5))
    
    ax[0].set_xticklabels([])
    
    fig.align_ylabels(ax[:])
    fig.tight_layout()
    
    # Configure the data cursor  
    c2 = mplcursors.cursor(multiple=True) # enabling the cursor
    @c2.connect("add")
    def _(sel):
        xi, yi = sel.target

        # if the click was in the Magnitude chart, the phase presented is estimated through interpolation
        # if the click was in the Phase chart, the magnitude presented is estimated through interpolation
        try:
            element = UpperLines.index(id(sel.artist))
            df = dataFrameList[element]
            finterpPhi = interp1d(df['f'].values, df['phi'].values, kind='cubic')
            sel.annotation.set_text(f"Freq: {xi:.2f}Hz\nMag: {yi:.2f}dB\nPhi: {finterpPhi(xi):.2f}deg")
        except:
            element = bottomLines.index(id(sel.artist))
            df = dataFrameList[element]
            finterpMag = interp1d(df['f'].values, df['Mag_dB'].values, kind='cubic')
            sel.annotation.set_text(f"Freq: {xi:.2f}Hz\nMag: {finterpMag(xi):.2f}dB\nPhi: {yi:.2f}deg")

    plt.show()
    return fig, ax