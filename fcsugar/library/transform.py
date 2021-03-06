#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
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


from ..containers import DataFrameContainer
from ..core import *
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


@node
def LDA(container: DataFrameContainer, data_column: str, labels_column: str, n_components: int):
    X = np.vstack(container.dataframe[data_column].values)
    y = container.dataframe[labels_column]

    lda = LinearDiscriminantAnalysis(n_components=n_components)

    X_ = lda.fit_transform(X, y)

    container.dataframe['lda_transform'] = X_.tolist()
    container.dataframe['lda_transform'] = container.dataframe['lda_transform'].apply(np.array)

    return container
