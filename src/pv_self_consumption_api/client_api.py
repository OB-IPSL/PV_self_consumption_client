import requests
from pathlib import Path
import yaml
import pv_self_consumption_api.utils as utils
from pv_self_consumption_api.models import Parameters, Result

DEFAULT_API_HOST = 'voc-dev.ipsl.fr'
DEFAULT_API_PORT = 9999
API_ROUTE = '/api/pv_self_consumption/optimisesc'


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
        demand = utils.read_demand(demand_file_path)
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
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        result = Result.model_validate_json(r.content)
        return result, parameters    