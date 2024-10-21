from pydantic import BaseModel
from pydantic.functional_validators import field_validator
import numpy as np

class Parameters(BaseModel):
    supply: list[float]
    price_sale: float # Sale price for electricity exported to the grid (€/kWh)
    price_buy: float # Buy price for electricity imported from the grid (€/kWh)
    Emax: float # Maximum export (kW)
    Imax: float # Maximum import (kW)
    Bmax: float # Maxium battery storage (kWh)
    ts_in: float # Timescale of battery charge (hr)
    ts_out: float # Timescale of battery discharge (hr)
    Beff: float # Efficiency of battery charge-discharge cycle (unitless)
    B0f: float # Battery initial state (unitless, fraction of Bmax)
    dB: float # battery discretisation step (kWh)
    # Number of consumption scenarios to be considered
    # In the range 100 to 10000, 1000 is a good number
    Nscen: int
    # Timestep (hr/timestep)
    # For now 1.0 hour is recommended
    dt: float

    @field_validator('supply')
    @classmethod
    def convert_ndarray_to_list(cls, value):
        if isinstance(value, np.ndarray):
            return np.array(value)
        else:
            return value


class Result(BaseModel):
    Cusage: dict[str, list[float]] # Dictionary of usages as C[usage] in kW
    P: list[float] # Production (same as supply) in kW
    C: list[float] # Total consumption (sum over usages) in kW
    Enet: list[float] # Net export to the grid in kW, can be positive (export) or negative (import)
    Curt: list[float] # Curtailed production in kW
    Bnet: list[float] # Net battery charge in kW, can be positive (charge) or negative (discharge)
    Bstates: list[float] # Battery states by step of dB in kWh
    L: list[float] # Loss due to battery charge and discharge in kW
    
    # Computed for a timestep (dt):
    Production: float # in kWh
    Consumption: float # in kWh
    Export: float # in kWh
    Import: float # in kWh
    Loss: float # in kWh
    Curtail: float # in kWh
    Self_consumption_rate: float # in %
    Balance: float # in kWh
    Is_balanced: bool # if optimization is right or wrong