import client_api as client_api
import numpy as np
import pandas as pd
from pathlib import Path
import os
import time
from utils import make_figure

#
#--parameters of the optimisation system
#---------------------------------------
#--timestep (hr/timestep)
#--for now 1.0 hour is recommended
dt=1.0 
#--number of timesteps for optimising supply and demand
#--cost of calculations increase with Ntimes
Ntimes=24
#--number of consumption scenarios to be considered
#--in the range 100 to 10000, 1000 is a good number
Nscen=1000
#
#--parameters of the PV-battery system
#-------------------------------------
#--sale price for electricity exported to the grid (€/kWh)
price_sale=0.06
#--buy price for electricity imported from the grid (€/kWh)
price_buy=0.20
#--maximum export (kW)
Emax=5                    
#--maximum import (kW)
Imax=8                    
#--max battery storage (kWh)
Bmax=10.0                 
#--timescale of battery charge (hr)
ts_in=5.0
#--timescale of battery discharge (hr)
ts_out=5.0
#--timescale of storage decay (hr)
ts_decay=24.0
#--efficiency of battery charge-discharge cycle (unitless)
Beff=0.8                  
#--battery initial state (unitless, fraction of Bmax)
B0f=0.5                   
#--battery discretisation step (kWh)
dB=0.1                    
#
#--forecast of the production for the next Ntimes times by timestep (kW)
#-----------------------------------------------------------------------
supply=np.array([0.,0.,0.,0.,0.,0.,0.,3.,8.,10.,14.,16.,4.,4.,10.,8.,3.,0.,0.,0.,0.,0.,0.,0.])

#--initialise parameters for api client
parameters = client_api.create_parameters(globals().copy())

#--input file for flexible usage
demand_file_path = Path('usage.csv')

#--call and time api
print('')
print('Thank you for choosing our api')
start_time = time.time()
result = client_api.optimize_sc_stub(parameters=parameters, demand_file_path=demand_file_path)
end_time = time.time()
print('Result from api in ', "%.3f" %(end_time-start_time),' s')

#--load characteristics of the demand for the next Ntimes times and its flexibility
demand=pd.read_csv('usage.csv',skiprows=12,skipinitialspace=True)
demand.set_index('usage',inplace=True)

#--load outputs from the api
Cusage=result.Cusage
P=result.P
C=result.C
Enet=result.Enet
Curt=result.Curt
Bnet=result.Bnet
Bstates=result.Bstates
L=result.L
#
#--some post-processing of the results
#-------------------------------------
#
#--add initial state of battery to Bstates
Bstates=np.append([Bmax*B0f],Bstates)
#
#--convert Enet into net Import and net Export (kW)
I=np.where(Enet<=0,Enet,0.)
E=np.where(Enet>=0,Enet,0.)
#
#--compute total energies over the time period
Prod=P.sum()*dt
Cons=C.sum()*dt
Export=E.sum()*dt
Import=-I.sum()*dt
Curtail=Curt.sum()*dt
Loss=L.sum()*dt
#
#--compute self-consumption rate
self=(1+I.sum()/C.sum())*100
#
#--print results
print('')
print(f'Production  {Prod:.2f} kWh') 
print(f'Consumption {Cons:.2f} kWh') 
print(f'Export      {Export:.2f} kWh') 
print(f'Import      {Import:.2f} kWh') 
print(f'Loss        {Loss:.2f} kWh') 
print(f'Curtail     {Curtail:.2f} kWh') 
print(f'Self-consumption {self:.2f} %')

#--assert that fluxes balances out
eps=1.e-6
assert Prod+Import-Cons-Export-Loss-Curtail < eps, 'Energy fluxes do not balance out'
#
#--directory for plots
dirplots='./plots/'
if not os.path.exists(dirplots): os.makedirs(dirplots)
#
#--pltshow
pltshow=False
pltshow=True
#
#--make plots
make_figure(price_buy,price_sale,demand,Cusage,P,C,Enet,Emax,Imax,Curt,L,Bnet,Bstates,Ntimes,pltshow,dirplots)
#
