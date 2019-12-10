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
from inspect import getfullargspec, getsource
from typing import *


class Container:
    """
    Data Container
    """
    def __init__(self):
        self._log = []
        self.functions = {}

    @property
    def log(self) -> List[dict]:
        return self._log

    def __rshift__(self, node):
        arg_names = getfullargspec(node.process).args

        if 'self' in arg_names:
            arg_names.remove('self')
        arg_names = arg_names[1:]

        params = {**dict(zip(arg_names, node.args)),  # positional args
                  **node.kwargs
                  }

        self._log.append({node.name: params})

        if node.name not in self.functions.keys():
            self.functions[node.name] = getsource(node.process)

        result = node.process(self, *node.args, **node.kwargs)
        return result


class Node(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.name = self.__class__.__name__

    @abstractmethod
    def process(self, t, *args, **kwargs) -> Container:
        pass


def node(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        class _Node:
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs
                self.name = func.__name__

            def process(container, *args, **kwargs):
                pass

        n = _Node(*args, **kwargs)
        n.process = func

        return n
    return wrapper
