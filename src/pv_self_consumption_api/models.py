from pydantic import BaseModel
from pydantic.functional_validators import field_validator
import numpy as np

class Parameters(BaseModel):
    supply: list[float]
    price_sale: float
    price_buy: float
    Emax: float
    Imax: float
    Bmax: float
    ts_in: float
    ts_out: float
    Beff: float
    B0f: float
    dB: float
    Nscen: int
    dt: float

    @field_validator('supply')
    @classmethod
    def convert_ndarray_to_list(cls, value):
        if isinstance(value, np.ndarray):
            return np.array(value)
        else:
            return value


class Result(BaseModel):
    Cusage: dict[str, list[float]]
    P: list[float]
    C: list[float]
    Enet: list[float]
    Curt: list[float]
    Bnet: list[float]
    Bstates: list[float]
    L: list[float]

    @staticmethod
    def get_list_class_members():
        return vars(Result)['__annotations__'].keys()