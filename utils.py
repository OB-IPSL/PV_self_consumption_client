import matplotlib.pyplot as plt

#--make plots from output of optimisation
def make_figure(price_buy,price_sale,demand,Cusage,P,C,Enet,Emax,Imax,Curt,L,Bnet,Bstates,Ntimes,pltshow,dirplots):
    #
    eps=1e-6
    #
    fig, axs = plt.subplots(5,figsize=(6,8))
    #
    axs[0].stairs([price_sale]*Ntimes,label='Sale')
    axs[0].stairs([price_buy]*Ntimes,label='Buy')
    axs[0].set_ylabel('Price')
    axs[0].set_xlim(0,Ntimes+eps)
    axs[0].set_xticks(range(0,Ntimes))
    axs[0].set_xticklabels([])
    axs[0].set_title('Electricity price (in €/kWh)')
    axs[0].legend(loc='upper left',fontsize=8)
    #
    for usage in demand.index:
       axs[1].stairs(Cusage[usage],label=usage)
    axs[1].plot([0,Ntimes],[0,0],c='black',linewidth=0.5)
    axs[1].set_xlim(0,Ntimes+eps)
    axs[1].set_xticks(range(0,Ntimes))
    axs[1].set_xticklabels([])
    axs[1].set_ylabel('Power')
    axs[1].set_title('Consumption by usage (kW)')
    axs[1].legend(loc='upper left',fontsize=8)
    #
    axs[2].stairs(P,label='P')
    axs[2].stairs(C,label='C (tot)')
    axs[2].stairs(Enet,label='E (net)')
    axs[2].plot([0,Ntimes],[0,0],c='black',linewidth=0.3)
    axs[2].plot([0,Ntimes],[Emax,Emax],c='black',linewidth=0.3,linestyle='dotted')
    axs[2].plot([0,Ntimes],[-Imax,-Imax],c='black',linewidth=0.3,linestyle='dotted')
    axs[2].set_xlim(0,Ntimes+eps)
    axs[2].set_xticks(range(0,Ntimes))
    axs[2].set_xticklabels([])
    axs[2].set_ylabel('Power')
    axs[2].set_title('Electricity fluxes (kW)')
    axs[2].legend(loc='upper left',fontsize=8)
    #
    axs[3].stairs(Curt,label='Curt')
    axs[3].stairs(L,label='Loss')
    axs[3].plot([0,Ntimes],[0,0],c='black',linewidth=0.3)
    axs[3].set_xlim(0,Ntimes+eps)
    axs[3].set_xticks(range(0,Ntimes))
    axs[3].set_xticklabels([])
    axs[3].set_ylabel('Power')
    axs[3].set_title('Electricity fluxes (kW)')
    axs[3].legend(loc='upper left',fontsize=8)
    #
    axs[4].stairs(Bnet,label='B in/out')
    axs[4].plot(Bstates,label='B SoC',zorder=10,c='red')
    axs[4].plot([0,Ntimes],[0,0],c='black',linewidth=0.5)
    axs[4].set_xlim(0,Ntimes+eps)
    axs[4].set_xticks(range(0,Ntimes+1))
    axs[4].set_xlabel('Hours in the day')
    axs[4].set_ylabel('SoC / Power')
    axs[4].set_title('Battery SoC (kWh) / Battery in/out (kW)')
    axs[4].legend(loc='upper left',fontsize=8)
    #
    fig.tight_layout()
    plt.savefig(dirplots+'bess_timeseries.png')
    if pltshow: plt.show()
    plt.close()
    #
    return
