#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2019 Kushal Kolar
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from fcsugar import *
from ..containers import DataFrameContainer
import numpy as np
from typing import *


@node
def splice(container: DataFrameContainer, data_column: str, start: int, stop: int):
    container.dataframe['spliced'] = container.dataframe[data_column].apply(lambda a: a[start:stop])
    return container


@node
def partition(container: DataFrameContainer, n_partitions: int):
    size = container.dataframe.index.size

    ixs = np.array(range(size))

    partitions = np.array_split(ixs, n_partitions)
    labels = np.empty(shape=(size,), dtype=np.int64)

    for label, p in enumerate(partitions):
        labels[p] = label

    container.dataframe['partition'] = labels
    return container


# TODO: Create container for numpy arrays!
@node
def sample_partition(contrainer: DataFrameContainer, data_column: str, labels_column: str) -> np.ndarray:
    partitions = contrainer.dataframe[labels_column].unique()

    df = contrainer.dataframe

    samples = []
    for p in partitions:
        s = df[data_column][df[labels_column] == p].sample(1).values[0]
        samples.append(s)

    samples = np.array(samples)

    return samples


def _pad_arrays(a: np.ndarray, method: str = 'random', output_size: int = None, mode: str = 'minimum',
               constant: Any = None) -> np.ndarray:
    """
    Pad all the input arrays so that are of the same length. The length is determined by the largest input array.
    The padding value for each input array is the minimum value in that array.

    Padding for each input array is either done after the array's last index to fill up to the length of the
    largest input array (method 'fill-size') or the padding is randomly flanked to the input array (method 'random')
    for easier visualization.

    :param a: 1D array where each element is a 1D array
    :type a: np.ndarray

    :param method: one of 'fill-size' or 'random', see docstring for details
    :type method: str

    :param output_size: not used

    :param mode: one of either 'constant' or 'minimum'.
                 If 'minimum' the min value of the array is used as the padding value.
                 If 'constant' the values passed to the "constant" argument is used as the padding value.
    :type mode: str

    :param constant: padding value if 'mode' is set to 'constant'
    :type constant: Any

    :return: Arrays padded according to the chosen method. 2D array of shape [n_arrays, size of largest input array]
    :rtype: np.ndarray
    """

    l = 0  # size of largest time series

    # Get size of largest time series
    for c in a:
        s = c.size
        if s > l:
            l = s

    if (output_size is not None) and (output_size < l):
        raise ValueError('Output size must be equal to larger than the size of the largest input array')

    # pre-allocate output array
    p = np.zeros(shape=(a.size, l), dtype=a[0].dtype)

    # pad each 1D time series
    for i in range(p.shape[0]):
        s = a[i].size

        if s == l:
            p[i, :] = a[i]
            continue

        max_pad_en_ix = l - s

        if method == 'random':
            pre = np.random.randint(0, max_pad_en_ix)
        elif method == 'fill-size':
            pre = 0
        else:
            raise ValueError('Must specific method as either "random" or "fill-size"')

        post = l - (pre + s)

        if mode == 'constant':
            p[i, :] = np.pad(a[i], (pre, post), 'constant', constant_values=constant)
        else:
            p[i, :] = np.pad(a[i], (pre, post), 'minimum')

    return p


@node
def pad_arrays(container: DataFrameContainer, data_column, method: str = 'random'):
    data = _pad_arrays(container.dataframe[data_column].values, method=method)

    container.dataframe['pad_arrays'] = data.tolist()
    container.dataframe['pad_arrays'] = container.dataframe['pad_arrays'].apply(np.array)

    return container
