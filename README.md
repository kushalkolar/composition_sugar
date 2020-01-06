# Composition Sugar
Syntactic sugar for function composition in Python

See usage examples on binder\
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kushalkolar/composition_sugar/master)

Create readable pipelines for processing data. It is meant for quickly writing/organizing pipelines with wrapper functions that are frequently used.

```python
data >> FuncA(args) >> FuncB(args) >> FuncC(args) >> ...
```

This is equivalent to:

```python
FuncC(FuncB(FuncA(data, args), args), args)
```

#### Automatic GUI generation and updating live plots
Write a pipeline and automatically generate a GUI which can be used to process data that are fed into live plots. Uses ipywidgets.

**See the following notebook for details:** `examples/gui_live_plotting.ipynb`
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kushalkolar/composition_sugar/master)



#### Logging
Besides being more readable, the functions & parameters are logged. See the binder demo for more details.

```python
>>> pprint(container.log, width=20)

    [{'splice': {'data_column': '_RAW_CURVE',
                 'start': 0,
                 'stop': 2990}},
     {'normalize': {'data_column': 'spliced'}},
     {'rfft': {'data_column': 'normalize'}},
     {'absval': {'data_column': 'fft'}},
     {'log': {'data_column': 'absval'}},
     {'splice': {'data_column': 'log',
                 'start': 0,
                 'stop': 1000}},
     {'LDA': {'data_column': 'spliced',
              'labels_column': 'FCLUSTER_LABELS',
              'n_components': 2}}]

``` 

### Data Container

Define a data container

Example with pandas DataFrame:

```python
from fcsugar import Container

class DataFrameContainer(Container):
    def __init__(self, df: pd.DataFrame):
        self.df = df
        
    @classmethod
    def from_hdf5(cls, path: str, key: str):
        df = pd.read_hdf(path, key=key, mode='r')
        return cls(df)
````

### Processing Node

Simply use the `@node` decorator on a function to use it with a data container

Example that splices arrays in a specific DataFrame column:

```python
from fcsugar import node

@node
def splice(container, data_column, start, stop):
    container.df['spliced'] = container.df[data_column].apply(lambda a: a[start:stop])
    return container
```
        
Basic format:

```python
@node
def func(container, *args, **kwargs):
    # do stuff to container
    return container
```

**The first argument _must_ always be the data container**

You can also create more complex processing nodes by inheriting from Node:

```python
from fcsugar import Node

class Complex(Node):        
    def process(self, container, *args, **kwargs):
        # do more complex stuff
        something_complex = self.some_other_func()

        # do other stuff
        final_result = do_more_stuff(something_complex)

        # the container which went through complex processing
        return final_result

    def some_other_func(self, ...):
        # does some stuff

    def do_more_stuff(self, ...):
        # more stuff
```

See full examples on binder\
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kushalkolar/composition_sugar/master)
