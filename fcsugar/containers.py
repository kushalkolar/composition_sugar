from .core import Container
import pandas as pd


class DataFrameContainer(Container):
    def __add__(self, dataframe_container):
        self.df = pd.concat([self.df, dataframe_container.df])
        return self
