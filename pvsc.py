import yaml
from pathlib import Path
import argparse
import pv_self_consumption_api.client_api as client_api
import pv_self_consumption_api.utils as utils
import sys

PARAMETERS_EXAMPLES = \
"""\
#--parameters of the optimisation system
#---------------------------------------
#--timestep (hr/timestep)
#--for now 1.0 hour is recommended
dt: 1.0
#--number of consumption scenarios to be considered
#--in the range 100 to 10000, 1000 is a good number
Nscen: 1000

#--parameters of the PV-battery system
#-------------------------------------
#--sale price for electricity exported to the grid (€/kWh)
price_sale: 0.06
#--buy price for electricity imported from the grid (€/kWh)
price_buy: 0.20
#--maximum export (kW)
Emax: 5                    
#--maximum import (kW)
Imax: 8                    
#--max battery storage (kWh)
Bmax: 10.0                 
#--timescale of battery charge (hr)
ts_in: 5.0                 
#--timescale of battery discharge (hr)
ts_out: 5.0                
#--efficiency of battery charge-discharge cycle (unitless)
Beff: 0.8                  
#--battery initial state (unitless, fraction of Bmax)
B0f: 0.5                   
#--battery discretisation step (kWh)
dB: 0.1                    
#
#--forecast of the production for the next Ntimes times by timestep (kW)
#-----------------------------------------------------------------------
supply: [0., 0., 0., 0., 0., 0., 0., 3., 8., 10., 14., 16., 4., 4., 10., 8., 3., 0., 0., 0., 0., 0., 0., 0.]
"""

DEMAND_EXAMPLE =\
"""\
#--input file to parametrize the flexibility in the demand
#--all numbers are integers
#
#--usage: name of usage 
#--uniform: boolean that determines if usage requires a uniform power or not
#--intermittent: boolean that determines if usage can be intermittent (stopped and restarted) or not
#--L: length, number of timesteps usage is required, for uniform power usages only
#--P: power of usage, in kW, for uniform power usages only
#--E: total energy required for non-uniform usages only, in kW.timestep (ie not multiplied by the duration of the timestep)
#--Pmax: maximum power of usage for non-uniform usages only, in kW
#--i1: index of start of time window for usage (i1 included)
#--i2: index of end of time window for usage (i2 not included)
usage,   uniform,  intermittent, L,  P,  E,   Pmax,  i1,  i2
car1,    False,    True,         0,  0,  10,  4,     0,   12
car2,    True,     True,         10, 5,  0,   0,     0,   18
wash,    True,     False,        1,  2,  0,   0,     8,   11
cook,    True,     False,        2,  1,  0,   0,     10,  13
heater,  False,    True,         0,  0,  4,   2,     20,  24
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='pvsc',\
                                     description='PV self consumption optimisation API client')
    
    subparsers = parser.add_subparsers(help='available commands', required=True)
    
    parser_optimization = subparsers.add_parser('optimize', help='run optimisation')
    parser_optimization.add_argument('parameter_file_path', metavar='PARAMETER_FILE_PATH', type=str, help='the parameter yaml file path')
    parser_optimization.add_argument('demand_file_path', metavar='DEMAND_FILE_PATH', type=str, help='the path to the demand csv file')
    parser_optimization.add_argument('-m', '--make-plots', default=False, action='store_true', help='save plots')
    parser_optimization.add_argument('-p', '--port', default=client_api.DEFAULT_API_PORT, type=int, help='specify the port number')
    parser_optimization.add_argument('-H', '--host', default=client_api.DEFAULT_API_HOST, type=str, help='specify the API host')

    parser_example = subparsers.add_parser('example', help='generate file examples')
    parser_example.add_argument('-p', '--parameters', default=False, action='store_true', help='generate an example of a parameter file')
    parser_example.add_argument('-d', '--demand'    , default=False, action='store_true', help='generate an example of a demand file')

    result = parser.parse_args()
    return result


def load_parameters(file_path: Path) -> dict:
    with open(file_path, 'r') as file:
        parameters = yaml.safe_load(file)
    return parameters


def print_parameter_file_example() -> None:
    print(PARAMETERS_EXAMPLES)


def print_demand_file_example() -> None:
    print(DEMAND_EXAMPLE)

def main() -> int:
    args = parse_args()
    if 'demand_file_path' in args:
        try:
            result, parameters = client_api.optimize_sc(parameter_file_path=Path(args.parameter_file_path),\
                                                        demand_file_path=Path(args.demand_file_path),
                                                        port=args.port,
                                                        host=args.host)
            print(result.model_dump_json())
            if args.make_plots:
                utils.make_plot(parameters=parameters, result=result, demand_file_path=args.demand_file_path)
        except Exception as e:
            print(f'[ERROR] {str(e)}', file=sys.stderr)
            return 1
    else:
        if args.parameters:
            print_parameter_file_example()
        if args.demand:
            print_demand_file_example()
    return 0


if __name__ == '__main__':
    main_exit_code = main()
    exit(main_exit_code)
