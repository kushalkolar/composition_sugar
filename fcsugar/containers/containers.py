from ..core import Container
import pandas as pd


class DataFrameContainer(Container):
    def __init__(self, dataframe: pd.DataFrame):
        Container.__init__(self)
        self.dataframe = dataframe

    @classmethod
    def from_hdf5(cls, path: str, key: str):
        df = pd.read_hdf(path, key=key, mode='r')
        return cls(df)

    def __add__(self, dataframe_container):
        self.dataframe = pd.concat([self.dataframe, dataframe_container.df])
        return self
