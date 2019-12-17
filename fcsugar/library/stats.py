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


from ..core import *
from scipy.stats import zscore as _zscore
import numpy as np
from ..containers import DataFrameContainer


@node
def zscore(container: DataFrameContainer, data_column: str, axis: int = None):
    container.dataframe['zscore'] = container.dataframe[data_column].apply(lambda a: _zscore(a, axis=axis))
    return container
