import requests
import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict
from pathlib import Path
from pydantic.functional_validators import field_validator
import yaml
import pandas as pd
import pv_self_consumption_api.utils as utils

DEFAULT_API_HOST = 'klima.ipsl.fr'
DEFAULT_API_PORT = 443
API_ROUTE = '/api/pv_self_consumption/optimisesc'

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
    
    def __str__(self) -> str:
        return super.__str__(self) # TODO


def numpy_array_decoder(object: dict):
        for key, value in object.items():
            if isinstance(value, list):
                object[key] = np.array(value)
            elif isinstance(value, dict):
                for k, v in value.items():
                    value[k] = np.array(value[k])
                object[key] = value
        return object   


def _check_files(parameter_file_path: Path, demand_file_path: Path)-> Parameters:
    
    if not parameter_file_path.exists():
        raise Exception('missing parameter file')
    if not demand_file_path.exists():
        raise Exception('missing demand file')
    with open(parameter_file_path, 'r') as parameter_file:
        try:
            dict_parameters = yaml.safe_load(parameter_file)
            result = Parameters(**dict_parameters)
        except Exception as e:
            raise Exception(f'unable to parse parameters: {str(e)}')
        try:
            demand = pd.read_csv(demand_file_path, skiprows=12, skipinitialspace=True)
            demand.set_index('usage', inplace=True)
        except Exception as e:
            raise Exception(f'unable to read demand file: {str(e)}')
        try:
            utils.check_compliance_inputs(demand=demand, **dict_parameters)
        except Exception as e:
            raise Exception(f'wrong parameters or demand: {str(e)}')
        return result


def optimize_sc(parameter_file_path: Path, demand_file_path: Path,
                port: int = DEFAULT_API_PORT, host: str = DEFAULT_API_HOST) -> tuple[Result, Parameters]:
    parameters = _check_files(parameter_file_path, demand_file_path)
    with open(demand_file_path, 'rb') as demand_file:
        files = {'demand_file': demand_file}
        r = requests.post(f'http://{host}:{port}/{API_ROUTE}', data={'data': parameters.model_dump_json()}, files=files)
        result = Result(r.json(object_hook=numpy_array_decoder))
        return result, parameters