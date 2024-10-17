import matplotlib.pyplot as plt
import numpy as np
from pv_self_consumption_api.models import Parameters, Result
from pathlib import Path
import pandas as pd
import os

#--check the compliance of the inputs and parameters
def check_compliance_inputs(supply,demand,price_sale,price_buy,Emax,Imax,Bmax,ts_in,ts_out,Beff,B0f,dB,Nscen,dt):
    #
    eps=1.e-6
    #
    assert price_sale < price_buy, 'price_sale has to be smaller than price_buy to maximize self-consumption'
    #
    assert dt > 0, f'dt has to be strictly positive ({dt})'
    assert abs(1/dt - int(1/dt)) < eps, f'dt should be a fraction of an hour {dt}'
    #
    assert dB > 0, f'dB has to be strictly positive ({dB})'
    assert Emax >= 0, f'Emax has to be positive ({Emax})'
    assert Imax >= 0, f'Imax has to be positive ({Imax})'
    assert Bmax > 0, f'Bmax has to be strictly positive ({Bmax})'
    assert ts_in > 0, f'ts_in has to be strictly positive ({ts_in})'
    assert ts_out > 0, f'ts_out has to be strictly positive ({ts_out})'
    assert Beff > 0, f'Beff has to be strictly positive ({Beff})'
    assert Beff <= 1, f'Beff has to be less than unity ({Beff})'
    assert B0f >= 0, f'B0f has to be positive ({B0f})'
    assert B0f <= 1, f'B0f has to be less than 1 ({B0f})'
    assert Nscen >= 100, f'Nscen has to be larger than 100 ({Nscen})'
    assert Nscen <= 10000, f'Nscen has to be less than 10000 ({Nscen})'
    #
    assert (demand.L).any() >=0, 'all of the L values have to be positive'
    assert (demand.P).any() >=0, 'all of the P values have to be positive'
    assert (demand.E).any() >=0, 'all of the E values have to be positive'
    assert (demand.Pmax).any() >=0, 'all of the Pmax values have to be positive'
    #
    for usage,row in demand.iterrows():
        L=row.L
        P=row.P
        E=row.E
        Pmax=row.Pmax
        i1=row.i1
        i2=row.i2
        uniform=row.uniform
        intermittent=row.intermittent
        assert i1 >= 0, f'i1 for usage {usage} has to be larger or equal to 0 ({i1})'
        assert i2 <= len(supply), f'i2 for usage {usage} has to be smaller or equal to the size of supply {i2}'
        assert i2 > i1, f'i2 for usage {usage} has to be strictly larger than i1 ({i2} <= {i1})'
        assert i2-i1>=L, f'i2-i1 for usage {usage} has to be larger or equal to L ({i2-i1} < {L})'
        assert (uniform==True) | (intermittent==True), f'uniform and intermittent cannot be both False for {usage}'
        if uniform:
           assert L >= 1, f'L for uniform usage {usage} has to be larger or equal to 1 ({L})'
           assert P >= 1, f'P for uniform usage {usage} has to be larger or equal to 1 ({P})'
           assert E == 0, f'E for uniform usage {usage} has to be equal to 0 ({E})'
           assert Pmax == 0, f'Pmax for uniform usage {usage} has to be equal to 0 ({Pmax})'
        else:
           assert L == 0, f'L for non-uniform usage {usage} has to be equal to 0 ({L})'
           assert P == 0, f'P for non-uniform usage {usage} has to be equal to 0 ({P})'
           assert E >= 1, f'E for non-uniform usage {usage} has to be larger or equal to 1 ({E})'
           assert Pmax >= 1, f'Pmax for non-uniform usage {usage} has to be larger or equal to 1 ({Pmax})'
           assert (i2-i1)*Pmax >= E, f'Pmax for non-uniform usage {usage} has to be large enough to allow completion of E ({i1=}, {i2=}, {Pmax=}, {E=})'
    #
    return


def read_demand(demand_file_path: Path)-> pd.DataFrame:
    try:
        demand = pd.read_csv(demand_file_path, skiprows=12, skipinitialspace=True)
        demand.set_index('usage', inplace=True)
        return demand
    except Exception as e:
        raise Exception(f'unable to read demand file: {str(e)}')


def make_plot(parameters: Parameters, result: Result, demand_file_path: Path, plots_dir_path: Path = Path('./plots/')) -> None:
    make_figure(parameters.price_buy, parameters.price_sale, read_demand(demand_file_path),\
                result.Cusage, result.P, result.C, result.Enet, parameters.Emax,\
                parameters.Imax, result.Curt, result.L, result.Bnet, result.Bstates,\
                len(parameters.supply), plots_dir_path)


#--make plots
def make_figure(price_buy, price_sale, demand, Cusage, P, C, Enet, Emax, Imax, Curt,
                L, Bnet, Bstates, Ntimes, dirplots: Path):
    #
    eps=1e-6
    #
    #--convert uniform prices to numpy array
    if isinstance(price_buy,(int,float)):
        price_buy=np.ones((Ntimes))*price_buy
    if isinstance(price_sale,(int,float)):
        price_sale=np.ones((Ntimes))*price_sale
    #
    #--define figure
    fig, axs = plt.subplots(5,figsize=(6,8))
    #
    axs[0].stairs(price_sale,label='Sale')
    axs[0].stairs(price_buy,label='Buy')
    axs[0].set_ylabel('Price')
    axs[0].set_xlim(0,Ntimes+eps)
    axs[0].set_ylim(0,0.3)
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
    if not os.path.exists(dirplots): os.makedirs(dirplots)
    plt.savefig(dirplots.joinpath('bess_timeseries.png'))
    plt.close()
    #
    return