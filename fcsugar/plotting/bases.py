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

from ..core import config, utils
from bokeh.io import output_notebook, push_notebook, output_file, show
from warnings import warn


class BasePlot:
    def __init__(self):
        if config.bokeh_output == 'notebook':
            output_notebook()
            self.output_file = None

        elif config.bokeh_output == 'external':
            self.output_file = utils.TempFile(ext='html')
            output_file(self.output_file.path)


class WidgetEntry:
    def __init__(self, setter: callable, getter: callable, name: str):
        self.setter = setter
        self.getter = getter
        self.name = name


class WidgetRegistry:
    """
    Register widgets to conveniently store and restore their states
    """

    def __init__(self):
        self.widgets = dict()

    def register(self, widget, setter: callable, getter: callable, name: str):
        """
        Register a widget. The `setter` and `getter` methods must be interoperable
        :param widget: widget to register
        :type widget: QtWidgets.QWidget
        :param setter: widget's method to use for setting its value
        :type setter: callable
        :param getter: widget's method to use for getting its value. This value must be settable through the specified "setter" method
        :type getter: callable
        :param name: a name for this widget
        :type name: str
        """
        if (not callable(setter)) or (not callable(getter)):
            raise TypeError('setter and getter must be callable')

        self.widgets[widget] = WidgetEntry(setter=setter, getter=getter, name=name)

    def get_state(self) -> dict:
        """Get a dict of states for all registered widgets"""
        s = dict()

        for w in self.widgets.keys():
            name = self.widgets[w].name
            s[name] = self.widgets[w].getter()

        return s

    def set_state(self, state: dict):
        """Set all registered widgets from a dict"""
        for w in self.widgets.keys():
            name = self.widgets[w].name

            # account for using old saved state files whilst control widgets change
            if name not in state.keys():
                warn(f'State not available for widget: {name}\n{w}')
                continue

            s = state[name]

            self.widgets[w].setter(s)
