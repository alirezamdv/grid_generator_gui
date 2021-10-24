#!/usr/bin/python
import math

import netCDF4 as nc
import numpy as np
from pathlib import Path
import argparse
import os


class NetcdfToBin:

    def __init__(self, path_to_nc: str = None):
        if not path_to_nc:
            print(" please provide the path to .nc file!")
            exit(1)
        if not os.path.isfile(path_to_nc) or not path_to_nc.endswith(".nc"):
            print("the path is not valid!")
            exit(1)
        self.path = path_to_nc
        self.name = Path(path_to_nc).stem
        self.dir_path = "."
        self.ds = self.read_()
        self.mk_dir()
        self.data = {}
        self.out_path = self.dir_path + f"/{self.name}_bin"
        self.get_data(write=False)

    def read_(self):
        try:
            return nc.Dataset(self.path)
        except Exception as e:
            print(e)

    def mk_dir(self):
        try:
            os.makedirs(self.dir_path + f"/{self.name}_bin", exist_ok=True)
        except Exception as e:
            print(e)
            exit(1)

    def get_data(self, i=None, j=None, write=False):
        for var in self.ds.variables:
            var_name = 'lon' if 'lon' in var and not any(char.isdigit() for char in var) else 'lat' if 'lat' in var\
                else 'topo' if 'topo' in var else var
            np_arr = self.ds[var][i:j]
            self.data[f'{var_name}'] = np.array(np_arr)
            self.data[f'{var_name}_max'] = np_arr.max()
            self.data[f'{var_name}_min'] = np_arr.min()
            self.data[f'{var_name}_len'] = np_arr.shape[0]
            self.data[f'{var_name}_path'] = f'{self.out_path}/{var_name}.bin32'
            if write:
                self.gradient()
                with open(f'{self.out_path}/{var_name}.bin32', 'wb') as f:
                    # metadata[f'{var}_binary_len'] = len(np_arr.tobytes())
                    f.write(np_arr.tobytes())
                    print(f'successfully wrote the {var_name} with {np_arr.shape} shape to {var_name}.bin32. ')

    def gradient(self) -> None:
        # calculate topography gradient
        tpx, tpy = np.gradient(self.data['topo'])
        tpxy = np.sqrt(np.power(tpx, 2) + np.power(tpy, 2))  # absolute value of the gradient
        tpxy = tpxy / np.max(np.max(tpxy))  # normalise to 1
        with open(self.out_path + '/grad.bin32', 'wb') as f:
            # metadata[f'{var}_binary_len'] = len(np_arr.tobytes())
            f.write(tpxy.tobytes())
            print(f'successfully wrote the grade with {tpxy.shape} shape to grad.bin32. ')

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='writing netCDF to binary file.')
#     parser.add_argument('path', type=str,
#                         help='path to the nc file!')
#     args = parser.parse_args()
#     write_netCDF_variables_to_bin32(args.path)
