def bodeFromDataFrame(dataFrameList):
    fig, ax = plt.subplots(2,figsize=(15, 7))
    for item in dataFrameList:
        line0, = ax[0].plot(item['f'].to_numpy(), item['magdB'].to_numpy())
        line1, = ax[1].plot(item['f'].to_numpy(), item['phaseDegree'].to_numpy())
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
    return fig, ax