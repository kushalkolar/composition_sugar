from matplotlib import cm as matplotlib_color_map
from typing import *
import numpy as np
from collections import OrderedDict


qual_cmaps = ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1',
              'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c']


def make_colormap(n_colors: int, cmap: str = 'hsv', output: str = 'bokeh',
                  spacing: str = 'uniform', alpha: float = 1.0) -> List[Union[str, np.ndarray]]:
    """
    If non-qualitative map: returns list of colors evenly spread through the chosen colormap.
    If qualitative map: returns subsequent colors from the chosen colormap

    :param n_colors: Numbers of colors to return

    :param cmap:     name of colormap

    :param output:   option: 'mpl' returns RGBA values between 0-1 which matplotlib likes,
                     option: 'bokeh' returns hex strings that correspond to the RGBA values which bokeh likes

    :param spacing:  option: 'uniform' returns evenly spaced colors across the entire cmap range
                     option: 'subsequent' returns subsequent colors from the cmap

    :param alpha:    alpha level, 0.0 - 1.0

    :return:         List of colors as either hex strings or numpy array with length n_colors
    """

    valid = ['mpl', 'bokeh']
    if output not in valid:
        raise ValueError(f'output must be one {valid}')

    valid = ['uniform', 'subsequent']
    if spacing not in valid:
        raise ValueError(f'spacing must be one of either {valid}')

    if alpha < 0.0 or alpha > 1.0:
        raise ValueError('alpha must be within 0.0 and 1.0')

    cm = matplotlib_color_map.get_cmap(cmap)
    cm._init()

    lut = (cm._lut).view(np.ndarray)

    lut[:, 3] *= alpha

    if spacing == 'uniform':
        if not cmap in qual_cmaps:
            cm_ixs = np.linspace(0, 210, n_colors, dtype=int)
        else:
            if n_colors > len(lut):
                raise ValueError('Too many colors requested for the chosen cmap')
            cm_ixs = np.arange(0, len(lut), dtype=int)
    else:
        cm_ixs = range(n_colors)

    colors = []
    for ix in range(n_colors):
        c = lut[cm_ixs[ix]]
        if output == 'bokeh':
            c = tuple(c[:3] * 255)
            hc = '#%02x%02x%02x' % tuple(map(int, c))
            colors.append(hc)
        else:
            colors.append(c)

    return colors


def get_colormap(labels: iter, cmap: str, **kwargs) -> OrderedDict:
    """
    Get a dict for mapping labels onto colors

    Any kwargs are passed to make_colormap()

    :param labels:  labels for creating a colormap. Order is maintained if it is a list of unique elements.
    :param cmap:    name of colormap

    :return:        dict of labels as keys and colors as values
    """
    if not len(set(labels)) == len(labels):
        labels = list(set(labels))
    else:
        labels = list(labels)

    colors = make_colormap(len(labels), cmap, **kwargs)

    return OrderedDict(zip(labels, colors))


def map_labels_to_colors(labels: iter, cmap: str, **kwargs) -> List[Union[str, np.ndarray]]:
    """
    Map labels onto colors according to chosen colormap

    Any kwargs are passed to make_colormap()

    :param labels:  labels for mapping onto a colormap
    :param cmap:    name of colormap
    :return:        list of colors mapped onto the labels
    """
    mapper = get_colormap(labels, cmap, **kwargs)
    return list(map(mapper.get, labels))
