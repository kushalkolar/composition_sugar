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

from . import config
from uuid import uuid4
import os
from typing import Optional


class TempFile:
    def __init__(self, name: Optional[str] = None,
                 parent_dir: Optional[str] = None,
                 ext: Optional[str] = None):
        """

        :param name: file name, creates a random name if not provided
        :param parent_dir: parent directory of file, uses .fcsugar config dir if not provided
        :param ext: file extension, file is created without extension if not provided
        """
        if name is None:
            name = str(uuid4())

        if parent_dir is None:
            parent_dir = config.config_dir

        if ext is None:
            ext = ''

        if ext.startswith('.'):
            ext = ext[1:]

        self.path = os.path.join(parent_dir, f"{name}.{ext}")

    def write(self, s: str, mode: str = 'w', **kwargs):
        with open(self.path, mode, **kwargs) as f:
            f.write(s)

    def writelines(self, l: list, mode: str = 'w', **kwargs):
        with open(self.path, mode, **kwargs) as f:
            f.writelines(l)

    def append(self, s: str, mode: str = 'a', **kwargs):
        with open(self.path, mode, **kwargs) as f:
            f.write(s)

    def read(self, mode: str = 'r', **kwargs) -> str:
        with open(self.path, mode, **kwargs) as f:
            s = f.read()

        return s

    def readlines(self, mode: str = 'r', **kwargs) -> list:
        with open(self.path, mode, **kwargs) as f:
            l = f.readlines()

        return l

    def __del__(self):
        os.remove(self.path)
