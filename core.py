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


class Container:
    """
    Data Container
    """
    def __rshift__(self, node):
        return node.process(self, *node.args, **node.kwargs)


class Node(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.node_name = self.__class__.__name__

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

            def process(container, *args, **kwargs):
                pass

        n = _Node(*args, **kwargs)
        n.process = func

        return n
    return wrapper
