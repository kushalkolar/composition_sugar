#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (C) 2019 Kushal Kolar

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from ..core import Container, hdftools
import pandas as pd
import numpy as np
from typing import Union


class DataFrameContainer(Container):
    def __init__(self, dataframe: pd.DataFrame):
        Container.__init__(self)
        self.dataframe = dataframe

    def to_dict(self) -> dict:
        pass

    @classmethod
    def from_hdf5(cls, path: str, key: str = 'DATAFRAME_CONTAINER'):
        df = pd.read_hdf(path, key=key, mode='r')
        return cls(df)

    def to_hdf5(self, path: str, key: str = 'DATAFRAME_CONTAINER'):
        pass

    def __add__(self, dataframe_container):
        self.dataframe = pd.concat([self.dataframe, dataframe_container.df])
        return self


class ArrayContainer(Container):
    def __init__(self, array: np.ndarray, labels: np.ndarray = None):
        Container.__init__(self)

        if array.shape != labels.shape:
            raise ValueError("Shape of array and labels must match exactly")

        self.array = array
        self.labels = labels

    def to_dict(self):
        return {'array': self.array, 'labels': self.labels}

    @classmethod
    def from_hdf5(cls, path: str, key: str = 'ARRAY_CONTAINER'):
        d = hdftools.load_dict(path, group=key)

        if ('array' not in d.keys()) or ('labels' not in d.keys()):
            raise TypeError("Not a valid ArrayContainer. File does not have required 'array' and 'labels' keys")

        return cls(**d)

    def to_hdf5(self, path, key: str = 'ARRAY_CONTAINER'):
        hdftools.save_dict(self.to_dict(), path, group=key)
