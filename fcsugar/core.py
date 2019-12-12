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

from abc import ABCMeta, abstractmethod
from functools import wraps
from inspect import getfullargspec, getsource, signature
from typing import *
from traceback import format_exc
from ipywidgets import widgets
from IPython.display import display
from . import config
from collections import OrderedDict


class Container:
    """
    Data Container
    """

    def __init__(self):
        self._log = OrderedDict()
        self.functions = {}
        self.pipeline = []
        self.subs = []

        self.status_widget = widgets.Textarea(description='Status', value='',
                                              layout=widgets.Layout(width='80%'))
        display(self.status_widget)

# TODO: Think about how to deal with log if the pipeline is executed consecutively multiple times
    @property
    def log(self) -> List[dict]:
        d = OrderedDict()
        for node in self._log.keys():

            n_occurances = [item.split('.')[0] for item in list(d)].count(node.name)

            name = f"{node.name}.{n_occurances}"

            d[name] = self._log[node]
        return d

    def append_log(self, node):
        self._log[node] = node.params
        # self._log.append({node.name: node.params})

        if node.name not in self.functions.keys():
            self.functions[node.name] = getsource(node.process)

    def __rshift__(self, node):
        arg_names = getfullargspec(node.process).args

        if 'self' in arg_names:
            arg_names.remove('self')
        arg_names = arg_names[1:]

        params = {**dict(zip(arg_names, node.args)),  # positional args
                  **node.kwargs
                  }

        node.params = params

        self.pipeline.append(node)
        node.subscribe(lambda: self.execute_pipeline(clear=False))
        if config.show_gui:
            node.make_gui()
        return self

    def load_functions(self, globals: dict, locals: dict):
        for func in self.functions.values():
            exec(func, globals, locals)

    def execute_pipeline(self, clear=True):
        container = _execute_pipeline(self, clear=clear)

        for sub in container.subs:
            sub(container)

        return container

    def connect(self, func: callable):
        self.subs.append(func)


def _execute_pipeline(container: Container, ix=0, clear=True):
    if ix == len(container.pipeline):
        if clear:
            container.pipeline.clear()
        container.status_widget.value = f"\rYay! Pipeline computed without errors =D"
        return container

    node = container.pipeline[ix]
    container.append_log(node)

    container.status_widget.value = f"\rProcessing node: {node.name}"

    try:
        return _execute_pipeline(node.process(container, **node.params), ix + 1, clear=clear)
    except Exception as e:
        if clear:
            container.pipeline.clear()
        container.status_widget.value = str(e)
        container.status_widget.value = format_exc()

        return container


class Node(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        self.args = args
        self.kwargs = kwargs
        self.params = None

        self.subs = []

    @abstractmethod
    def process(self, t, *args, **kwargs) -> Container:
        pass

    def make_gui(self):
        sig = signature(self.process)

        # label = f"======= {self.name} =======\n"

        label = f"<b>{self.name}</b>"

        display(widgets.HTML(value=label))

        for i, arg_name in enumerate(sig.parameters):
            if i == 0:
                continue

            arg_type = sig.parameters[arg_name].annotation

            wd = dict(description=arg_name, value=self.params[arg_name])

            if arg_type is str:
                w = widgets.Text(**wd)
            elif arg_type is int:
                w = widgets.IntText(**wd)
            elif arg_type is float:
                w = widgets.FloatText(**wd)
            else:
                return

            w.observe(self.set_param)

            display(w)

    def set_param(self, widget):
        name = widget['owner'].description
        val = widget['owner'].value
        self.params[name] = val
        for sub in self.subs:
            sub()

    def subscribe(self, func: callable):
        self.subs.append(func)


def node(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        class _Node(Node):
            def __init__(self, *args, **kwargs):
                Node.__init__(self, *args, **kwargs)
                self.name = func.__name__

            def process(container, *args, **kwargs):
                pass

        n = _Node(*args, **kwargs)
        n.process = func

        return n

    return wrapper
