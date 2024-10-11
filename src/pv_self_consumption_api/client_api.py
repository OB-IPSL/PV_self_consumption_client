import requests
import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict
from pathlib import Path
from typing import Any
from pydantic.functional_validators import field_validator


API_URL = 'http://localhost:9999/api/optimisesc'


class Parameters(BaseModel):
    model_config = ConfigDict(extra='ignore')
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


class Result:
    Cusage: dict[str, NDArray]
    P: NDArray
    C: NDArray
    Enet: NDArray
    Curt: NDArray
    Bnet: NDArray
    Bstates: NDArray
    L: NDArray
    
    def __init__(self, raw_result: dict[str, list[float]|dict[str, list[float]]]) -> None:
        for key, value in raw_result.items():
            setattr(self, key, value)

    @staticmethod
    def get_list_class_members():
        return vars(Result)['__annotations__'].keys()

def create_parameters(script_variables: dict[Any, Any]) -> Parameters:
    return Parameters(**script_variables)


def numpy_array_decoder(object: dict):
        for key, value in object.items():
            if isinstance(value, list):
                object[key] = np.array(value)
            elif isinstance(value, dict):
                for k, v in value.items():
                    value[k] = np.array(value[k])
                object[key] = value
        return object   


def optimize_sc_stub(parameters: Parameters, demand_file_path: Path) -> Result:
    with open(demand_file_path, 'rb') as demand_file:
        files = {'demand_file': demand_file}
        r = requests.post(API_URL, data={'data': parameters.model_dump_json()}, files=files)
        result = Result(r.json(object_hook=numpy_array_decoder))
        return result
