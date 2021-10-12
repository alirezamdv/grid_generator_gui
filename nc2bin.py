#!/usr/bin/python
import math

import netCDF4 as nc
import numpy as np
from pathlib import Path
import argparse
import os


def write_netCDF_variables_to_bin32(path_to_nc: str = None) -> object:
    if not path_to_nc:
        print(" please provide the path to .nc file!")
        exit(1)
    if not os.path.isfile(path_to_nc) or not path_to_nc.endswith(".nc"):
        print("the path is not valid!")
        exit(1)
    dir_path = os.path.dirname(os.path.realpath(__file__))

    try:
        name = Path(path_to_nc).stem
        os.makedirs(dir_path + f"/{name}_bin", exist_ok=True)
        out_path = dir_path + f"/{name}_bin"

    except Exception as e:
        print(e)
        exit(1)
    try:
        ds = nc.Dataset(path_to_nc)
    except Exception as e:
        print(e)

    data = {}
    for var in ds.variables:
        np_arr = ds[var][:]
        data[f'{var}'] = np.array(np_arr)
        data[f'{var}_max'] = np_arr.max()
        data[f'{var}_min'] = np_arr.min()
        data[f'{var}_len'] = np_arr.shape[0]
        data[f'{var}_path'] = f'{out_path}/{var}.bin32'
        # metadata[f'{var}_len'] = #out_path + f'/{var}.bin32'
        # metadata[f'var_max']=np_arr.max()
        with open(f'{out_path}/{var}.bin32', 'wb') as f:
            # metadata[f'{var}_binary_len'] = len(np_arr.tobytes())
            f.write(np_arr.tobytes())
            print(f'successfully wrote the {var} with {np_arr.shape} shape to {var}.bin32. ')
    return data

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='writing netCDF to binary file.')
#     parser.add_argument('path', type=str,
#                         help='path to the nc file!')
#     args = parser.parse_args()
#     write_netCDF_variables_to_bin32(args.path)
