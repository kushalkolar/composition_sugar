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

from bokeh.plotting import figure as figure, gridplot
from bokeh.colors.rgb import RGB
from bokeh.io import output_notebook, push_notebook, output_file, show
from bokeh.models import widgets
from .bases import BasePlot
from ..containers import *
from ..core import config
from typing import *


class Controls:
    def __init__(self, parent):
        self.output_file = parent.output_file
        self.controls = []

    def generate(self, container: Union[DataFrameContainer, ArrayContainer]):
        if isinstance(container, DataFrameContainer):
            self._generate_dataframecontainer(container)

    def _generate_dataframecontainer(self, container):
        self.data_column = widgets.Select(title='Data Column', options=container.dataframe.columns.to_list())
        self.labels_column = widgets.Select(title='Labels Column', options=container.dataframe.columns.to_list())

        self.controls = [self.data_column, self.labels_column]
        for c in self.controls:
            show(c)

    def _generate_arraycontainer(self):
        pass


class BokehScatter(BasePlot):
    def __init__(self):
        BasePlot.__init__(self)
        self.controls = Controls(self)

    def update_data(self, container: Union[DataFrameContainer, ArrayContainer]):
        pass

    def update_plot(self, ):
        pass
