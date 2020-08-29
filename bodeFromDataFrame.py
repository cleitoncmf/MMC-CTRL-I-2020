import matplotlib.pyplot as plt
import mplcursors # modeule for cursors 

# The argument must be a list of frames
def bodeFromDataFrame(dataFrameList):
    if not isinstance(dataFrameList, list):
        raise Exception("The argument is not a list") 

    fig, ax = plt.subplots(2,figsize=(15, 7))
    for item in dataFrameList:
        if 'f' not in item.columns:
            raise Exception("The data frame does not have the column f") 
        if 'Mag_dB' not in item.columns:
            raise Exception("The data frame does not have the column Mag_dB") 
        if 'phi' not in item.columns:
            raise Exception("The data frame does not have the column phi") 
        line0, = ax[0].plot(item['f'].to_numpy(), item['Mag_dB'].to_numpy())
        line1, = ax[1].plot(item['f'].to_numpy(), item['phi'].to_numpy())
    ax[0].set_xscale('log')
    ax[1].set_xscale('log')
    ax[1].set_xlabel('Frequency - Hz')
    ax[0].set_ylabel('Magnitude - dB')
    ax[1].set_ylabel('Phase - deg')
    ax[0].grid(color='k', linestyle='-', linewidth=0.5, alpha=0.7,dash_capstyle='butt')
    ax[1].grid(color='k', linestyle='-', linewidth=0.5, alpha=0.7,dash_capstyle='butt')
    ax[0].grid(which='minor',color='k', linestyle='--', linewidth=0.5, alpha=0.7,dash_capstyle='butt',dashes=(5, 5))
    ax[1].grid(which='minor',color='k', linestyle='--', linewidth=0.5, alpha=0.7,dash_capstyle='butt',dashes=(5, 5))
    #ax[0].set_xticklabels([])
    fig.align_ylabels(ax[:])
    
    # Configure the data cursor  
    c2 = mplcursors.cursor(multiple=True) # enabling the cursor
    @c2.connect("add")
    def _(sel):
        xi, yi = sel.target
        #gain_dBi = teste.loc[teste['f']==xi,'w'].values[0]
        sel.annotation.set_text(f"Freq.: {xi:.2f}Hz\nGain: {yi:.2f} dB\nPhase: {yi:.2f} deg\nValue: {yi:.2f}")


    plt.show()
    return fig, ax